import matplotlib.pyplot as plt
import os.path
import csv

directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(directory, 'death-rate-from-pm25-vs-pm25-concentration.csv') 
datafile = open(filename,'rb')

years = []
countries = []
num_deaths = []
pollution = []
sizes = []

datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    if int(row[2]) >= 2010 and row[3] != "" and row[4] != "" and row[5] != "":
        countries.append(row[0])
        years.append(int(row[2]))
        num_deaths.append(float(row[3]))
        pollution.append(float(row[4]))
        sizes.append(float(row[5])/100)

plt.scatter(pollution, num_deaths, c=[[0,0,0.54,0.3]], s=sizes, edgecolors=[[0.769,0.847,0.902,0.3]])
plt.xlabel('Mean Annual PM2.5 Air Pollution Exposure (micrograms per cubic meter)')
plt.ylabel('Number of Deaths (per 100,000)')
plt.title('PM2.5 Air Pollution since 2010 vs. Death Rate')
plt.text(35,20,'NOTE: Circle size corresponds to GDP per capita')
plt.show()