'''
Created on 2014-06-02

@author: iman

input:
value: is the last observed glucose level

output:
msg_fast_deviating: indicating if the glucose level is changing too rapidly.
-1 means glucose level is falling rapidly.
1 means glucose level is rising rapidly.
0 means there is not rapid changes.
msg_threshold: indicating that which direction the glucose level moving
-1 means that it is falling.
1 means that it is rising.
time_to_go: shows the estimated time before the glucose level reaches either of the
thresholds
note: 0 means that the glucose level is already at either of the thresholds
'''
import numpy as np

__Y = None
__M = None
__std_counter = None

history_window_size = 12 #eq. to 1 hour of data
low_threshold = 4.5
high_threshold = 7.4
std_coef = 3#the deviation from mean is supposed to stay less than std_coef times of std
std_counter_max = 6 #number of times the deviation is more than std_coef*std

def Glucose_Predictor(value):
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

        std = np.std(__Y)
        mean = np.mean(__Y)
        msg_fast_deviating = 0
        if (value - mean) > std_coef* std:
                __std_counter += 1
                if __std_counter == std_counter_max:
                        msg_fast_deviating = 1
        elif (mean - value) < std_coef* std:
                __std_counter += 1
                if __std_counter == std_counter_max:
                        msg_fast_deviating = -1
        else:
                __std_counter = 0

        __Y[range(history_window_size - 1)] = __Y[range(1, history_window_size)]#shift
        __Y[history_window_size - 1] = value#insert the new value
        msg = []


        if value < low_threshold:
                msg_threshold = -1
                time_to_go = 0
        elif value > high_threshold:
                msg_threshold = 1
                time_to_go = 0
        else:
                params = __M*__Y#update the parameters
                next_low = (low_threshold - params[1])/(params[0]+ np.finfo(np.float64).eps)
                if next_low > 0:
                        msg_threshold = -1
                        time_to_go = next_low * 5
                else:
                        next_high = (high_threshold - params[1])/(params[0] + np.finfo(np.float64).eps)
                        if next_high > 0:
                                msg_threshold = 1
                                time_to_go = next_high * 5
                        else:
                                time_to_go = 0
                                if np.abs(mean - high_threshold) < np.abs(mean - low_threshold):
                                        msg_threshold = 1
                                else:
                                        msg_threshold = -1


        return msg_fast_deviating, msg_threshold, int(time_to_go)