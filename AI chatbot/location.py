# Getting the user's device name and IP Address
import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(f"\nUser's device name is : {hostname}")
print(f"User's IP Address is : {IPAddr}\n")


# Hospitals dataset
import pandas as pd

hs_dataset = pd.read_csv("Hospital.csv")
hs_dataset.head()

# Fetching the required columns
hs_new = hs_dataset[['NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'WEBSITE', 'LATITUDE', 'LONGITUDE']].copy()
hs_new.head()

# Renaming the column names
hs_new=hs_new.rename(columns={'LATITUDE': 'LAT', 'LONGITUDE': 'LON'})

import math
def Dist(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def MinIndex(d):
  min = 1000
  index = 0
  for i in range(len(d)):
    if (min > d[i]):
      min = d[i]
      index = i
  return index

def FindDist(la, lo):
  dist = []
  for i in range(len(hs_new)):
    plat = hs_new['LAT'][i]
    plon = hs_new['LON'][i]
    d = Dist(la,lo,plat,plon)
    dist.append(d)
  ind = MinIndex(dist)

  # Printing the nearest hospital
  print(f"\nHospital Name : \n{hs_new['NAME'][ind]}")
  print(f"\n\nHospital Address : \n{hs_new['ADDRESS'][ind]},{hs_new['CITY'][ind]},{hs_new['STATE'][ind]} - {hs_new['ZIP'][ind]}")
  print(f"\n\nHospital Website : {hs_new['WEBSITE'][ind]}")
  # print(dist)

latitude = 24
longitude = 20
FindDist(latitude, longitude)
