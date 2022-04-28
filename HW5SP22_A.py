import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import math

Re = 0
f = 0.02

def ff(Re, rr, CBEQN=False):
    """
    This function calculates the friction factor for a pipe based on input Re and relative roughness.
    The calculation method is selected using the CBEQN boolean.
    :param Re: the Reynolds number under question.
    :param rr: the relative pipe roughness (expect between 0 and 0.05)
    :param CBEQN:  boolean to indicate if I should use Colebrook (True) or laminar equation
    :return: the (Darcy) friction factor
    """
    if(CBEQN):
        # note:  in numpy log is for natural log.  log10 is log base 10.
        # Colebrook Equation
        ff = lambda f: 1/f**0.5+2.0*np.log10(rr/3.7+2.51/(Re*f**0.5))
        return fsolve(ff, 0.001)
    else:
        return 64/Re


def plotMoody(PlotPoint=False, pt=(0,0)):
    """
    This function produces the Moody diagram for a Re range from 1 to 10^8 and
    for relative roughness from 0 to 0.05 (20 steps).  The laminar region is described
    by the simple relationship of f=64/Re whereas the turbulent region is described by
    the Colebrook equation.
    :return: just shows the plot, nothing returned
    """
    #Step 1:  create logspace arrays for ranges of Re
    ReValsCB=np.logspace(np.log10(4000.0),8,100)  # for use with Colebrook equation
    ReValsL=np.logspace(np.log10(600.0),np.log10(2000.0),20)  # for use with Laminar flow
    ReValsTrans=np.logspace(np.log10(2000.0), np.log10(4000.0), 20)  # for use with Transition range for laminar
    #Step 2:  create array for range of relative roughness
    rrVals=np.array([0,1E-6,5E-6,1E-5,5E-5,1E-4,2E-4,4E-4,6E-4,8E-4,1E-3,2E-3,4E-3,6E-3,8E-8,1.5E-2,2E-2,3E-2,4E-2,5E-2])

    #Step 2:  calculate the friction factor in the laminar range
    ffLam=np.array([ff(Re,0.0) for Re in ReValsL])
    ffTrans=np.array([ff(Re, 0.0) for Re in ReValsTrans])

    #Step 3:  calculate friction factor values for each rr at each Re for turbulent range.
    ffCB = np.array([[ff(Re, rr, CBEQN=True) for Re in ReValsCB] for rr in rrVals])  #  I used nested list comprehensions


    #Step 4:  construct the plot
    plt.loglog(ReValsL, ffLam[:], color="k")  # plot the solid line part for f=64/Re
    plt.loglog(ReValsTrans, ffTrans[:], linestyle='dashed', color="k")  # plot the dashed line part for f=64/Re

    ax = plt.gca()
    # plot the lines from Colebrook for each roughness. Use plt.annotate to put roughness values
    for nRelR in range(len(ffCB)):
        plt.loglog(ReValsCB,ffCB[nRelR],color='k', label=nRelR)
        plt.annotate(xy=(1E8,ffCB[nRelR][-1]),text=rrVals[nRelR])
    #Plot x and y axes, as well as adding labels/text accordingly
    plt.xlim(600,1E8)  # restrict the plot x range
    plt.ylim(0.008, 0.10)  # restrict the plot y range
    plt.xlabel('Reynolds number ' r'$Re = \frac{Vd}{\nu}$', fontsize=16)
    plt.ylabel('Friction factor ' r'$f = \frac{h}{\left(\frac{L}{d}\cdot\frac{V^2}{2g}\right)}$', fontsize=16)
    plt.text(2.5E8,0.02, 'Relative roughness ' r'$\frac{\epsilon}{d}$',rotation=90, fontsize=16)  # for the text at right of graph for relative roughness
    plt.title('Moody Chart', fontsize=16)
    #Specifying the tick marks on the graph

    ax.tick_params(axis="both", which="both", direction="in")  # format tick marks
    ax.tick_params(which='both')  # format grid lines
    ax.tick_params(axis="both", which="both", right="True")  # add minor tick labels to y
    ax.tick_params(which='both', top=True)
    ax.yaxis.set_minor_formatter(FormatStrFormatter("%.3f"))
    plt.grid(which='both')

    # This part is added for part B to work properly in order to plot the points with markers accordingly to trans/lam
    if (PlotPoint):
        plt.plot(pt[0],pt[1],marker='o' if (pt[0]<=2000 or pt[0]>=4000) else '^', markersize=12, mec='r',mfc='none')
        #mec = marker edge color, mfc = marker face color
    plt.show()



def main():

    plotMoody(PlotPoint=False, pt=(0,0))

if __name__ == "__main__":
    main()