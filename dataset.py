import requests
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
resp = requests.get(url, timeout=30)
resp.raise_for_status()

# Tolerate BOMs and whitespace; parse JSON with fallback
text = resp.text.lstrip("\ufeff").strip()
try:
    data = resp.json()
except ValueError:
    # Fallback parser if resp.json() fails (e.g., BOM or minor formatting)
    try:
        data = json.loads(text)
    except Exception as e:
        raise SystemExit(f"Failed to parse JSON from API. First 200 chars: {text[:200]}")

# Build DataFrame from parsed JSON
if isinstance(data, list):
    dataset = pd.DataFrame(data)
elif isinstance(data, dict):
    # Try common wrapper keys if provider changes shape
    for key in ("items", "data", "results", "value"):
        if key in data and isinstance(data[key], list):
            dataset = pd.DataFrame(data[key])
            break
    else:
        dataset = pd.json_normalize(data)
else:
    raise SystemExit("Unexpected JSON structure from the API.")

print(dataset.info())

#converted values in "vrednost" to number format
dataset['vrednost'] = pd.to_numeric(dataset['vrednost'])

#printing all unique names in for of list so that i can be choosen for uniqe product
print('List of available product which you can enter is: ', ', '.join(dataset['nProizvod'].unique()))
product = str(input("Enter product name: "))

#creating variable for unique product
cond = dataset.loc[dataset['nProizvod'] == product]

#creating variable for unique year
year = cond['god']


#ploting results in matplotlib
fig, ax = plt.subplots()
ax.stackplot(year, cond['vrednost'], alpha=0.5)

ax.set_title('Price of ' + str(product) + " from year " + str(dataset['god'].min()) + "-" + str(dataset['god'].max()))
ax.set_xlabel('Year')
ax.set_ylabel('Price')

plt.show()
