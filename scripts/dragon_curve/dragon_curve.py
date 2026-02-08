# -*- coding: utf-8 -*-
"""
Generate a dragon curve

@author: Nicolás Guarín-Zapata

"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from PIL import Image


fpath = "../../fonts/tex-gyre-adventor/texgyreadventor-regular.otf"
prop = fm.FontProperties(fname=fpath)


def save_gif_PIL(outfile, files, fps=5, loop=0):
    """Helper function for saving GIFs
    
    Parameters
    ----------
    outfile : string
        Path to the output file.
    files : list
        List of paths with the PNG files.
    fps : int (optional)
        Frames per second.
    loop : int
        The number of times the GIF should loop.
        0 means that it will loop forever.
    """
    imgs = [Image.open(file) for file in files]
    imgs[0].save(fp=outfile, format='GIF', append_images=imgs[1:],
                 save_all=True, duration=int(1000/fps), loop=loop)


repo = "https://raw.githubusercontent.com/nicoguaro/matplotlib_styles/master"
style = repo + "/styles/neon.mplstyle"
plt.style.use(style)


col1 = "#04D9D9"
col2 = "#F241A3"

np.random.seed(3)

A = 0.5*np.array([
[1, -1],
[1, 1]])

plt.figure(figsize=(6,6))
x0 = np.random.normal(0, 1, 2)
niter = 15000
files = []
for cont in range(niter):
    x1 = A @ x0
    x2 = A @ x0 + np.array([1, 0])
    plt.plot(*x1.T, ".", alpha=0.4, color=col1, mec=None, mfc=col1, markersize=2)
    plt.plot(*x2.T, ".", alpha=0.4, color=col2, mec=None, mfc=col2, markersize=2)
    pick = np.random.randint(0, 2)
    if pick:
        x0 = x1.copy()
    else:
        x0 = x2.copy()
    
    if cont % 500 == 0:
        file = f"dragon_curve{str(cont).zfill(5)}.png"
        plt.axis("image")
        plt.xlim(-0.75, 1.75)
        plt.ylim(-0.5, 1.5)
        plt.axis("off")
        plt.text(1.75, -0.9, "@nicoguaro", fontsize=14,
                     horizontalalignment='right',
                     fontproperties=prop)
        plt.savefig(file, dpi=300)
        files.append(file)




# plt.show()

save_gif_PIL("dragon_curve.gif", files, fps=5, loop=0)

[os.remove(file) for file in files]