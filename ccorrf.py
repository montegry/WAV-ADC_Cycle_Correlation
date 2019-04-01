import numpy as np
import math


def cyc_corr(buff_in, period):
    # print(buff_in[:30])
    # counting size of I,Q array
    if len(buff_in) % 2 == 0:
        i_q_arr_size = int(len(buff_in)/2)
    else:
        i_q_arr_size = int(len(buff_in)/2)
        buff_in = buff_in[:len(buff_in)-1]
    # -------------------------------
    i_q_array = np.array(buff_in).reshape(i_q_arr_size, 2)
    # print("I,Q array size:{0}\n I,Q array:{1}".format(len(i_q_array), i_q_array[:3]))
    phase_array = phase(i_q_array)
    frequency_array = frequency(i_q_array)
    # print("Phase array size:{0}\n Freq array size:{1}".format(len(phase_array), len(frequency_array)))
    ph_arr_size = int(len(phase_array)/period) * period  # counting size of end array
    fr_arr_size = int(len(frequency_array)/period) * period
    # print("Phase array size:{0}\n Freq array size:{1}".format(ph_arr_size, fr_arr_size))
    phase_array = phase_array[:ph_arr_size]  # cut phase array to period module size
    frequency_array = frequency_array[:fr_arr_size]
    # print("Phase array size:{0}\n Freq array size:{1}".format(len(phase_array), len(frequency_array)))
    phase_arr_to_corr = np.array(phase_array, dtype=float).reshape(int(len(phase_array)/period), period)
    freq_arr_to_corr = np.array(frequency_array, dtype=float).reshape(int(len(frequency_array)/period), period)
    # correlation
    ph_corr_arr = correlate(phase_arr_to_corr)
    fr_corr_arr = correlate(freq_arr_to_corr)
    # correlation

    # average
    average = 20
    ph_aver_arr = average_f(ph_corr_arr, period, average)
    fr_aver_arr = average_f(fr_corr_arr,  period, average)

    return ph_corr_arr, fr_corr_arr, ph_aver_arr, fr_aver_arr


def phase(buff_in):
    """Takes array size {X,2} count phase of signal, returns list of phases"""
    buff_ph = []
    # print(buff_in)
    for i in range(len(buff_in)):

        it = buff_in[i][0]  # I quadrature
        qt = buff_in[i][1]  # Q quadrature
        sq = 0
        # PHASE____________
        if it >= 0:
            sq = math.atan2(it, qt)
        elif it < 0:
            sq = math.atan2(it, qt) + math.pi
        buff_ph.append(sq)
        # PHASE_____________
    return buff_ph


def frequency(buff_in):
    """Takes array size of (X,2) return array of counted frequencies"""
    buff_fr = []
    for i in range(len(buff_in)-1):
        i1q0 = buff_in[i + 1, 0] * buff_in[i, 1]  # Array [X,Y] - Y = 1,0 (0-I,1-Q)
        q1i0 = buff_in[i+1, 1] * buff_in[i, 0]
        i1i0 = buff_in[i, 0] * buff_in[i+1, 0]
        q1q0 = buff_in[i, 1] * buff_in[i+1, 1]
        fr = math.atan2(i1q0-q1i0, i1i0+q1q0)
        buff_fr.append(fr)
    return buff_fr


def correlate(in_arr):
    out_arr = []
    for i in range(len(in_arr)-1):
        out_arr.append(in_arr[i, :] - in_arr[i+1, :])
    return out_arr
    
    
def average_f(in_arr, period, average):
    
    averaged_buff = []
    averaged_vector = np.full(period, average)

    try:
        # print("fun-average before cyc \n size of in mass:{0},\n average:{1}".format(len(in_arr), average))
        for i in range(0, len(in_arr)-average, average):
            # print("fun-average i:", i)
            to_append = 0
            for j in range(average):
                to_append += in_arr[i+j]
            to_append /= averaged_vector
            averaged_buff.append(to_append)
    except Exception as e:
        print("Error in ccorf:", e)
    return averaged_buff
