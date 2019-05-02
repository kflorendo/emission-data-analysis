import matplotlib.pyplot as plt
import os.path
import csv

# open CSV file containing data
directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'death-rate-from-pm25-vs-pm25-concentration.csv') 
datafile = open(filename,'rb')

# create 5 empty arrays
countries = []
num_deaths = []
pollution = []
sizes = []
font_sizes = []

# iterate through each row in CSV file
datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    if int(row[2]) >= 2010 and row[3] != "" and row[4] != "" and row[5] != "": # chooses data points since 2010, ignores empty data cells
        countries.append(row[0])
        num_deaths.append(float(row[3]))
        pollution.append(float(row[4]))
        sizes.append(float(row[5])/100)
    
# makes font size related to country GDP (dot size)
for i, size in enumerate(sizes):
    if countries[i] in ["Mauritius", "Malta", "Luxembourg", "Madagascar", "Cyprus", "Netherlands", "Austria", "Cote d'Ivoire", "Cambodia", "Armenia", "Kenya", "Saint Lucia", "Antigua and Barbuda", "Israel", "Italy", "Uruguay", "Bahamas", "Ecuador", "Barbados", "Burundi", "Moldova", "Swaziland", "Haiti", "Algeria", "Mozambique", "Morocco", "Latvia", "Slovakia", "Botswana", "Sao Tome and Principe", "Dominican Republic", "Saint Vincent and the Grenadines", "Suriname", "Thailand", "Paraguay", "Colombia", "Iceland", "Ireland", "Panama", "Portugal", "Japan", "France", "Spain", "New Zealand", "Belgium"]:
        font_sizes.append("no")
    elif num_deaths[i] < 30:
        font_sizes.append(5)
    else:
        if size > 900:
            font_sizes.append(12)
        elif size > 300:
            font_sizes.append(8)
        elif size > 150:
            font_sizes.append(6)
        else:
            font_sizes.append(5)

# creates scatter plot
plt.scatter(pollution, num_deaths, c=[[0,0,0.54,0.3]], s=sizes, edgecolors=[[0.769,0.847,0.902,0.3]])
for i, txt in enumerate(countries):
    if font_sizes[i] != "no":
        if countries[i] == "Saudi Arabia":
            plt.annotate(txt, (pollution[i], num_deaths[i]), xytext = (126,102), fontsize = font_sizes[i])
        else:    
            plt.annotate(txt, (pollution[i], num_deaths[i]), fontsize = font_sizes[i])
plt.xlabel('Mean Annual PM2.5 Air Pollution Exposure (micrograms per cubic meter)')
plt.ylabel('Number of Deaths (per 100,000)')
plt.title('PM2.5 Air Pollution since 2010 vs. Death Rate')
plt.text(35,20,'NOTE: Circle size corresponds to GDP per capita')
plt.show()