# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 14:23:34 2017

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

import time
from WeatherOilEnergyPost_pulls import RetrieveData


# 
# 
ind = 1
SleepMins = 0.1

while ind < 6:
    
    #
    (body_mailcontent,data_WindDirComp) = RetrieveData()
    
    print()
    print(body_mailcontent)
    print()

    
    #
    time.sleep(SleepMins*60)

    #
    print('Loop: ',ind, '--------------------------------------------')
    ind = ind + 1
    
    
# 
# 




# 
# 




# 
# 





