import numpy
import numpy as np
from numpy.linalg.linalg import cholesky
import matplotlib.pyplot as plt


def plot_simulated_paths(simulated_path: np.array, number_of_simulations: int):
    for simulation_index in range(number_of_simulations):
        plt.plot(simulated_path[simulation_index])
    plt.show()


def generate_standard_brownian_motion(number_of_simulations: int, number_of_timesteps: int, dt: float):
    """ Construct standard brownian motion with constant dt  """
    # W(t) ~ N(0, t) -> (W(t) - 0)/sqrt(t) = z -> W(t) = sqrt(t) * z
    # I(s,t) = W(t) - W(s) ~ N(0, t-s) -> (I(s,t) - 0)/sqrt(t-s) = z -> I(s,t) = sqrt(t-s) * z

    Z = np.random.normal(0, 1, size=(number_of_simulations, number_of_timesteps))
    I = np.sqrt(dt) * Z
    W = np.cumsum(I, axis=1)
    return W


def generate_standard_correlated_brownian_motion(number_of_simulations: int, number_of_timesteps: int, dt: float, correlation_matrix: np.array):
    """ Construct standard brownian motion with constant dt  """
    # W(t) ~ N(0, t) -> (W(t) - 0)/sqrt(t) = z -> W(t) = sqrt(t) * z
    # I(s,t) = W(t) - W(s) ~ N(0, t-s) -> (I(s,t) - 0)/sqrt(t-s) = z -> I(s,t) = sqrt(t-s) * z

    L = cholesky(correlation_matrix)
    Z = np.random.normal(0, 1, size=(number_of_simulations, number_of_timesteps))
    I = np.dot(L, np.sqrt(dt) * Z)
    W = np.cumsum(I, axis=1)
    return W


def generate_standard_brownian_bridge_autogenerated():
    """ Construct standard brownian bridge with constant dt  """

    dt = 1/12
    Z = np.random.normal(0, 1, size=(1, 2))
    I = np.sqrt(dt) * Z
    W = np.cumsum(I, axis=1)

    dt_ = 1/252
    Z_ = np.random.normal(0, 1, size=(1, 20))
    I_ = np.sqrt(dt_) * Z_
    W_ = np.zeros(shape=(1, 22))
    W_[0, 0] = x_0 = W[0, 0]
    W_[0, 21] = x_1 = W[0, 1]

    a = 0
    b = dt
    for i in range(1, 21):
        s = i * dt_
        W_[0, i] = ((b-s)/(b-a)) * x_0 + ((s-a)/(b-a)) * x_1 + np.sqrt( (b-s) * (s-a)/ (b-a)) * I_[0, i-1]

    return x_0, x_1, W_


def generate_standard_brownian_bridge(x_0: float, x_1: float):
    """ Construct standard brownian bridge with constant dt  """

    dt_ = 1/252
    Z_ = np.random.normal(0, 1, size=(1, 20))
    I_ = np.sqrt(dt_) * Z_
    W_ = np.zeros(shape=(1, 22))
    W_[0, 0] = x_0
    W_[0, 21] = x_1

    a = 0
    b = 1/12
    for i in range(1, 21):
        s = i * dt_
        W_[0, i] = ((b-s)/(b-a)) * x_0 + ((s-a)/(b-a)) * x_1 + np.sqrt( (b-s) * (s-a)/ (b-a)) * I_[0, i-1]

    return W_


def generate_bivariate_standard_brownian_bridge(x_0: float, x_1: float, y_0: float, y_1: float, correlation_matrix: np.array):
    """ Construct bivariate standard brownian bridge with constant dt  """

    L = cholesky(correlation_matrix)

    dt_ = 1/252
    Z_ = np.random.normal(0, 1, size=(2, 20))
    I_ = np.dot(L, np.sqrt(dt_) * Z_)
    W_ = np.zeros(shape=(2, 22))
    W_[0, 0] = x_0
    W_[0, 21] = x_1
    W_[1, 0] = y_0
    W_[1, 21] = y_1

    a = 0
    b = 1/12
    for i in range(1, 21):
        s = i * dt_
        W_[0, i] = ((b - s) / (b - a)) * x_0 + ((s - a) / (b - a)) * x_1 + np.sqrt((b - s) * (s - a)/ (b - a)) * I_[0, i - 1]
        W_[1, i] = ((b - s) / (b - a)) * y_0 + ((s - a) / (b - a)) * y_1 + np.sqrt((b - s) * (s - a) / (b - a)) * I_[1, i - 1]

    return W_



if __name__ == "__main__":
    # number_of_simulations = 2
    # number_of_timesteps = 1000
    # dt = 1/252
    # W = generate_standard_brownian_motion(number_of_simulations, number_of_timesteps, dt)
    # plot_simulated_paths(W, number_of_simulations)

    # number_of_simulations = 2
    # number_of_timesteps = 1000
    # dt = 1 / 252
    # correlation_matrix = np.array([[1.0, 0.5], [0.5, 1.0]])
    # W = generate_standard_correlated_brownian_motion(number_of_simulations, number_of_timesteps, dt, correlation_matrix)
    # plot_simulated_paths(W, number_of_simulations)

    # number_of_simulations = 1
    # x_0, x_1, W = generate_standard_brownian_bridge_autogenerated()
    # print(f"W[0] = {x_0}, W[1] = {x_1}")
    # plot_simulated_paths(W, number_of_simulations)

    # number_of_simulations = 1
    # x_0 = 1
    # x_1 = 2
    # W = generate_standard_brownian_bridge(x_0, x_1)
    # print(f"W[0] = {x_0}, W[1] = {x_1}")
    # plot_simulated_paths(W, number_of_simulations)

    number_of_simulations = 2
    correlation_matrix = np.array([[1.0, 0.9], [0.9, 1.0]])
    x_0 = 1
    x_1 = 2
    y_0 = 3
    y_1 = 1
    W = generate_bivariate_standard_brownian_bridge(x_0, x_1, y_0, y_1, correlation_matrix)
    print(f"W[0,0] = {x_0}, W[0,1] = {x_1}")
    print(f"W[1,0] = {y_0}, W[1,1] = {y_1}")
    plot_simulated_paths(W, number_of_simulations)

    print("@")
