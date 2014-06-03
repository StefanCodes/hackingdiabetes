'''
Created on 2014-06-02

@author: iman
'''
import numpy as np

__Y = None
__M = None
__std_counter = None

history_window_size     = 12 #eq. to 1 hour of data
low_threshold           = 4.5
high_threshold          = 7.4
std_coef                = 3#the deviation from mean is supposed to stay less than std_coef times of std
std_counter_max         = 6 #number of times the deviation is more than std_coef*std

def Glucose_Predictor(y):
        global __Y
        global __M
        global __std_counter
        
        if __Y is None:
                __Y = np.zeros(shape=(history_window_size, 1))
        if __M is None:
                X = np.ones (shape=(history_window_size, 1))
                X = np.matrix(np.column_stack((range(-history_window_size + 1, 1), X)))
                __M = (X.T*X).I*X.T
        if __std_counter is None:
                __std_counter = 0
                
        std  = np.std(__Y)
        mean = np.mean(__Y)
        if np.abs(y - mean) > std_coef* std:
                __std_counter += 1
                if __std_counter == std_counter_max:
                        msg = 'Rising Very Fast'
                        print msg
        else:
                __std_counter = 0

        __Y[range(history_window_size - 1)] = __Y[range(1, history_window_size)]#shift
        __Y[history_window_size - 1] = y#insert the new value
        msg = []
        if y < low_threshold:
                msg = "Below Lower Threshold: %s" % y
        elif y > high_threshold:
                msg = "Above Higher Threshold: %s" % y
        else:
                params = __M*__Y#update the parameters
                next_low = (low_threshold - params[1])/(params[0]+ np.finfo(np.float64).eps)
                if next_low > 0:
                        msg = "Next Low Happening in %d  min" % (next_low[0]*5)
                else:
                        next_high = (high_threshold - params[1])/(params[0] + np.finfo(np.float64).eps)
                        if next_high > 0:
                                msg = "Next High Happening in %d  min" % (next_high[0]*5)

