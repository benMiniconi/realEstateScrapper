R = 6373.0
# radius of the Earth
import math
import pandas as pd
import geopy.distance

villeReference = [{"menerbes": [5.21667, 43.8333]}, {"bonnieux": [5.3, 43.8167]},
                  {"saint martin de re": [-1.36667, 46.2]}, {"sainte marie en re": [-1.3, 46.15]},
                  {"lourmarin": [5.36667, 43.7667]}, {"yvetot": [0.766667, 49.6167]}]


def calculDistance(latReference, longReference, lat2, long2):
    lat1 = math.radians(latReference)
    # coordinates

    lon1 = math.radians(longReference)
    lat2 = math.radians(lat2)
    lon2 = math.radians(long2)

    dlon = lon2 - lon1
    # change in coordinates

    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    # Haversine formula

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance






def getElligibleCities(cityDF):
    #cityDF = pd.read_csv("villes_france_with_coord.csv")
    cityList = cityDF['villeLowerCase'].array
    cityLong = cityDF['long'].array
    cityLat = cityDF['lat'].array
    cityDistanceAcceptable = {}

    for cityKey in range(0, len(cityList)):
        for ville in villeReference:
            villeName = list(ville.keys())
            distanceRaw = calculDistance(ville[villeName[0]][1], ville[villeName[0]][0], cityLat[cityKey], cityLong[cityKey])
        # distance2 = geopy.distance.vincenty((43.8333, 5.21667), (cityLat[cityKey], cityLong[cityKey])).km
            #print(distanceRaw)
            if distanceRaw < 15:
                #print("If")
                #print(cityKey, distanceRaw)
                #print(len(cityDistanceAcceptable))
                cityDistanceAcceptable[cityKey] = True
            elif distanceRaw >= 15:
                if cityKey in cityDistanceAcceptable.keys():
                    cityDistanceAcceptable[cityKey] = True if cityDistanceAcceptable[cityKey] else False
                else:
                    cityDistanceAcceptable[cityKey] = False




    cityDF.insert(5, column="cityDistanceAcceptable", value=list(cityDistanceAcceptable.values()))
    elligibleCity = cityDF[cityDF["cityDistanceAcceptable"] == True]
    compression_opts = dict(method='zip',
                            archive_name='out.csv')
    #elligibleCity.to_csv('elligibleCity.csv', index=False,)
    return elligibleCity
# cityDF.append(df2)


