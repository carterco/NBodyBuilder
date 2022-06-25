# NBodyBuilder

Welcome NBodyBuilders!

Instructions for use:

1) pip install NBodyBuilder
3) import NBodyBuilder.NBodyBuilder as nb
4) Ensure that you're running in an environment that can open a pop-up window (WSL via terminal may have issues with this)
5) If you'd like to build your simulation using a GUI, run nb.gui()
4) If you'd like to build your simulation using text prompts, run nb.non_gui()
5) Enjoy the simulation!

Mac specific instructions:

OS-users may experience trouble installing because of '_tkinter':
ModuleNotFoundError: No module named '_tkinter'

To fix this error, try:
> brew install python-tk

Troublshooting:

1) Make sure you set and submit *all* inputs before clicking "Run and Plot" -- otherwise, you may get an error
2) Similarly, you need to adjust the slidebar before clicking "Run and Plot"
