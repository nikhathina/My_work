import pandas as pd
import folium
import numpy as np
import webbrowser
import folium.plugins as plugins

'''#read-excel-with-sheet-name
ff= pd.read_excel('D://address_geocode/Lab7Data/C-U_restaurants.xlsx', sheet_name= 'FF')
#print (ff)
#define-dataframe
df = pd.DataFrame(ff, columns= ['ID', 'ID Code', 'Facility Name', 'Address', 'City', 'State', 'Zip'])
#create-one-column-by-adding-3
df["addresses"]= df["Address"].map(str)+ ',' +df["City"].map(str)+ ',' + df["State"].map(str)+ ',' + df ["Zip"].map(str) 
#ad = df['addresses']
print (df['addresses'])

df2= pd.DataFrame(ff, columns= ['ID', 'ID Code', 'Facility Name'])
df3= df2.insert(3, 'addresses', df ['addresses'])

#save-output-files-as-csv-and-excel
df.to_csv('D://address_geocode/Lab7Data/new_file.csv', index = False) 
#df.to_excel('D://address_geocode/Lab7Data/new_file.xls', index = False)

df= pd.read_csv ('new_file.csv')
#remove-unwanted-columns
df= df.drop (['Address', 'City', 'State', 'Zip'], axis=1)
print (df.head())
# Import the geocoding tool
from geopandas.tools import geocode
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

locator = Nominatim (user_agent='Nikhat_hina')
# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# 2- - create location column
df['location'] = df['addresses'].apply(geocode)
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
# 4 - split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)

print (df)
df.to_csv('D://address_geocode/Lab7Data/geocoded_addresses.csv', index = False)'''

#import csv
df = pd.read_csv ('D://address_geocode/Lab7Data/geocoded_addresses.csv')
print (df.head())

count_nan = df['location'].isnull().sum()
print ('Count of NaN: ' + str(count_nan)) #count-nan-values
nan_values= df[df.isna().any(axis=1)] #select all rows-with-nan-values
print (nan_values)
'''df= pd.DataFrame(nan_values, columns= ['ID','ID Code', 'Facility Name', 'addresses'])
print (df)
df.to_csv('D://address_geocode/Lab7Data/ungeocoded_addresses.csv', index = False)'''
nan_value = float("NaN")
#Convert NaN values to empty string

df.replace("", nan_value, inplace=True)

df.dropna(subset = ["location", "latitude", "longitude", "point", "altitude"], inplace=True)

print (df.head())

#df= ['geocoded_add']
np.where (df.applymap(lambda x: x == ''))

map1 = folium.Map(location=(40.14, -88.21), tiles='cartodbpositron', zoom_start=12)
df.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]]).add_to(map1), axis=1)


#display (map1)

folium_map = folium.Map(location=(40.14, -88.21),
                        zoom_start=12,
                        tiles='cartodbpositron')


plugins.FastMarkerCluster(data=list(zip(df['latitude'].values, df['longitude'].values))).add_to(folium_map)
folium.LayerControl().add_to(folium_map)
folium_map
#Display the map
folium_map.save("map.html")
webbrowser.open("map.html")