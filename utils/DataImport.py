def import_from_file(file_name):
    time_series = open(file_name).readlines()
    try:
        time_series.remove('')
    except:
        pass
    time_series = map(str.strip, time_series)
    time_series = [float(i) for i in time_series]
    return time_series
