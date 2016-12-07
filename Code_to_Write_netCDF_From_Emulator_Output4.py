# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 13:42:59 2016

@author: earkpr
"""

#%%

import string
import glob
import numpy as np
from netCDF4 import Dataset
import sys
##from Scientific.IO.NetCDF import NetCDFFile as Dataset
from numpy import arange, dtype # array module from http://numpy.scipy.org
import iris


## Path to run the python routine from:
path = '/nfs/a107/earkpr/ACID-PRUFF/Jill/'

base_dir = '/nfs/a107/earkpr/ACID-PRUFF/Jill/'
single_file = 'SAresults_N50_Lon9_Lat8_VL9.dat'

filename = 'SAresults'
variable = 'N50'
vertical_level = 'VL9'


reference_netCDF_file = '/nfs/a107/earkpr/ACID-PRUFF/Jill/ERF_PDPI_xmcta-xmdbi_xmdga-xmdoi_pm2006ANN_191_N48.nc'

#%%


longitude = [ 0, 3.75, 7.5, 11.25, 15, 18.75, 22.5, 26.25, 30, 33.75, 37.5,
    41.25, 45, 48.75, 52.5, 56.25, 60, 63.75, 67.5, 71.25, 75, 78.75, 82.5,
    86.25, 90, 93.75, 97.5, 101.25, 105, 108.75, 112.5, 116.25, 120, 123.75,
    127.5, 131.25, 135, 138.75, 142.5, 146.25, 150, 153.75, 157.5, 161.25,
    165, 168.75, 172.5, 176.25, 180, 183.75, 187.5, 191.25, 195, 198.75,
    202.5, 206.25, 210, 213.75, 217.5, 221.25, 225, 228.75, 232.5, 236.25,
    240, 243.75, 247.5, 251.25, 255, 258.75, 262.5, 266.25, 270, 273.75,
    277.5, 281.25, 285, 288.75, 292.5, 296.25, 300, 303.75, 307.5, 311.25,
    315, 318.75, 322.5, 326.25, 330, 333.75, 337.5, 341.25, 345, 348.75,
    352.5, 356.25]
    
for x in range(len(longitude)):
    longitude[x]=longitude[x]-180
    print x, longitude[x]

latitude = [-90, -87.5, -85, -82.5, -80, -77.5, -75, -72.5, -70, -67.5, -65,
    -62.5, -60, -57.5, -55, -52.5, -50, -47.5, -45, -42.5, -40, -37.5, -35,
    -32.5, -30, -27.5, -25, -22.5, -20, -17.5, -15, -12.5, -10, -7.5, -5,
    -2.5, 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5,
    35, 37.5, 40, 42.5, 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70,
    72.5, 75, 77.5, 80, 82.5, 85, 87.5, 90 ]
    
#%%
    
print longitude[34]
print latitude[-1]


#%%

## List files in the directory that are called SAresults*.dat 

#%%

final_array=[]

##  KP Should be able to get this info from the files 

nlon = 96 
nlat = 73
nppe = 26


#%% 

file_list_array=[]
lon_final_array=[]
lat_final_array=[]

## DEFINE ARRAYS TO BE READ FROM FILE
V_array=[]
D1_array=[]
Dt_array=[]
Main_Effect_array=[]
Total_Effect_array=[]


## LOOP OVER THE FILES, IN ORDER OVER LON THEN LATS
## Files are labled Lon1 - Lon96, Lat1 - Lat73
 
## KP_COMMENT:

# Jill asked for plots from 0 t0 360, but data is -180 to 180 (if you read lon in ascending numberical order)
# As long as the data is read in in from the netCDF it should be possible to plot either?  
# Need to check 

# JILL OPTIONS HERE

lon_gridbox_array = np.concatenate([range(48,97), range(1,48)], axis=0)
###lon_gridbox_array = np.concatenate([range(1,97)], axis=0)


#TRY UNCOMMENTING THE LINE BELOW AND COMMENTING OUT ONE TWO LINES BELOW
#for lon in range(1,97):
for lon in lon_gridbox_array:
    print lon
    for lat in range(1,74):
        with open(path+"SAresults_N50_Lon"+str(lon)+"_Lat"+str(lat)+"_VL9.dat", "r") as ins:
            filename=str(path+"SAresults_N50_Lon"+str(lon)+"_Lat"+str(lat)+"_VL9.dat")
            file_lon = str(lon)
            file_lat = str(lat)
            for line in ins:
                columns=line.split()
                col0=columns[0]
                col1=columns[1]            
                col2=columns[2]            
                col3=columns[3]
                col4=columns[4]
                final_array.append([filename,file_lon,file_lat,col0,col1,col2,col3,col4])
                file_list_array.append(filename)
                lon_final_array.append(file_lon)
                lat_final_array.append(file_lat)
                ##print 'lon=',lon,' lat=',lat,' file_lon=',file_lon, 'file_lat=',file_lat
                V_array.append(col0)
                D1_array.append(col1)
                Dt_array.append(col2)
                Main_Effect_array.append(col3)
                Total_Effect_array.append(col4)

#%%

lon_final_array = np.array(lon_final_array)
lat_final_array = np.array(lat_final_array)

V_array = np.array(V_array)
D1_array = np.array(D1_array)
Dt_array = np.array(Dt_array)
Main_Effect_array = np.array(Main_Effect_array)
Total_Effect_array = np.array(Total_Effect_array)

final_array_np = np.array(final_array)

## Reshape array from 1D to 3D for writing to netCDF 
lon_final_array = np.reshape(lon_final_array[:],(nppe,nlat,nlon), order='F')
lat_final_array = np.reshape(lat_final_array[:],(nppe,nlat,nlon), order='F')

#print "nlat = ", nlat
#print "nlon = ", nlon

print "LON"
print lon_final_array[:,0,0]
print ""
print lon_final_array[0,:,0]
print ""
print lon_final_array[0,0,:]
print ""
print ""
print ""
print ""
print "LAT"
print lat_final_array[:,0,0]
print ""
print lat_final_array[0,:,0]
print ""
print lat_final_array[0,0,:]
print ""
#
#sys.exit()
#
V_array_reshape = np.reshape(V_array[:], (nppe,nlat,nlon), order='F')
D1_array_reshape = np.reshape(D1_array[:], (nppe,nlat,nlon), order='F')
Dt_array_reshape = np.reshape(Dt_array[:], (nppe,nlat,nlon), order='F')
Main_Effect_array_reshape = np.reshape(Main_Effect_array[:], (nppe,nlat,nlon), order='F')
Total_Effect_array_reshape = np.reshape(Total_Effect_array[:], (nppe,nlat,nlon), order='F')

lon_array = []
lat_array = []
ppe_array = []

lon_array = map(float, range(0,nlon)) 
lat_array = map(float, range(0,nlat)) 
ppe_array = range(0,nppe) 

## Calculate lon / lat coordinates.
#%%
#lon_array = np.array(lon_array) * float(360.0 / nlon) - 180.0 + 1.875
#lat_array = np.array(lat_array) * float(180.0 / nlat) - 90.0 + 1.23287671
##

#print lon_array
#print lat_array

#%%

pp_array = np.array(ppe_array)

gridbox_number_lon = range(0,nlon)
gridbox_number_lat = range(0,nlat)

lat_array = np.array(lat_array)
lon_array = np.array(lon_array)


##print lat_array
print lat_final_array

# open a new netCDF file for writing.
ncfile = Dataset('/nfs/a107/earkpr/ACID-PRUFF/Jill/Output_netCDF_File.nc','w') 

# create the lat, lon and ppe dimensions.
ncfile.createDimension('latitude',nlat)
ncfile.createDimension('longitude',nlon)
ncfile.createDimension('ppe',nppe)

lats = ncfile.createVariable('latitude',dtype('float32').char,('latitude',))
lons = ncfile.createVariable('longitude',dtype('float32').char,('longitude',))

#lats[:] = np.array(lat_array,dtype=np.float32)
#lons[:] = np.array(lon_array,dtype=np.float32)
#%%
#lats[:] = np.array(latitude,dtype=np.float32)
#lons[:] = np.array(longitude,dtype=np.float32)

lats[:] = latitude
lons[:] = longitude

print latitude
print longitude

print lats
print lons

#%%
V = ncfile.createVariable('V',dtype('float32').char,('ppe','latitude','longitude'))
D1 = ncfile.createVariable('D1',dtype('float32').char,('ppe','latitude','longitude'))
Dt = ncfile.createVariable('Dt',dtype('float32').char,('ppe','latitude','longitude'))

V[:,:,:]  = np.array(V_array_reshape,dtype=np.float32)
D1[:,:,:] = np.array(D1_array_reshape,dtype=np.float32)
Dt[:,:,:] = np.array(Dt_array_reshape,dtype=np.float32)

# close the file.
ncfile.close()

#%%
