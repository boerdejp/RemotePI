# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 19:20:00 2017

@author: jordy
"""

# 
# 
# 
# 
# 
# 
# 



# 
# 
import pandas as pd
import urllib.request
import datetime
import numpy as np


# LOAD DATA
# 
outfit = pd.read_csv('outfit_data.txt', names = ["Daylight", "Windspeed", "Temperature", "Rain", "Shorts", "Long pants","Sweater","Wind jack","Rain jacket"])
outfit.head
outfit.describe().transpose()
outfit.shape




# GRAB DATA FROM KNMI
#
url = "http://www.knmi.nl/nederland-nu/weer/waarnemingen"
#
# REQUEST HTLM DATA FROM URL
print()
print('---')    
print()
print('Pulling data from knmi.nl ...')
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
output = response.read().decode('utf-8')
#
# RETRIEVE DATA FOR SPECIFIC LOCATION
Location = 'Schiphol'
index = str.find(output, Location)
output_Location = output[index:index+260]
output_Location = output_Location.strip().split('>')
#
# SPLIT DATA INTO MEASURED PROPERTIES
date_time = output[str.find(output, 'uur<')-19:str.find(output, 'uur<')]
#
now_temperature_string = output_Location[4]
now_temperature = float(now_temperature_string[0:-4])
#
now_windspeed_string = output_Location[10]
now_windspeed = float(now_windspeed_string[0:-4])
#
now_rain_string = output_Location[2]
now_rain = 0
if now_rain_string[0:-4] == 'af en toe lichte regen':
    now_rain = 1
elif now_rain_string[0:-4] == 'motregen en regen':
    now_rain = 1
    
print('Pulling data from knmi.nl ... DONE')




# GRAB DATA FROM TIMEANDDATE
#
url = "https://www.timeanddate.com/sun/netherlands/amsterdam"
#
# REQUEST HTLM DATA FROM URL
print()
print('Pulling data from timeanddate.com ...')
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
output = response.read().decode('utf-8')
#
# RETRIEVE DATA FOR SPECIFIC LOCATION
Trigger = 'Next Equinox'
index = str.find(output, Trigger)
output_Trigger = output[index:index+260]
#
today_sunrise = str(output_Trigger[218:223])
today_sunset = str(output_Trigger[134:139])

sunrise = datetime.datetime.strptime(today_sunrise,'%H:%M')
sunset = datetime.datetime.strptime(today_sunset,'%H:%M')
dnow = datetime.datetime.now()

if dnow > sunrise is True:
    if dnow < sunset is True:
        now_daylight = 1
else:
    now_daylight = 0
print('Pulling data from timeanddate.com ... DONE')
print()
print('---')    
print()
print('According to KNMI.nl its now '+str(now_temperature)+' degrees, wind speed is '+str(now_windspeed)+' m/s and '+now_rain_string[0:-4])




# SPLIT DATA TO INPUT (PROPERTIES) AND OUTCOME (CULTIVATOR)
# 
X = outfit.ix[:,0:4]
y = outfit.ix[:,4:9]



# SPLIT DATA INTO TRAIN- AND TEST SUBSETS
# 
# official method
from sklearn.model_selection import train_test_split
#
# to TRAIN and TEST use this:
X_train, X_test, y_train, y_test = train_test_split(X, y)
# to apply, use this:
X_train = X
y_train = y
X_now = np.array([[ now_daylight, now_windspeed, now_temperature, now_rain],[ now_daylight, now_windspeed, now_temperature, now_rain ]])



# SCALE DATA
# 
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# 
scaler.fit(X_train)
StandardScaler(copy=True, with_mean=True, with_std=True)
# 
#print(X_test)
X_test_pre = X_test
X_train = scaler.transform(X_train)
#X_test = scaler.transform(X_test)
X_now = scaler.transform(X_now)



# SETUP ANN
# 
from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(4,5,6,5),max_iter=5000)



# FIT ANN TO TRAINING DATA
# 
mlp.fit(X_train,y_train)



# APPLY ANN TO TEST DATA, USE ANN TO PREDICT OUTCOMES
# 
predictions_test = mlp.predict(X_test)
predictions_now = mlp.predict(X_now)




# 
# 
#print(predictions)

weather = X_test_pre.iloc[-1,:]
# daylight [0/1]
weather_daylight = weather[0]
# wind spead [m/s]
weather_windspeed = weather[1]
# temperature [degC]
weather_temperature = weather[2]
# rain [0/1]
weather_rain = weather[3]

suggestion = predictions_now[-1,:]
# shorts
sugg_shorts = suggestion[0]
# long pants
sugg_longs = suggestion[1]
# sweater
sugg_sweater = suggestion[2]
# wind jack
sugg_windjack = suggestion[3]
# raincoat
sugg_raincoat = suggestion[4]


#
if now_daylight == 0:
    daytext = 'Right now, there is no daylight,'
else: 
    daytext = 'Right now, there is daylight,'
if now_rain == 0:
    raintext = 'and no rain,'
else:
    raintext = 'and rain,'    

if sugg_shorts == 1:
    shortstext = ' shorts'
    shortsYN = '(YES)'
    shortsY = ' shorts'
    shortsN = ''
else:
    shortstext = ''
    shortsYN = '(no)'
    shortsY = ''
    shortsN = ', shorts'
if sugg_longs == 1:
    longstext = ', tights'
    longsYN = '(YES)'
    longsY = ', tights'
    longsN = ''
else:
    longstext = ''
    longsYN = '(no)'
    longsY = ''
    longsN = ', tights'
if sugg_sweater == 1:
    sweatertext = ', a sweater'
    sweaterYN = '(YES)'
    sweaterY = ', a sweater'
    sweaterN = ''
else:
    sweatertext = ''
    sweaterYN = '(no)'
    sweaterY = ''
    sweaterN = ', a sweater'
if sugg_windjack == 1:
    windjacktext = ', a wind stopper'
    windjackYN = '(YES)'
    windjackY = ', a wind stopper'
    windjackN = ''
else:
    windjacktext = ''
    windjackYN = '(no)'
    windjackY = ''
    windjackN = ', a wind stopper'
if sugg_raincoat == 1:
    raincoattext = ', a rain jacket'
    raincoatYN = '(YES)'
    raincoatY = ', a rain jacket'
    raincoatN = ''
else:
    raincoattext = ''
    raincoatYN = '(no)'
    raincoatY = ''
    raincoatN = ', a rain jacket'


print()
print('-> I suggest you wear'+shortsY+', a shirt'+longsY+sweaterY+windjackY+raincoatY)
if sum( sugg_shorts + sugg_longs + sugg_sweater + sugg_windjack + sugg_raincoat ) == 6:
    # print nothing, all is suggested to be worn    
    print()
else:
    print()
    print('(No need to bring'+shortsN+longsN+sweaterN+windjackN+raincoatN,')')
    
print()
print('---')    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
