from __future__ import (absolute_import, division, print_function)

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.patches import Polygon
import matplotlib as mpl

import os.path
import csv
import StringIO

# Get color for state based on amount of emissions
def getColor(emission):
    if emission < 5000000:
        color = (0,0,1.0,0.1)
    elif emission < 10000000:
        color = (0,0,1.0,0.3)
    elif emission < 25000000:
        color = (0,0,1.0,0.5)
    elif emission < 60000000:
        color = (0,0,1.0,0.7) 
    elif emission < 100000000:
        color = (0,0,1.0,0.8)
    else:
        color = (0,0,1.0,1.0)
    return color

fig, ax = plt.subplots()

# Map of lower 48 states
m = Basemap(llcrnrlon=-119,llcrnrlat=20,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# Alaska and Hawaii
m_ = Basemap(llcrnrlon=-190,llcrnrlat=20,urcrnrlon=-143,urcrnrlat=46,
            projection='merc',lat_ts=20)  # do not change these numbers

# draw state boundaries
shp_info = m.readshapefile('st99_d00','states',drawbounds=True,
                           linewidth=0.45,color='gray')
shp_info_ = m_.readshapefile('st99_d00','states',drawbounds=False)

# open emmisions data file
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'emissions_data_set.csv') 

state_name_dict = {
        'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa','AZ': 'Arizona','CA': 'California','CO': 'Colorado',
        'CT': 'Connecticut','DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia','GU': 'Guam','HI': 'Hawaii',
        'IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts',
        'MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi',
        'MT': 'Montana','NA': 'National','NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey',
        'NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania',
        'PR': 'Puerto Rico','RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah',
        'VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'
}

#initialize coal emission dictionary (key = state name, amt emissions = value)
coal_dict = {}

# populate dictionary by going line by line through file
with open(filename,'rb') as f:
    for _ in range(4):
        next(f)
    for line in f:
        separated = list(csv.reader(StringIO.StringIO(line), skipinitialspace=True))[0]
        print(separated)
        state_abbrev = separated[1]
        state_name = state_name_dict[state_abbrev]
        source = separated[3]
        co2_amt = int(separated[4].replace(',',''))
        if source == "Coal":
            coal_dict[state_name] = co2_amt

#function to crate map given dictionary and title for graph
def createMap(source_dict, title):
    colors={}
    statenames=[]
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # skip DC and Puerto Rico.
        if statename not in ['District of Columbia','Puerto Rico'] and statename in source_dict:
            emission = source_dict[statename]
            colors[statename] = getColor(emission)
        statenames.append(statename)
    
    # cycle through state names, color each one
    for nshape,seg in enumerate(m.states):
        # skip DC and Puerto Rico
        if statenames[nshape] not in ['Puerto Rico', 'District of Columbia'] and statenames[nshape] in source_dict:
            color = colors[statenames[nshape]]
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
        elif statenames[nshape] not in source_dict:
            color = (0,0,0,0.3)
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
    
    AREA_1 = 0.005  # exclude small Hawaiian islands that are smaller than AREA_1
    AREA_2 = AREA_1 * 30.0  # exclude Alaskan islands that are smaller than AREA_2
    AK_SCALE = 0.19  # scale down Alaska to show as a map inset
    
    HI_OFFSET_X = -1900000  # X coordinate offset amount to move Hawaii "beneath" Texas
    HI_OFFSET_Y = 250000    # Y offset for Hawaii
    AK_OFFSET_X = -250000   # X offset for Alaska
    AK_OFFSET_Y = -750000   # Y offset for Alaska
    
    for nshape, shapedict in enumerate(m_.states_info):  # plot Alaska and Hawaii as map insets
        if shapedict['NAME'] in ['Alaska', 'Hawaii']:
            seg = m_.states[int(shapedict['SHAPENUM'] - 1)]
            if shapedict['NAME'] == 'Hawaii' and float(shapedict['AREA']) > AREA_1 and "Hawaii" in source_dict:
                seg = [(x + HI_OFFSET_X, y + HI_OFFSET_Y) for x, y in seg]
                color = colors[statenames[nshape]]
            elif shapedict['NAME'] == 'Alaska' and float(shapedict['AREA']) > AREA_2 and "Alaska" in source_dict:
                seg = [(x*AK_SCALE + AK_OFFSET_X, y*AK_SCALE + AK_OFFSET_Y)\
                    for x, y in seg]
                color = colors[statenames[nshape]]
            poly = Polygon(seg, facecolor=color, edgecolor='gray', linewidth=.45)
            ax.add_patch(poly)
    
    # add title
    ax.set_title(title)
    
    # plot bounding boxes for Alaska and Hawaii insets
    light_gray = [0.8]*3  # define light gray color RGB
    x1,y1 = m_([-190,-183,-180,-180,-175,-171,-171],[29,29,26,26,26,22,20])
    x2,y2 = m_([-180,-180,-177],[26,23,20])
    m_.plot(x1,y1,color=light_gray,linewidth=0.8)
    m_.plot(x2,y2,color=light_gray,linewidth=0.8)
    
    # show color bar
    ax_c = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    
    cmap = mpl.colors.ListedColormap([(0,0,1.0,0.1), (0,0,1.0,0.3), (0,0,1.0,0.5), (0,0,1.0,0.7), (0,0,1.0,0.8), (0,0,1.0,1.0)])     
    bounds = [0, 5000000, 10000000, 25000000, 60000000, 100000000, 150000000]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    
    cb = mpl.colorbar.ColorbarBase(ax_c, cmap=cmap,
                                norm=norm,
                                boundaries=bounds,
                                ticks=bounds,
                                spacing='proportional',
                                orientation='vertical')
                                
    cb.ax.tick_params(labelsize=5) 
    
    plt.show()

createMap(coal_dict, 'U.S. Carbon Dioxide Emissions by State in 2017 (Metric Tons)')