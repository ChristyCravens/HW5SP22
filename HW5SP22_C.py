from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np


def ode_system(X, t, *params):
    """
    The ode system is defined in terms of state variables.
    I have as unknowns:
    x: position of the piston (This is not strictly needed unless I want to know x(t))
    xdot: velocity of the piston
    p1: pressure on right of piston
    p2: pressure on left of the piston
    For initial conditions, we see: x=x0=0, xdot=0, p1=p1_0=p_a, p2=p2_0=p_a
    The asterisk before params just says that there's no defined number of arguments within params.
    :param X: The list of state variables
    :param t: The time for this instance of the function
    :param params: The list of physical constants for the system
    :return: The list of derivatives of the state variables
    """
    #unpack the parameters
    A, V, m, Cd, beta, Ps, rho, Pa, K, y = params

    #calculate derivatives
    #conveniently rename state variables
    x = X[0]
    xdot = X[1]
    P1 = X[2]
    P2 = X[3]

    #use my equations from the assignment
    xddot = (A / m) * (P1 - P2)
    p1dot = (beta / (V * rho)) * (y * K * (Ps - P1) - rho * A * xdot)
    p2dot = (beta / (V * rho)) * (rho * A * xdot - y * K * (P2 - Pa))

    # return the list of derivatives of the state variables
    return [xdot, xddot, p1dot, p2dot]


def main():
    """
    This function uses the outlined parameters given to plot the system on an appropriately labeled graph.
    :return: plots
    """

    # Time for plot #After some trial and error, I found all the action seems to happen in the first 0.02 seconds
    t = np.linspace(0, 0.02, 200)

    # Pack parameters
    myargs= (4.909e-4, 1.473e-4, 30, 0.6, 2e9, 1.4e7, 850, 1e5, 2e-5, 0.002)

    # Initial Conditions
    x0=0
    xdot0=0
    p1_0=1E5
    p2_0=1E5
    I0 = [x0, xdot0, p1_0, p2_0]

    # call odeint with ode_system as callback, initial conditions and extra arguments/parameters
    x = odeint(ode_system, I0, t, args=myargs)


    #plot the result
    plt.plot(t, x[:, 1], 'hotpink')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity of Piston (m/s)')
    plt.title('Mechanical Displacement Speed ($\dot{x}$)')
    plt.show()

    plt.plot(t, x[:, 2], color='turquoise', label="P1")
    plt.plot(t, x[:, 3], '--', color='purple', label="P2")
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (Pa)')
    plt.legend()
    plt.title('P1 and P2 vs Time')
    plt.show()


if __name__=="__main__":
    main()


