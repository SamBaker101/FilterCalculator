'''Sam Baker - 11/2020
Calculator for finding settling time and ripple in filters for PWM signals'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import pandas as pd


#Generate an array of rc values between rc_start and rc_stop with a step size of rc resolution
def create_rc_array(rc_start, rc_stop, rc_resolution):
    array = np.arange(rc_start, rc_stop, rc_resolution, dtype=float)
    return array


#Calculates period, time high and time low based on frequency and duty cycle
def get_period(frequency, duty_cycle):
    period = 1/frequency
    time_high = period*duty_cycle
    time_low = period*(1-duty_cycle)

    return period, time_high, time_low


#Given starting voltage, final voltage, rc and time solves step responce equation
def v_calc(v0, vf, rc, time):
    exponent = -(time/rc)
    v1 = vf
    v2 = v0 - vf

    return v1 + v2*math.exp(exponent)


#Iterates through list of rc values
#For each rc value will calculate v_high and_v_low for each step until v_high-v_high_last < v_resolution
def generate_values(rc_values, period, time_high, time_low, v_resolution, v_low, v_high):
    delta_v_list = []
    settling_times = []

    for rc in rc_values:
        time = 0
        v_start = v_low
        v_up_old = 5
        v_up = 0
        v_down = 0
        delta_v = 5
        while abs(v_up_old - v_up) > v_resolution:
            time = time + period
            v_up_old = v_up
            v_up = v_calc(v_down, v_high, rc, time_high)
            v_down = v_calc(v_up, v_low, rc, time_low)
            delta_v = abs(v_up-v_down)

        delta_v_list.append(delta_v)
        settling_times.append(time)

    return delta_v_list, settling_times


def main():
    #Declare parameters
    frequency = 980
    duty_cycle = 0.5

    rc_start = 0.001
    rc_stop = 0.01
    rc_resolution = 0.00001

    v_low = 0
    v_high = 5
    v_resolution = 0.01

    #create derived values
    rc_values = create_rc_array(rc_start, rc_stop, rc_resolution)
    period, time_high, time_low = get_period(frequency, duty_cycle)

    #Run calculations
    delta_v_list, settling_times = generate_values(rc_values, period, time_high, time_low, v_resolution, v_low, v_high)


    #Plotting
    sns.set_theme()

    ripple_frame = pd.DataFrame({'RC Values (1/s)': rc_values, 'Peak to Peak Voltage Ripple (V)': delta_v_list})
    settle_frame = pd.DataFrame({'RC Values (1/s)': rc_values, 'Settling Time (s)': settling_times})

    fig, ax = plt.subplots(1,2)

    sns.lineplot(x='RC Values (1/s)', y='Peak to Peak Voltage Ripple (V)', data=ripple_frame, ax=ax[0])

    sns.lineplot(x='RC Values (1/s)', y='Settling Time (s)', data=settle_frame, ax=ax[1])


    plt.show()



main()