import numpy as np
import pandas as pd


def date2rad(dates, time_segment='hour'):
    """Convert hours to radians

    Parameters
    ----------
    dates : array-like of shape = [n_samples] of hours.
        Where the decimal point represent minutes / 60 + seconds / 60 / 100 ...
        0 <= times[:] <= 24

    time_segment: string of values ['hour', 'dayweek', 'daymonth']

    Returns
    -------
    radians : array-like of shape = [n_samples]
        Calculated radians

    Examples
    --------
    >>> import numpy as np
    >>> from pycircular.utils import date2rad
    >>> times = np.array([4, 6, 7])
    >>> for time_segment in ['hour', 'dayweek', 'daymonth']:
    >>>     print(time_segment, date2rad(times, time_segment))

    """

    if time_segment == 'hour':

        radians = dates * 2 * np.pi / 24

        # Fix to rotate the clock and move PI / 2
        # https://en.wikipedia.org/wiki/Clock_angle_problem

        radians = - radians + np.pi/2

    elif time_segment == 'dayweek':

        # Day of week goes counter-clockwise
        radians = dates * 2 * np.pi / 7 + np.pi/2

    elif time_segment == 'daymonth':

        # Day of month goes counter-clockwise
        radians = dates * 2 * np.pi / 31 + np.pi/2
        # TODO: check what to do with last day of month

    # Change to be in [0, 2*pi]
    radians1 = []
    for i in radians:
        if(i<0):
            radians1.append(i+2*np.pi)
        
        elif(i>(2*np.pi)):
            radians1.append(i-2*np.pi)
        
        else:
            radians1.append(i) 
        

    return radians1


def _date2rad(dates, time_segment='hour'):
    """Convert time_segment to radians

    From pycircular.utils.date2rad and pycircular.utils.freq_time

    Parameters
    ----------
    dates : pandas DatetimeIndex array-like of shape = [n_samples] of dates.

    time_segment: string of values ['hour', 'dayweek', 'daymonth']

    Returns
    -------
    radians : array-like of shape = [n_samples]
        Calculated radians

    """

    # calculate times
    times = dates.dt.hour + dates.dt.minute / 60 + dates.dt.second / 60 / 60
    # Change from 100 to 60, consistency for radians

    if time_segment == 'hour':

        radians = times * 2 * np.pi / 24

        # Fix to rotate the clock and move PI / 2
        # https://en.wikipedia.org/wiki/Clock_angle_problem

        radians = - radians + np.pi/2

    elif time_segment == 'dayweek':

        time_temp = dates.dt.dayofweek  # Monday=0, Sunday=6
        times = time_temp + times / 24

        # Day of week goes counter-clockwise
        radians = times * 2 * np.pi / 7 + np.pi/2

    elif time_segment == 'daymonth':

        time_temp = dates.dt.day
        times = time_temp + times / 24

        # Day of month goes counter-clockwise
        radians = times * 2 * np.pi / 31 + np.pi/2
        # TODO: check what to do with last day of month

    # Change to be in range [0, 2*pi]
    if hasattr(radians, 'shape'):
        # Check if an array
        radians.loc[radians < 0] += 2 * np.pi
        radians.loc[radians > 2 * np.pi] -= 2 * np.pi
    else:
        # If it is a scalar
        if radians < 0:
            radians += 2 * np.pi
        elif radians > 2 * np.pi:
            radians -= 2 * np.pi

    return radians


def freq_time(dates, time_segment='hour', freq=True, continious=True):
    """Calculate frequency per time period and calculate continius time period

    Parameters
    ----------
    dates : array-like of shape = [n_samples] of dates in format 'datetime64[ns]'.

    time_segment: string of values ['hour', 'dayweek', 'daymonth']

    freq : Whether to return the frequencies


    Returns
    -------
    freq_arr : array-like of shape = [unique_time_segment, 2]
        where: freq_arr[:, 0] = unique_time_segment
               freq_arr[:, 1] = frequency in percentage

    times : array-like of shape = [n_samples]
        Where the decimal point represent minutes / hours depending on time_segment

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from pycircular.utils import freq_time
    >>> dates = pd.to_datetime(["2013-10-02 19:10:00", "2013-10-21 19:00:00", "2013-10-24 3:00:00"])
    >>> for time_segment in ['hour', 'dayweek', 'daymonth']:
    >>>     print(time_segment)
    >>>     freq_arr, times = freq_time(dates, time_segment=time_segment)
    >>>     print(freq_arr)
    >>>     print(times)

    """

    # Get frequency per time_segment
    dates_index = pd.DatetimeIndex(dates)

    # calculate times
    times = dates_index.hour + dates_index.minute / 60 + dates_index.second / 60 / 100

    if time_segment == 'hour':

        time_temp = dates_index.hour

    elif time_segment == 'dayweek':

        time_temp = dates_index.dayofweek  # Monday=0, Sunday=6
        times = time_temp + times / 24

    elif time_segment == 'daymonth':

        time_temp = dates_index.day
        times = time_temp + times / 24

    freq_arr = None

    if freq:
        freq_ = pd.Series(time_temp).value_counts()
        freq_ = freq_ / freq_.sum()

        freq_arr = np.zeros((freq_.shape[0], 2))  # Hour, freq
        freq_arr[:, 0] = freq_.index
        freq_arr[:, 1] = freq_.values

    if continious:
        return freq_arr, times
    else:
        return freq_arr, time_temp
