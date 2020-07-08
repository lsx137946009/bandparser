#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 15:45:47 2019

@author: lsx
"""

import numpy as np
import time

def function_date_parse(frame, date0_loc, date1_loc, date2_loc, date3_loc):
    date0 = '{:08b}'.format(frame[date0_loc]) 
    date1 = '{:08b}'.format(frame[date1_loc])
    date2 = '{:08b}'.format(frame[date2_loc])
    date3 = '{:08b}'.format(frame[date3_loc])
    date = (date0+date1+date2+date3)[::-1]
    date_sec  = int(date[0 : 5], 2)
    date_min  = int(date[6 :11], 2)
    date_hour = int(date[12:16], 2)
    date_day  = int(date[17:21], 2)
    date_mon  = int(date[22:25], 2)
    date_year = int(date[26:31], 2) + 2000
    time_ = time.struct_time(
            tm_year=date_year, 
            tm_mon =date_mon, 
            tm_mday=date_day, 
            tm_hour=date_hour, 
            tm_min =date_min, 
            tm_sec =date_sec)
    return time_
    
def function_byte_shift(byte_list):
    byte_list.reverse()
    data_len = len(byte_list)
    shift = np.array(list(map(lambda x: 2**x, range(0, data_len*8, 8)))) # [1, 256, 65536, ...]
    data = np.array(byte_list)
    value = float(np.dot(shift, data))
    return value
    
def function_byte_shift_sign(byte_list):
    sign = byte_list.pop(0)
    if sign == 0:
        sign = -1
    elif sign == 1:
        sign = 1
    else:
        value = None
    value = function_byte_shift(byte_list)
    value = float(sign*value)
    return value

kind_field_mapping = [
                   [int(0xff), int(0xa1)],
                   [int(0xff), int(0x84)]
                  ]
                        
def function_kind_parse(kind_list):   
    byte_kind = function_byte_shift(kind_list)
    kind = kind_field_mapping[byte_kind]
    return kind                    
                        
def function_time_ts2sec(time):
    return time

time_func_mapping = {'sec': function_time_ts2sec}                       
                        