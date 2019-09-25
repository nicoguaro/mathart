# -*- coding: utf-8 -*-
"""
Newton fractal for the equation

    x**3 + 1


Currently, it is quite slow since it is using Python loops instead
of vectorization of the operations.

Author: Nicolas Guarin Zapata
"""

import numpy as np
import matplotlib.pyplot as plt


def newt(x, fun, der, tol=1e-5, niter=100):
    """ Find a root using Newton Method"""
    x0 = x
    for k in range(niter):
        x = x0 - fun(x0)/der(x0)   
        err = np.abs((x - x0)/x)
        if err < tol:
            break
        if k == niter - 1:
            x = 1000
        x0 = x
    return x


def img_newt(N, xran=(-3, 3), yran=(-3, 3), tol=1e-5, niter=100):
    """
    Add colors to a matrix according to the fixed point
    of the given equation.
    """
    sol = [-(np.sqrt(3.0)*1j - 1.0)/2.0, 
           (np.sqrt(3.0)*1j + 1.0)/2.0,
          -1.0]
    col_newt = np.zeros((N, N, 3))
    Y, X = np.mgrid[yran[0]:yran[1]:N*1j,
                    xran[0]:xran[1]:N*1j]
    for row in range(N):
        for col in range(N):
            x = X[row, col]
            y = Y[row, col]
            xf = newt(x + y*1j, fun, der, tol=tol, niter=niter)           
            if abs(xf - sol[0])<1e-6:
                col_newt[row, col, :] = colors[0]
            if abs(xf - sol[1])<1e-6:
                col_newt[row, col, :] = colors[1]
            if abs(xf - sol[2])<1e-6:
                col_newt[row, col, :] = colors[2]
            if abs(xf - 1000) < 1e-6:
                col_newt[row, col, :] = colors[3]
    return col_newt


#%% Computation
colors = [[0.0431, 0.4078, 0.6588],
          [0.1176, 0.6431, 0.2314],
          [0.6745, 0.1216, 0.2431],
          [0.2, 0.2, 0.2]]
fun = lambda x: x*x*x + 1.0
der = lambda x: 3.0*x*x
col_newt = img_newt(2000, tol=1e-10, niter=1000)

#%% Visualization
plt.figure(figsize=(4,4))
plt.imshow(col_newt, extent=(-3, 3, -3, 3), origin='lower')
plt.axis('off')
plt.savefig('newton_fractal.png', dpi=500, transparent=True,
            bbox_inches='tight', pad_inches=0)
plt.show()
