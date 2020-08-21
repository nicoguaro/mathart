#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lissajous figures for closed curves

The parameterization used for the curves is the azimuth angle.

@author: Nicolás Guarín-Zapata
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.font_manager as fm

fpath = "../../fonts/tex-gyre-adventor/texgyreadventor-regular.otf"
prop = fm.FontProperties(fname=fpath)


def update(k, u, f1, g1, nx=5, ny=5, dx=0.5, dy=0.5, colors=None,
                f2=None, g2=None, name=False, guides=False, tracer=False):
    """Update the axes for the new frame

    Parameters
    ----------
    k : int
        Position on the parameter array.
    u : ndarray, float
        Azimuth angle, parameter array.
    f1 : callable
        Horizontal component of the base curve.
    g1 : callable
        Vertical component of the base curve.
    nx : int
        Number of plots in the horizontal direction.
    ny : int (optional)
        Number of plots in the vertical direction.
    dx : float (optional)
        Horizontal separation between curves.
    dy : float (optional)
        Vertical separation between curves.
    colors : list (optional)
        List of colors.
    f2 : callable (optional)
        Horizontal component of the curves vertical curves. If not
        defined, f1 are used.
    g2 : callable (optional)
        Horizontal component of the curves vertical curves. If not
        defined, f1 are used.
    name : bool (optional)
        Add a name (nicoguaro) to the plot.
    guide : bool (optional)
        Add guides to the plot.
    trace : bool (optional)
        Add a tracer to the base plots.
    """
    if f2 is None:
        f2 = f1
        g2 = g1
    if colors is None:
        colors = ['#04D9D9', '#F241A3', '#FA851E', '#BFD91A', '#D9D9D9',
                  '#1AA0D9', '#E62F53', '#FEED00']
    ncolors = len(colors)
    plt.cla()
    t = u[:k]
    cont = 0
    for row in range(1, nx + 1):
        for col in range(1, nx + 1):
            if row == 1:
                x = f(col*u) + (2 + dx)*col
                y = g(col*u)
                plt.plot(x, y, lw=1, color=colors[col%ncolors], zorder=4)
                if tracer:
                    plt.plot(x[k - 1], y[k - 1], marker="o", mfc="#D9D9D9",
                             mec="#333333", zorder=5)
                if guides:
                    y2 = g2(ny*u)        
                    plt.vlines(x[k - 1], -(2 + dy)*ny + y2[k - 1], y[k - 1],
                               zorder=3, colors="#D9D9D9", linestyles="dotted",
                               lw=0.5)
            if col == 1:
                x = f2(row*u)
                y = g2(row*u) - (2 + dy)*row

                plt.plot(x, y, lw=1, color=colors[row%ncolors], zorder=4)
                if tracer:
                    plt.plot(x[k - 1], y[k - 1], marker="o", mfc="#D9D9D9",
                             mec="#333333", zorder=5)
                if guides:
                    x2 = f(nx*u)
                    plt.hlines(y[k - 1], x[k - 1], (2 + dx)*nx + x2[k - 1],
                               zorder=3, colors="#D9D9D9", linestyles="dotted",
                               lw=0.5)
            x = f(col*t) + (2 + dx)*col
            y = g2(row*t) - (2 + dy)*row
            plt.plot(x, y, lw=1, color=colors[cont%ncolors], zorder=4)
            cont += 1
    plt.axis("image")
    plt.axis("off")
    ax = plt.gca()
    _, x_max = ax.get_xlim()
    y_min, _ = ax.get_ylim()
    if name:
        plt.text(x_max, y_min - 2*dy, "@nicoguaro", fontsize=20,
                 horizontalalignment='right',
                 fontproperties=prop, alpha=0.7)
    return None


def curve_select(npts, curve, r=2.0, n=3):
    """Select the base curve to use for the Lissajous curves

    Parameters
    ----------
    npts : int
        Number of points for the azimuth angle (parameter).
    u : str
        Kind of curve to use.
    r : float (optional)
        Parameter for the superquadric.
    n : int (optional)
        Number of leeves for the clover.

    Returns
    -------
    u : ndarray, float
        Azimuth angle, parameter array.
    f : callable
        Horizontal component of the base curve.
    g : callable
        Vertical component of the base curve.    
    """
    u = np.linspace(0, 2*np.pi, npts)
    if curve == "flower":
        f = lambda t: np.cos(t)*(1 + 0.2*np.cos(8*t))/1.2
        g = lambda t: np.sin(t)*(1 + 0.2*np.cos(8*t))/1.2
    elif curve == "superquadric":
        m = 2.0/r
        f = lambda t: np.sign(np.cos(t)) * np.abs(np.cos(t))**m
        g = lambda t: np.sign(np.sin(t)) * np.abs(np.sin(t))**m
    elif curve == "square":
        rho = lambda t: np.maximum(np.abs(np.cos(t)), np.abs(np.sin(t)))
        f = lambda t: np.cos(t) / rho(t)
        g = lambda t: np.sin(t) / rho(t) 
    elif curve == "butterfly":
        f = lambda t: 0.5*np.cos(t)*(np.cos(5*t)**2 + np.sin(3*t) + 0.3)
        g = lambda t: 0.5*np.sin(t)*(np.cos(5*t)**2 + np.sin(3*t) + 0.3)
    elif curve == "bicardioid":
        f = lambda t: np.cos(2*t)*np.cos(t)
        g = lambda t: np.sin(2*t)*np.cos(t)
    elif curve == "clover":
        f = lambda t: np.cos(t)*np.sin(n*t)
        g = lambda t: np.sin(t)*np.sin(n*t)
    else:
        f = lambda t: -np.sin(t)**3
        g = lambda t: np.cos(t) - 5/13*np.cos(2*t) - 2/13*np.cos(3*t) \
                      - np.cos(4*t)/13 + 2.5/13
    return u, f, g 



if __name__ == "__main__":
    # Plots setup
    repo = "https://raw.githubusercontent.com/nicoguaro/matplotlib_styles/master"
    style = repo + "/styles/neon.mplstyle"
    plt.style.use(style)
    
    # Parameters
    nx = 5
    ny = 5
    dx = 0.5
    dy = 0.5
    npts = 501
    u, f, g = curve_select(npts, "clover", n=2)
    _, f2, g2 = curve_select(npts, "clover", n=3)
    
    # Animation
    fig = plt.figure(figsize=(8, 8))
    ani = animation.FuncAnimation(fig, update, range(0, npts, 10), repeat=False,
                                  fargs=(u, f, g, nx, ny, dx, dy, None, 
                                         f2, g2, True, True, True))
    ani.save("lissajous.gif", writer='imagemagick', dpi=100)
    plt.show()
