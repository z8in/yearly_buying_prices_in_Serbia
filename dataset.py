import requests
from pandas.io.json import json_normalize
import pandas as pd
import json
import ssl
import matplotlib.pyplot as plt

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
    
# Data are from json file from public website from opendata.stat.gov.rs        
url = 'https://opendata.stat.gov.rs/data/WcfJsonRestService.Service1.svc/dataset/0306IND01/2/json'
dataset = pd.read_json(url)

print(dataset.info())

#converted values in "vrednost" to number format
dataset['vrednost'] = pd.to_numeric(dataset['vrednost'])

#printing all unique names in for of list so that i can be choosen for uniqe product
print('List of available product which you can enter is: ', ', '.join(dataset['nProizvod'].unique()))
product = str(input("Enter product name: "))

#creating variable for unique product
cond = dataset.loc[dataset['nProizvod'] == product]

#creating variable for unique year
year = dataset['god'].unique()


#ploting results in matplotlib
fig, ax = plt.subplots()
ax.stackplot(year, cond['vrednost'], alpha=0.5)

ax.legend(loc='upper left')
ax.set_title('Price of ' + str(product) + " from year " + str(dataset['god'].min()) + "-" + str(dataset['god'].max()))
ax.set_xlabel('Year')
ax.set_ylabel('price')

plt.show()
