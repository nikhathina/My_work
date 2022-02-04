import rasterio
import numpy as np
from rasterio.plot import show
import matplotlib.pyplot as plt
import fiona
import geopandas as gpd

riverImage = rasterio.open('D://hatarilabs/Data/Rst/riverImage2.tif')
fig, ax = plt.subplots(figsize=(16,12))
show(riverImage)

redBand, greenBand, blueBand = riverImage.read(1), riverImage.read(2), riverImage.read(3)

#change data type
redBand = np.float32(redBand)
greenBand = np.float32(greenBand)
blueBand = np.float32(blueBand)

fig, ax = plt.subplots(figsize=(16,12))
plt.imshow(redBand)
plt.show ()

#calculate hatariIndex
hatariIndex = np.zeros(blueBand.shape)

hatariIndex[ (redBand > greenBand)] = 1
fig, ax = plt.subplots(figsize=(16,12))
plt.imshow(hatariIndex)
plt.colorbar(shrink=0.5)
plt.show ()

#calculate hatariIndex
hatariIndex = np.zeros(blueBand.shape)
#condition, straightline= or

hatariIndex[ (redBand > greenBand) |  (redBand > 70) & (redBand < 120)] = 1
fig, ax = plt.subplots(figsize=(16,12))
plt.imshow(hatariIndex)
plt.colorbar(shrink=0.5)
plt.show ()

#calculate hatariIndex
hatariIndex = np.zeros(blueBand.shape)

hatariIndex[ (redBand > greenBand)] = 1

#extract river from index
from rasterio.features import shapes

hatariIndex= hatariIndex.astype('float32')

riverShape = shapes(hatariIndex)

#print one coordinate
for river in riverShape:
    print(river)
    break
    #output type is geojson

#transform the row n columns to coordinates
def transformPoint(pair):
    lonlatPair = riverImage.xy(pair[1],pair[0])
    return lonlatPair

#test transformation
riverShape = shapes(hatariIndex)

#print one coordinate
for river in riverShape:
    print(river[0]['coordinates'])
    coordList = [transformPoint(pair) for pair in river[0]['coordinates'][0]]
    print(coordList)
    break    


#create line shapefile
riverShape = shapes(hatariIndex)

# define schema
schema = {
    'geometry':'LineString',
    'properties':[('ID','int')]
}

#open a fiona object
lineShp = fiona.open ('D:/hatarilabs/Data/Shp/riverLine.shp', mode='w', driver='ESRI Shapefile',
          schema = schema, crs = "EPSG:4326")

#print one coordinate
i=0
for river in riverShape:
    coords = river[0]['coordinates'][0]
    
    if len(coords) > 15:
        coordList = [transformPoint(pair) for pair in coords]

        rowDict = {
                    'geometry' : {'type':'LineString',
                                     'coordinates': coordList},
                    'properties': {'ID' : i},
                    }
        lineShp.write(rowDict)
        i+=1

lineShp.close()

riverImage = gpd.read_file('D://hatarilabs/Data/Shp/riverLine.shp')
fig, ax = plt.subplots(figsize=(16,12))
riverImage.plot (cmap= 'Greys', ax=ax, alpha=.5, markersize =10)
plt.show ()