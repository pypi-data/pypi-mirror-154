"""
Created on May 24 22:12:45 2022
"""

import tkinter as tk
from typing import Any, Union

# added try/except because pip bundle and main file do not work with same imports

try:
    from . import tk_functions as tk_f
    from .utilities import convert
except ImportError:
    import tk_functions as tk_f
    from utilities import convert


class GetParameterSelection:

    def __init__(self, window, title, object_class):
        self.par_window = tk.Toplevel(window)

        _w, _h = window.winfo_width(), window.winfo_height()

        self.par_window.geometry(newGeometry=f'{_w}x{_h}')
        self.par_window.title(string=title)

        self.button_frame = tk.Frame(master=self.par_window, padx=10, pady=10)
        self.button_frame.pack(side=tk.TOP)

        self.parameter_frame = tk.Frame(master=self.par_window, padx=10, pady=10)

        self.parameter_frame.pack(side=tk.BOTTOM, expand=True)

        self.phy = tk.Button(master=self.button_frame, text='Physical Parameters',
                             command=lambda: show_physical_parameters(
                                     window=self.parameter_frame,
                                     object_class=object_class))
        self.phy.grid(row=0, column=0, sticky='news')

        if title is not 'Sun':
            self.orb = tk.Button(master=self.button_frame, text='Orbital Parameters',
                                 command=lambda: show_orbital_parameters(
                                         window=self.parameter_frame, object_name=title,
                                         object_class=object_class))
            self.orb.grid(row=0, column=1, sticky='news')


def show_physical_parameters(window: Union[tk.Tk, tk.Toplevel, tk.Frame],
                             object_class: Any):
    """
    Display the physical parameters of the celestial object.

    Parameters
    ----------
    window : Union[tk.Tk, tk.Toplevel, tk.Frame]
        tk.Tk or tk.Toplevel window or a tk.Frame to build the object inside.
    object_class : Any
        The object clas from which the attributes are to be read.

    Returns
    -------
    None.

    """

    _children = window.winfo_children()

    for child in _children:
        child.destroy()

    object_class = object_class.PhysicalParameters()

    planet_window = window

    # adjust the columns in window's width
    [planet_window.grid_columnconfigure(index=i, weight=1) for i in range(5)]

    # heading labels
    tk_f.label_placement(window=planet_window, text="Physical parameters", row=0,
                         column=0, pad_y=5, sticky="e")
    tk_f.label_placement(window=planet_window, text="Values", row=0, column=1, pad_y=5)
    tk_f.label_placement(window=planet_window, text="Unit space", row=0, column=2,
                         pad_y=5)
    tk_f.label_placement(window=planet_window, text="Reset", row=0, column=3, pad_y=5)

    # placing the equivalency button
    tk_f.object_button(window=planet_window, text="Equivalences",
                       function=lambda: tk_f.place_equivalencies(window=planet_window,
                                                                 cel_object=object_class,
                                                                 column=4,
                                                                 equiv_type='physical'),
                       row=0, column=4, width=25, sticky="nsew")

    # placing the details of celestial objects one by one
    tk_f.place_object_properties(window=planet_window, text="Age",
                                 value=object_class.age,
                                 function=convert, options=("s", "yr", "Myr", "Gyr"),
                                 row=1, column=0, default="Gyr")

    tk_f.place_object_properties(window=planet_window, text="Mass",
                                 value=object_class.mass, function=convert,
                                 options=("g", "kg", "M_earth", "M_jupiter", "M_sun"),
                                 row=2, column=0, default="kg")

    tk_f.place_object_properties(window=planet_window, text="Radius",
                                 value=object_class.radius, function=convert,
                                 options=("cm", "m", "km", "R_earth", "R_jupiter",
                                          "R_sun"), row=3, column=0, default="km")

    tk_f.place_object_properties(window=planet_window, text="Volume",
                                 value=object_class.volume, function=convert,
                                 options=("cm^3", "m^3", "km^3"), row=4, column=0,
                                 default="km^3")

    tk_f.place_object_properties(window=planet_window, text="Density",
                                 value=object_class.density, function=convert,
                                 options=("g/cm^3", "kg/cm^3", "kg/m^3"), row=5,
                                 column=0, default="g/cm^3")

    tk_f.place_object_properties(window=planet_window, text="Surface area",
                                 value=object_class.surface_area, function=convert,
                                 options=("cm^2", "m^2", "km^2"), row=6, column=0,
                                 default="km^2")

    tk_f.place_object_properties(window=planet_window, text="Surface gravity",
                                 value=object_class.surface_gravity, function=convert,
                                 options=("cm/s^2", "m/s^2", "km/s^2"), row=7, column=0,
                                 default="m/s^2")

    tk_f.place_object_properties(window=planet_window, text='Escape velocity',
                                 value=object_class.escape_velocity, function=convert,
                                 options=('cm/s', 'm/s', 'km/s', 'km/h'), row=8,
                                 column=0, default='km/s')


def show_orbital_parameters(window: Union[tk.Tk, tk.Toplevel, tk.Frame], object_name: str,
                            object_class: Any):
    """
    Display the orbital parameters of the celestial object.
    Parameters
    ----------
    window : Union[tk.Tk, tk.Toplevel, tk.Frame]
        tk.Tk or tk.Toplevel window or a tk.Frame to build the object inside.
    object_name: str
        The name of the object in consideration.
    object_class : Any
        The object clas from which the attributes are to be read.

    Returns
    -------
    None.

    """

    # destroy the previous contents of the frame
    _children = window.winfo_children()

    for child in _children:
        child.destroy()

    # initialize the new data
    object_class = object_class.OrbitalParameters()

    # assign the frame to a new variable
    planet_window = window

    # adjust the columns in frame's width
    [planet_window.grid_columnconfigure(index=i, weight=1) for i in range(5)]

    # heading labels
    tk_f.label_placement(window=planet_window, text="Orbital parameters", row=0,
                         column=0, pad_y=5, sticky="e")

    planet_moon = {'Moon': 'Earth'}

    if object_name in planet_moon.keys():
        tk_f.label_placement(window=planet_window,
                             text='The orbital parameters are given with respect to '
                                  f'the planet {planet_moon[object_name]}.',
                             row=20, column=0, pad_y=10, sticky='news', columnspan=10)

    tk_f.label_placement(window=planet_window, text="Values", row=0, column=1, pad_y=5)
    tk_f.label_placement(window=planet_window, text="Unit space", row=0, column=2,
                         pad_y=5)
    tk_f.label_placement(window=planet_window, text="Reset", row=0, column=3, pad_y=5)

    # placing the equivalency button
    tk_f.object_button(window=planet_window, text="Equivalences",
                       function=lambda: tk_f.place_equivalencies(window=planet_window,
                                                                 cel_object=object_class,
                                                                 column=4,
                                                                 equiv_type='orbital'),
                       row=0, column=4, width=25, sticky="nsew")

    # placing the details of celestial objects one by one
    tk_f.place_object_properties(window=planet_window, text='Semi Major Axis',
                                 value=object_class.semi_major_axis,
                                 function=convert, options=('cm', 'm', 'km', 'Mm', 'Gm',
                                                            'AU'),
                                 row=1, default='AU', column=0)

    tk_f.place_object_properties(window=planet_window, text='Eccentricity',
                                 value=object_class.eccentricity,
                                 function=convert, options=('', ''),
                                 row=2, default='', column=0)

    tk_f.place_object_properties(window=planet_window, text='Closest approach',
                                 value=object_class.apo, function=convert,
                                 options=('cm', 'm', 'km', 'Mm', 'Gm', 'AU'), row=3,
                                 default='AU', column=0)

    tk_f.place_object_properties(window=planet_window, text='Farthest approach',
                                 value=object_class.peri, function=convert,
                                 options=('cm', 'm', 'km', 'Mm', 'Gm', 'AU'), row=4,
                                 default='AU', column=0)

    tk_f.place_object_properties(window=planet_window, text='Orbital Period',
                                 value=object_class.orbital_period,
                                 function=convert, options=('s', 'hr', 'day', 'yr',
                                                            'Myr'),
                                 row=5, default='day', column=0)

    tk_f.place_object_properties(window=planet_window, text='Av. Orbital Speed',
                                 value=object_class.av_orbital_speed,
                                 function=convert,
                                 options=('cm/s', 'm/s', 'km/s', 'km/h'), row=6,
                                 default='km/s', column=0)

    tk_f.place_object_properties(window=planet_window, text='Mean anomaly',
                                 value=object_class.mean_anomaly, function=convert,
                                 options=('deg', 'rad'), row=7, default='deg', column=0)

    tk_f.place_object_properties(window=planet_window, text='Inclination',
                                 value=object_class.inclination, function=convert,
                                 options=('deg', 'rad'), row=8, default='deg', column=0)

    tk_f.place_object_properties(window=planet_window, text='Longitude of Asc. node',
                                 value=object_class.longitude_of_ascending_node,
                                 function=convert, options=('deg', 'rad'), row=9,
                                 default='deg', column=0)

    tk_f.place_object_properties(window=planet_window, text='Argument of peri.',
                                 value=object_class.argument_of_perihelion,
                                 function=convert, options=('deg', 'rad'), row=10,
                                 default='deg', column=0)

    tk_f.place_object_properties(window=planet_window, text='Axial Tilt',
                                 value=object_class.axial_tilt, function=convert,
                                 options=('deg', 'rad'), row=11, default='deg', column=0)
