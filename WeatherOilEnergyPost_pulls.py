# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 13:58:57 2017

@author: jordy
"""




import urllib.request

 


def RetrieveData():
    ### ----------- RETRIEVE CURRENT SCHIPHOL WEATHER DATA --------------------
    ## DEFINE URL TO DOWNLOAD HTML TEXT FROM
    url = "http://www.knmi.nl/nederland-nu/weer/waarnemingen"
    
    ## REQUEST HTLM DATA FROM URL
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    output = response.read().decode('utf-8')
    
    ## RETRIEVE DATA FOR SPECIFIC LOCATION
    Location = 'Schiphol'
    index = str.find(output, Location)
    output_Location = output[index:index+260]
    output_Location = output_Location.strip().split('>')
    
    ## SPLIT DATA INTO MEASURED PROPERTIES
    date_time = output[str.find(output, 'uur<')-24:str.find(output, 'uur<')]
    data_CloudCoverDutch = output_Location[2]
    data_TempDegC = output_Location[4]
    data_RelHumidity = output_Location[6]
    data_WindDirComp = output_Location[8]
    data_WindSpdMtrps = output_Location[10]
    data_VisibilityMtr = output_Location[12]
    data_PressureHpa = output_Location[14]
    
    
    ## CREATE OUTPUT FOR MAIL CONTENT
    body_actual = 'Op '+Location+' on '+date_time+' is het '+data_CloudCoverDutch[:-4]+', '+data_TempDegC[:-4]+' degC ('+data_PressureHpa[:-4]+' hPa)'+' and wind direction is: '+data_WindDirComp[:-4]+' ('+data_WindSpdMtrps[:-4]+ ' m/s)'
    
    
    
    
    
    ### ----------- RETRIEVE WEATHER PREDICTION NEXT DAY ----------------------
    ## DEFINE URL TO DOWNLOAD HTML TEXT FROM
    url = "https://www.knmi.nl/nederland-nu/weer/verwachtingen"
    
    ## REQUEST HTLM DATA FROM URL
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    output = response.read().decode('utf-8')
    
    ## RETRIEVE DATA FOR SPECIFIC LOCATION
    index = str.find(output, 'weather-map__table-cell')
    output = output[index:index+1450]
    output = output.strip().split()
    
    ## SPLIT DATA INTO MEASURED PROPERTIES
    ref=0
    date_day = output[ref+1]
    date_date = output[ref+6]
    data_TempDegCMax = output[ref+18]
    data_Precipitation = output[ref+32]
    data_PrecipChance = output[ref+39]
    data_SunChance = output[ref+46]
    #    data_WindDir = output[ref+56]
    #    data_WindSpeed = output[ref+57]
    
    ## CREATE OUTPUT FOR MAIL CONTENT
    body_forecast = '\n\nThe predicted weather for '+date_day+' '+date_date[12:-7]+' is '+' '+data_Precipitation[0:-2]+' mm rain ('+data_PrecipChance[0:-1]+'% chance) at max. '+data_TempDegCMax[0:-5]+' degC and '+data_SunChance[0:-1]+'% chance of sun.'
    
    
    
    
    
    ### ----------- RETRIEVE RECENT OIL PRICE DATA ----------------------------
    ## DEFINE URL TO DOWNLOAD HTML TEXT FROM
    url = "https://www.quandl.com/collections/markets/crude-oil"
    #    url2 = "https://www.quandl.com/collections/markets/natural-gas"
    
    ## REQUEST HTLM DATA FROM URL
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    output = response.read().decode('utf-8')
    
    ## RETRIEVE DATA FOR SPECIFIC TAG
    tag = 'Today, '
    index = str.find(output, tag)
    output_tag = output[index:index+600]
    output_tag = output_tag.strip().split('"')
    
    ## SPLIT DATA INTO DESIRED PROPERTIES
    data_date = output_tag[5]
    data_WTI_USDpbbl = output_tag[11]
    data_Brent_USDpbbl = output_tag[23]
    
    ## CREATE OUTPUT FOR MAIL CONTENT
    body_oilprice = '\n\nRecent ('+data_date+'), oil prices are '+data_Brent_USDpbbl+' (Brent) and '+data_WTI_USDpbbl+' for WTI ($/bbl)' 
    
    body_mailsubject = 'Vandaag: '+data_CloudCoverDutch[:-4]+' ('+data_TempDegCMax[0:-5]+'degC), WTI at $'+data_WTI_USDpbbl+'/bbl'
    body_mailcontent = body_actual+body_forecast+body_oilprice
    
    
    
    return(body_mailcontent,data_WindDirComp)


    
    
    