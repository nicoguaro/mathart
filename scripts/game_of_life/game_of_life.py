"""

A cellular automata with rules of the Conways Game
of Life, from http://en.wikipedia.org/wiki/Conway%27s_Game_of_Life.


Rules (From Wikipedia):
-----------------------

The universe of the Game of Life is an infinite two-dimensional
orthogonal grid of square cells, each of which is in one of two possible
states, alive or dead. Every cell interacts with its eight neighbours,
which are the cells that are horizontally, vertically, or diagonally
adjacent. At each step in time, the following transitions occur:

    1. Any live cell with fewer than two live neighbours dies, as if
      caused by under-population.
    2. Any live cell with two or three live neighbours lives on to the
      next generation.
    3. Any live cell with more than three live neighbours dies, as if by
      overcrowding.
    4. Any dead cell with exactly three live neighbours becomes a live
      cell, as if by reproduction.

The initial pattern constitutes the seed of the system. The first
generation is created by applying the above rules simultaneously to
every cell in the seed-births and deaths occur simultaneously, and the
discrete moment at which this happens is sometimes called a tick (in
other words, each generation is a pure function of the preceding one).
The rules continue to be applied repeatedly to create further
generations.

@author: Nicolás Guarín-Zapata
"""
import numpy as np
from numpy.random import randint
from matplotlib import pyplot as plt
import matplotlib.animation as animation


def automata_step(A):
    """
      Step the automata assuming a toroidal topology ("Periodic
      Boundaries").
    """
    alive_neigh = np.roll(A,  1, axis=0).astype(int) \
                + np.roll(A, -1, axis=0).astype(int) \
                + np.roll(A,  1, axis=1).astype(int) \
                + np.roll(A, -1, axis=1).astype(int) \
                + np.roll(A, (1, 1), axis=(0, 1)).astype(int) \
                + np.roll(A, (-1, 1), axis=(0, 1)).astype(int) \
                + np.roll(A, (-1, -1), axis=(0, 1)).astype(int) \
                + np.roll(A, (1, -1), axis=(0, 1)).astype(int)
    A[np.logical_and(alive_neigh < 2, A == 1)] = 0
    A[np.logical_and(alive_neigh > 3, A == 1)] = 0
    A[np.logical_and(alive_neigh == 3, A == 0)] = 1
    A[np.logical_and(np.logical_or(alive_neigh == 2,
                                   alive_neigh == 3),
                     A == 1)] = 1
    return A



def update(step, A, verbose=False):
    """Update the axes for the new frame"""
    if verbose:
        print("Step %d" % step)
    plt.cla()
    A = automata_step(A)
    plt.imshow(A, interpolation='nearest')
    plt.grid()
    plt.axis('off')
    return None

#%%
if __name__ == "__main__":
    plt.rcParams["image.cmap"] = "bone_r"
    
    n = 100  # Size of the grid
    m = 100  # Size of the initial population
    nsteps = 200  # Number of steps
    
    np.random.seed(seed=10)  # To guarantee reproducibility
    A = np.zeros((n, n), dtype=bool)
    A[n//2 - m//2:n//2 + m//2,
      n//2 - m//2:n//2 + m//2] = randint(0, 2, (m,m))
    

    # Animation
    fig = plt.figure(figsize=(5, 5))
    ani = animation.FuncAnimation(fig, update, range(nsteps),repeat=False,
                                  fargs=(A,))
    ani.save("game_of_life.gif", writer='imagemagick', dpi=100)
    plt.show()
