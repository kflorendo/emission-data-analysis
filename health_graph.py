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
GDPs = []

datareader = csv.reader(datafile) 
headers = datareader.next() # read first row and store separately
for row in datareader:
    if int(row[2]) >= 2011:
        countries.append(row[0])
        years.append(int(row[2]))
        num_deaths.append(round(float(row[3]),7))
        pollution.append(row[4])    
        GDPs.append(row[5])

plt.scatter(pollution, num_deaths, edgecolors='r')
plt.xlabel('Mean Annual PM2.5 Air Pollution Exposure (micrograms per cubic meter)')
plt.ylabel('Number of Deaths (per 100,000)')
plt.title('Death Rate vs. PM2.5 Air Pollution since 2011')
plt.show()