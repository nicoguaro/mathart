#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Animate the Euler line for random triangles.

@author: Nicolas Guarin-Zapata
@date: September 2019
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def plot_tri(ang, ax=None):
    if ax is None:
        ax = plt.gca()
    x = np.cos(ang)
    y = np.sin(ang)
    plt.plot(x, y, lw=0, marker="o", zorder=4, mec="#333333", mfc="#D9D9D9")
    x = np.r_[x, x[0]]
    y = np.r_[y, y[0]]
    ax.plot(x, y, zorder=3)
    az = np.linspace(0, 2*np.pi)
    x = np.cos(az)
    y = np.sin(az)
    ax.plot(x, y, color="#D9D9D9", lw=0.5, linestyle="dashed")
    return ax


def plot_pts(ang, ax=None):
    if ax is None:
        ax = plt.gca()
    x = np.cos(ang)
    y = np.sin(ang)
    # Centroid
    cent_x = np.sum(x)/3
    cent_y = np.sum(y)/3
    ax.plot(cent_x, cent_y, marker="o", zorder=5, mec="#333333")

    # Circumcenter
    ax.plot(0, 0, marker="o", zorder=5, mec="#333333")

    # Orthocenter
    side0 = np.sqrt((x[2] - x[1])**2 + (y[2] - y[1])**2)
    side1 = np.sqrt((x[0] - x[2])**2 + (y[0] - y[2])**2)
    side2 = np.sqrt((x[1] - x[0])**2 + (y[1] - y[0])**2)
    ang0 = np.arccos(0.5*(side1**2 + side2**2 - side0**2)/(side1*side2))
    ang1 = np.arccos(0.5*(side0**2 + side2**2 - side1**2)/(side0*side2))
    ang2 = np.arccos(0.5*(side0**2 + side1**2 - side2**2)/(side0*side1))
    ortho_x = (x[0]*np.tan(ang0) + x[1]*np.tan(ang1) + x[2]*np.tan(ang2))\
             / (np.tan(ang0) + np.tan(ang1) + np.tan(ang2))
    ortho_y = (y[0]*np.tan(ang0) + y[1]*np.tan(ang1) + y[2]*np.tan(ang2))\
             / (np.tan(ang0) + np.tan(ang1) + np.tan(ang2))
    ax.plot(ortho_x, ortho_y, marker="o", zorder=5, mec="#333333")
    return ax


def plot_euler_line(ang, ax=None):
    if ax is None:
        ax = plt.gca()
    x = np.cos(ang)
    y = np.sin(ang)
    cent_x = np.sum(x)/3
    cent_y = np.sum(y)/3
    angle_euler = np.arctan2(cent_y, cent_x)
    ax.plot([-1.2*np.cos(angle_euler), 1.2*np.cos(angle_euler)],
             [-1.2*np.sin(angle_euler), 1.2*np.sin(angle_euler)], zorder=4)
    return ax


def update(cont):
    """Update the axes for the new frame"""
    plt.cla()

    t = np.linspace(0, 2*np.pi)[cont]
    ang0 = -0.5 + np.pi*np.sin(2*t)/18
    ang1 = 1.5 + np.pi*np.sin(3*t)/18
    ang2 = 4 + np.pi*np.sin(5*t)/18
    ang = np.array([ang0, ang1, ang2])
    plot_tri(ang)
    plot_pts(ang)
    plot_euler_line(ang)
    plt.axis("image")
    plt.axis("off")
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.suptitle("Euler line", fontsize=18)
    plt.text(1.2, -1.2, "@nicoguaro", fontsize=14,
                 horizontalalignment='right',
                 fontname="Century Gothic", alpha=0.7)
    return None


if __name__ == "__main__":
    repo = "https://raw.githubusercontent.com/nicoguaro/matplotlib_styles/master"
    style = repo + "/styles/neon.mplstyle"
    plt.style.use(style)

    # Animation
    fig = plt.figure(figsize=(4, 4))
    ani = animation.FuncAnimation(fig, update, range(0, 50), repeat=False)
    ani.save("euler_line.gif", writer='imagemagick', dpi=300)
    plt.show()
