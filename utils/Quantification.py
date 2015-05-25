def quantify(time_series, quant_number):
    quant_time_series = []

    qMin = min(time_series)
    qMax = max(time_series)
    qStep = (qMax - qMin) / float(quant_number-1)

    for ts in time_series:
        quant = int((ts - qMin) / qStep)
        quant_time_series.append(quant * qStep + qMin)
    return quant_time_series


if __name__ == "__main__":
    time_series = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print quantify(time_series, 2)
    print quantify(time_series, 5)
    print quantify(time_series, 10)
