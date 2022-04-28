from HW5SP22_A import ff, plotMoody
import random as rnd
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def ffPoint(Re, rr):
    """
    This function takes Re and rr as parameters and outputs a friction factor according to the following:
    1.  if Re>4000 use Colebrook Equation
    2.  if Re<2000 use f=64/Re
    3.  else calculate a probabilistic friction factor where the distribution has a mean midway between the prediction
        of the f=64/Re and Colebrook Equations and a standard deviation of 20% of this mean
    :param Re:  the Reynolds number
    :param rr:  the relative roughness
    :return:  the friction factor
    """
    #Set up initial values
    Initial = np.ones(1) * 0.004
    #if else to determine if the flow is transition or otherwise
    if Re >= 4000:
        return ff(Re,rr,CBEQN=True)

    if Re <= 2000:
        return ff(Re,rr)
    CBff=ff(Re,rr,CBEQN=True)
    Lamff=ff(Re,rr)
    mean=(CBff+Lamff)/2
    sig=0.2*mean
    return rnd.normalvariate(mean, sig)

def PlotPoint(Re, f):
    """
    This function allows for us to automatically input a point on the plot that will locate and immediately tell
    us if the flow is transition or otherwise, where a red upward triangle signifies transitional flow and a red
    circle signifies all else.
    :param Re: Reynolds number
    :param f: friction factor
    :return: appropriate point on the Moody Chart, based on flow
    """
    #Use plotMoody from part A to solve for the points
    plotMoody(PlotPoint=True, pt=(Re, f))



def main():
    #Have user input the Reynolds number and relative roughness for evaluation
    Re = float(input("Enter Reynolds number: "))
    rr = float(input("Enter relative roughness value: "))
    f = ffPoint(Re, rr)
    #Call PlotPoint to plot the point based on these values and change the marker accordingly
    PlotPoint(Re, f)

    plt.show()

if __name__ == "__main__":
    main()