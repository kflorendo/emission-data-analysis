from __future__ import (absolute_import, division, print_function)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex, Normalize
from matplotlib.patches import Polygon
from matplotlib.colorbar import ColorbarBase

import os.path
import csv
import StringIO

def getColor(emission):
    if emission < 100000:
        color = (0,0,1.0,0.1)
    elif emission < 1000000:
        color = (0,0,1.0,0.3)
    elif emission < 10000000:
        color = (0,0,1.0,0.5)
    elif emission < 60000000:
        color = (0,0,1.0,0.7) 
    elif emission < 100000000:
        color = (0,0,1.0,0.8)
    else:
        color = (0,0,1.0,1.0)
    return color

fig, ax = plt.subplots()

# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119,llcrnrlat=20,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

# Mercator projection, for Alaska and Hawaii
m_ = Basemap(llcrnrlon=-190,llcrnrlat=20,urcrnrlon=-143,urcrnrlat=46,
            projection='merc',lat_ts=20)  # do not change these numbers

#%% ---------   draw state boundaries  ----------------------------------------
## data from U.S Census Bureau
## http://www.census.gov/geo/www/cob/st2000.html
shp_info = m.readshapefile('st99_d00','states',drawbounds=True,
                           linewidth=0.45,color='gray')
shp_info_ = m_.readshapefile('st99_d00','states',drawbounds=False)

#%% ---------   open file and get emission dict  ------------------------------
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'emissions_data_set.csv') 

state_name_dict = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

coal_dict = {}
gas_dict = {}
petrol_dict = {}

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
        elif source == "Natural Gas":
            gas_dict[state_name] = co2_amt
        elif source == "Petroleum":
            petrol_dict[state_name] = co2_amt

def createMap(source_dict, title):
    #%% -------- choose a color for each state based on population density. -------
    colors={}
    statenames=[]
    cmap = plt.cm.hot_r # use 'reversed hot' colormap
    vmin = 0; vmax = 150000000 # set range.
    norm = Normalize(vmin=vmin, vmax=vmax)
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # skip DC and Puerto Rico.
        if statename not in ['District of Columbia','Puerto Rico'] and statename in source_dict:
            emission = source_dict[statename]
            # calling colormap with value between 0 and 1 returns
            # rgba value.  Invert color range (hot colors are high
            # population), take sqrt root to spread out colors more.
            colors[statename] = getColor(emission)
            #print(cmap(np.sqrt((emission-vmin)/(vmax-vmin)))[:3])
            #colors[statename] = cmap(np.sqrt((emission-vmin)/(vmax-vmin)))[:3]
        statenames.append(statename)
    
    #%% ---------  cycle through state names, color each one.  --------------------
    for nshape,seg in enumerate(m.states):
        # skip DC and Puerto Rico.
        if statenames[nshape] not in ['Puerto Rico', 'District of Columbia'] and statenames[nshape] in source_dict:
            #color = rgb2hex(colors[statenames[nshape]])
            #color = rgb2hex(colors[statenames[nshape]])
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
    HI_OFFSET_Y = 250000    # similar to above: Y offset for Hawaii
    AK_OFFSET_X = -250000   # X offset for Alaska (These four values are obtained
    AK_OFFSET_Y = -750000   # via manual trial and error, thus changing them is not recommended.)
    
    for nshape, shapedict in enumerate(m_.states_info):  # plot Alaska and Hawaii as map insets
        if shapedict['NAME'] in ['Alaska', 'Hawaii']:
            seg = m_.states[int(shapedict['SHAPENUM'] - 1)]
            if shapedict['NAME'] == 'Hawaii' and float(shapedict['AREA']) > AREA_1:
                seg = [(x + HI_OFFSET_X, y + HI_OFFSET_Y) for x, y in seg]
                color = colors[statenames[nshape]]
            elif shapedict['NAME'] == 'Alaska' and float(shapedict['AREA']) > AREA_2:
                seg = [(x*AK_SCALE + AK_OFFSET_X, y*AK_SCALE + AK_OFFSET_Y)\
                    for x, y in seg]
                color = colors[statenames[nshape]]
            poly = Polygon(seg, facecolor=color, edgecolor='gray', linewidth=.45)
            ax.add_patch(poly)
    
    ax.set_title(title)
    
    #%% ---------  Plot bounding boxes for Alaska and Hawaii insets  --------------
    light_gray = [0.8]*3  # define light gray color RGB
    x1,y1 = m_([-190,-183,-180,-180,-175,-171,-171],[29,29,26,26,26,22,20])
    x2,y2 = m_([-180,-180,-177],[26,23,20])  # these numbers are fine-tuned manually
    m_.plot(x1,y1,color=light_gray,linewidth=0.8)  # do not change them drastically
    m_.plot(x2,y2,color=light_gray,linewidth=0.8)
    
    #%% ---------   Show color bar  ---------------------------------------
    ax_c = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    cb = ColorbarBase(ax_c,cmap=cmap,norm=norm,orientation='vertical',
                    label=r'[population per $\mathregular{km^2}$]')
    
    plt.show()

createMap(coal_dict, 'U.S. Coal CO2 Emissions by State')