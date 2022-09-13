from collections import defaultdict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path as op
import sys
import seaborn as sns
from collections import defaultdict
from circular.utils import freq_time, date2rad
from circular.stats import periodic_mean_std, von_mises_distribution, kuiper_two
from circular.plots import base_periodic_fig, clock_vonmises_distribution
from circular.circular import kernel, bwEstimation
import time

sys.path.append(op.dirname(op.dirname(op.dirname(op.abspath(__file__)))))

current_palette = sns.color_palette()

def get_p_value_user(n, timestamps, time_segments, plot): 

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8,8), subplot_kw=dict(polar=True))
    ax_ = {'hour': ax1, 'dayweek': ax2, 'daymonth': ax3}
    fig_adjustment = {'hour': 2*np.pi/30, 'dayweek': -2*np.pi/8, 'daymonth': -2*np.pi/35}
    str_ = 'Results periodic time analyzers \n'
    str_ += 'Number trx = ' + str(len(timestamps)) + '\n'
    return_dict = defaultdict(list)

    for time_segment in time_segments:
        freq_arr, times = freq_time(timestamps, time_segment=time_segment)
        fig, ax1 = base_periodic_fig(freq_arr[:, 0], 
                                    freq_arr[:, 1], 
                                    time_segment=time_segment,
                                    fig=fig, 
                                    ax1=ax_[time_segment]) 

        radians = date2rad(times, time_segment=time_segment)

        # Estimate kernel
        bw = bwEstimation(radians)
        print(bw, time_segment)
        y = kernel(radians, bw=bw, n=n)
        y = y / y.max()
        p, (z, d_cdf, k_cdf, D1_, D2_, D1, D2) = kuiper_two(radians, y, return_all=True)

        # Plot kernel
        ax1.plot(z + fig_adjustment[time_segment], y, color=current_palette[1], ls='-', linewidth=2)
        ax1.fill_between(z + fig_adjustment[time_segment], 0, y, alpha=0.5, color=current_palette[1])
        str_ += 'Risk pvalue ' + time_segment + ' = ' + str(p) + '\n'
        return_dict[time_segment] = [n, len(timestamps), bw, p]

    print(str_)

    if plot:
        # Print results
        ax4.fill_between(np.linspace(-np.pi, np.pi, 240), 0, 1, color="white")
        ax4.set_xticklabels([])
        ax4.set_yticklabels([])

        ax4.text(np.pi*5/4, 1, str_, style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})

        plt.show()
        plt.close()
    else: 
        pass

    return return_dict

def get_p_value_user_no_plot(n, timestamps, time_segments): 

    str_ = 'Results periodic time analyzers \n'
    str_ += 'Number trx = ' + str(len(timestamps)) + '\n'
    return_dict = defaultdict(list)

    for time_segment in time_segments:
        start = time.time()
        freq_arr, times = freq_time(timestamps, time_segment=time_segment)

        radians = date2rad(times, time_segment=time_segment)

        # Estimate kernel
        bw = bwEstimation(radians)
        y = kernel(radians, bw=bw, n=n)
        y = y / y.max()
        p, (z, d_cdf, k_cdf, D1_, D2_, D1, D2) = kuiper_two(radians, y, return_all=True)

        # Plot kernel
        str_ += 'Risk pvalue ' + time_segment + ' = ' + str(p) + '\n'

        end = time.time()
        secs = end - start
        return_dict[time_segment] = [n, len(timestamps), bw, p, secs]

    return return_dict


# def plot_several_timestamps(n, timestamps, time_segments, plot, colors, legends): ## plot several timestamps with respective label

#     fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16,16), subplot_kw=dict(polar=True))
#     ax_ = {'hour': ax1, 'dayweek': ax2, 'daymonth': ax3}
#     fig_adjustment = {'hour': 2*np.pi/30, 'dayweek': -2*np.pi/8, 'daymonth': -2*np.pi/35}
#     str_ = 'Results periodic time analyzers \n'
#     str_ += '\n'

#     for i, timestamp in enumerate(timestamps):
#         str_ += f'Number trx {legends[i]} = ' + str(len(timestamp)) + '\n'
#         for time_segment in time_segments:
#             freq_arr, times = freq_time(timestamp, time_segment=time_segment)
#             fig, ax1 = base_periodic_fig(freq_arr[:, 0], 
#                                         freq_arr[:, 1], 
#                                         color=colors[i], 
#                                         time_segment=time_segment,
#                                         fig=fig, 
#                                         ax1=ax_[time_segment]) 

#             radians = date2rad(times, time_segment=time_segment)

#             # Estimate kernel
#             bw = bwEstimation(radians)
#             print(bw, time_segment)
#             y = kernel(radians, bw=bw, n=n)
#             y = y / y.max()
#             p, (z, d_cdf, k_cdf, D1_, D2_, D1, D2) = kuiper_two(radians, y, return_all=True)

#             # Plot kernel
#             #ax1.plot(z + fig_adjustment[time_segment], y, color=current_palette[1], ls='-', linewidth=2)
#             ax1.plot(z + fig_adjustment[time_segment], y,ls='-', linewidth=2, color=colors[i], label=legends[i])
#             #ax1.fill_between(z + fig_adjustment[time_segment], 0, y, alpha=0.5, color=current_palette[1])
#             ax1.fill_between(z + fig_adjustment[time_segment], 0, y, alpha=0.5, color=colors[i])
#             str_ += 'Risk pvalue ' + time_segment + ' = ' + str(p) + '\n'

#         print(str_)
#         str_ += '\n'
    
#     if plot:
#         # Print results
#         ax4.fill_between(np.linspace(-np.pi, np.pi, 240), 0, 1, color="white")
#         ax4.set_xticklabels([])
#         ax4.set_yticklabels([])

#         ax4.text(np.pi*5/4, 1, str_, style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
#         ax1.legend(bbox_to_anchor=(1.1, 1.05))
#         plt.show()
#         plt.close()
#     else: 
#         pass