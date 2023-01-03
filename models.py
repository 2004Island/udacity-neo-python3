"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    # TODO: How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # TODO: Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        
        self.designation = info['designation']
        self.hazardous = info['hazardous']

        # edge cases 

        if 'name' in info:
            self.name = info['name']
        else:
            self.name = None
        
        if 'diameter' in info:
            self.diameter = info['diameter']
        else:
            self.diameter = float('nan')
        
        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            representation = str(f'{self.name}: {self.designation}')
        else:
            representation = str(self.designation)

        return representation

    def __str__(self):
        """Return `str(self)`."""
        if self.diameter != float('nan'):
            return f"A NEO {self.fullname}, has a diameter of {self.diameter:.3f} km and {'is' if self.hazardous else 'is not'} possibly hazardous"
        return f"A NEO {self.fullname}, and {'is' if self.hazardous else 'is not'} possibly hazardous"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"
    
    def create_dict(self):
        """ Create a dictionary from the attributes of the near earth object """

        return {'designation':self.designation, 'name':self.name, 'diameter':self.diameter, 'hazardous':self.hazardous}


class CloseApproach():
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """

        if 'time' in info:
            self.time = cd_to_datetime(info['time'])
        else:
            self.time = None

        if 'distance' in info:
            self.distance = info['distance']
        else:
            self.distance = float('nan')
        
        if 'velocity' in info:
            self.velocity = info['velocity']
        else:
            self.velocity = float('nan')

        # Create an attribute for the referenced NEO, originally None.
        if 'neo' in info:
            self.neo = info['neo']
        else:
            self.neo = None
        
        self.cad_designation = info['designation']

        self.approaches = []

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        if self.time:
            return datetime_to_str(self.time)
        else:
            return "a time not known"

        # TODO: Use self.designation and self.name to build a fullname for this object.
        return ''

    def __str__(self):
        """Return `str(self)`."""
        if self.neo:
            return f"A CloseApproach at {self.time_str} was recorded where {self.neo.fullname} approaches earth at a distance of {self.distance:.3f} au and a velocity of {self.velocity:.3f} km per second"
        return f'A CloseApproach at {self.time_str} was recorded where {self.cad_designation} approaches earth at a distance of {self.distance:.3f} au and a velocity of {self.velocity:.3f} km per second'
    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.3f}, " \
               f"velocity={self.velocity:.3f}, neo={self.neo!r})"
    
    def create_dict(self):
        """ Create a dictionary from the attributes of the close approach """

        return {'datetime': datetime_to_str(self.time), 'distance_au': self.distance, 'velocity_km': self.velocity}
