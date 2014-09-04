#!/usr/bin/env python

#this compiles the data fetched by get_game_data.py
#it puts it in the json
#useage: cat data/game_data*csv | ./map.py

import json
import sys
#import scipy.io
import numpy as np
import collections
import csv

out = collections.defaultdict(dict)

with open('game_data_21_06_2014.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        cookie = row[0]
        if len(cookie.split('-')) != 5:
            continue
        
        cookie = ''.join(cookie.split('-'))
        cookie = cookie[:29]
        
        attempt = row[1]
        
        #HACK, 5th row is now supposed to be 3rd row
        temp = row[4]
        row[4] = row[3]
        row[3] = row[2]
        row[2] = temp        
        
        out[cookie][attempt] = [int(di) for di in row[2:]]
    
json.dump(out, open('data_by_cookie_v2.json','w'),indent=1)
#scipy.io.savemat('data_by_cookie.mat', {'data': out}, oned_as ='column')   
