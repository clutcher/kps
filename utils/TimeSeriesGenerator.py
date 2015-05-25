def generate_static(number_of_nodes):
    return [1] * number_of_nodes


def generate_periodic(number_of_nodes):
    time_series = []
    period = [4, 3, 2, 1]
    for i in xrange(number_of_nodes / 4):
        time_series.extend(period)
    if number_of_nodes % 4 != 0:
        time_series.extend(period[:number_of_nodes % 4])
    return time_series


def generate_poisson(number_of_nodes):
    import numpy as np

    p_lambda = 10
    time_series = list(np.random.poisson(p_lambda, number_of_nodes))
    return time_series


def generate_random(number_of_nodes):
    import random

    time_series = []
    for i in xrange(number_of_nodes):
        time_series.append(random.random())
        # time_series.append(random.randint(1, number_of_nodes/10))
    return time_series


def generate_sinusoid(number_of_nodes):
    import numpy as np

    x = np.linspace(-10, 10, number_of_nodes)
    time_series = np.sin(x)
    return list(time_series)