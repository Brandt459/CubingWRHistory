from bs4 import BeautifulSoup
import requests
import csv
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

data = requests.get(
    'https://www.worldcubeassociation.org/results/records?show=history')

soup = BeautifulSoup(data.text, 'html.parser')

with open('data.csv', 'w', encoding='utf-8') as csvfile:
    csvfile.truncate()

events = ('3x3', '2x2', '4x4', '5x5', '6x6', '7x7', '3x3 Blindfolded', '3x3 FMC', '3x3 OH', 'Clock', 'Megaminx',
          'Pyraminx', 'Skewb', 'Square-1', '4x4 Blindfolded', '5x5 Blindfolded', '3x3 Multi-Blind', '3x3 With Feet', 'Magic', 'Master Magic', '3x3 Multi-Blind Old Style')

# Grab world record history and store in "data.csv"
i = 0
for tbody in soup.find_all('tbody'):
    for tr in tbody.find_all('tr'):
        date = tr.find('td', class_='date').text.strip()
        try:
            single = tr.find('td', class_='single').text.strip()
        except:
            continue
        name = tr.find('td', class_='name').text.strip()
        country = tr.find('td', class_='country').text.strip()
        competition = tr.find('td', class_='competition').text.strip()
        with open('data.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [events[i], date, single, name, country, competition])
    i += 1

# Declare "event" variable and store date and solve time for each world record
dates = []
times = []
event = '3x3'
with open('data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    for row in reader:
        if row[0] == event:
            row[1] = row[1].replace(',', '').split()
            row[1][0] = str(months[row[1][0]])
            row[1] = '/'.join(row[1])
            dates.append(row[1])
            if row[2].count(' ') > 0:
                row[2] = row[2][-1]
            times.append(row[2])

# Plot data
x = [datetime.strptime(d, '%m/%d/%Y').date() for d in dates]
y = times
plt.plot(x, y, marker='o')
plt.xlabel('Year')
plt.ylabel('Time')
axes = plt.gca()
axes.set_xlim([x[-1], x[0]])
axes.set_ylim([y[0], y[-1]])
plt.show()
