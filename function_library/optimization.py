"""Optimization example functions from the portfolio optimization lecture."""

import numpy as np


def quadratic_objective(x):
    """
    Source: lecture09/lecture09.ipynb.

    Original function: myfunction.
    Simple quadratic objective used in minimization examples.
    """
    return 3.2 + 5 * x ** 2


def brent_objective(x, a=3.4, b=2, c=0.8):
    """
    Source: lecture09/lecture09.ipynb.

    Original function: f.
    Objective used with scipy.optimize.brent.
    """
    return a - b * np.exp(-((x - c) ** 2))


def squared_distance_objective(x):
    """
    Source: lecture09/lecture09.ipynb.

    Original lambda: lambda x: (x[0] - 10) ** 2 + (x[1] - 25) ** 2.
    """
    return (x[0] - 10) ** 2 + (x[1] - 25) ** 2


def cubic_lambda_example(x):
    """
    Source: lecture09/lecture09.ipynb.

    Original lambda: lambda x: (x[0] + 1) + (x[1] + 2) ** 2 + (x[2] + 3) ** 3.
    """
    return (x[0] + 1) + (x[1] + 2) ** 2 + (x[2] + 3) ** 3


def constrained_objective(x):
    """
    Source: lecture09/lecture09.ipynb.

    Original lambda: lambda x: (x[0] - 1) ** 2 + (x[1] - 2.5) ** 2.
    """
    return (x[0] - 1) ** 2 + (x[1] - 2.5) ** 2


def constraint_one(x):
    """
    Source: lecture09/lecture09.ipynb.

    Original lambda: lambda x: x[0] - 2 * x[1] + 2.
    """
    return x[0] - 2 * x[1] + 2


def constraint_two(x):
    """
    Source: lecture09/lecture09.ipynb.

    Original lambda: lambda x: -x[0] - 2 * x[1] + 6.
    """
    return -x[0] - 2 * x[1] + 6


def constraint_three(x):
    """
    Source: lecture09/lecture09.ipynb.

    Original lambda: lambda x: x[0] + 2 * x[1] + 2.
    """
    return x[0] + 2 * x[1] + 2
