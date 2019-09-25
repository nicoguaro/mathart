==============
Newton fractal
==============

Compute, the `Newton fractal <https://en.wikipedia.org/wiki/Newton_fractal>`__
for the equation :math:`f(z) = z^2 + 1 `.

.. image:: newton_fractal.png
  :width: 400 px
  :alt: Newton fractal.
  :align:  center

This fractal is produced due the unstability of the Newton iteration

.. math::

  z_\text{new} = z_\text{old} - \frac{f(z_\text{old})}{f'(z_\text{old})}\, ,

for different selected initial conditions.


License
-------

Licensed under `MIT license <https://opensource.org/licenses/MIT>`__
