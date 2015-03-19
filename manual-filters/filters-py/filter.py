''' Module: filter

    Classes contained: Filter

    Created by S.T. Castle on 2015-01-16

    Create filters for image convolutions.
'''

import string
import math

class Filter:
    '''A box, tent, or gaussian filter.'''

    # Constructor.
    # params: filter_type: string with value BOX, TENT, or GAUSSIAN.
    #         filter_r: integer radius of the filter.
    # throws: KeyError
    def __init__(self, filter_type, filter_r):
        self.type = string.upper(filter_type)  # Filter type.
        self.r = filter_r                      # Filter radius.
        self.w = 2*self.r + 1;                 # Filter width.
        self.f = []                            # Filter values.
        
        # Stores the available filter types.
        types = {
            'BOX'      : self._make_box,
            'TENT'     : self._make_tent,
            'GAUSSIAN' : self._make_gaussian,
        }

        # Make the filter.
        try:
            types[self.type]()
        except KeyError:
            print 'ERROR: Filter type \'' +filter_type+ '\' is not supported.'

    # Methods to make the filter of the specified type.

    def _make_box(self):
        val = 1.0 / self.w  # Normalized, uniform values.
        # Put values into filter with width w.
        for i in range(self.w):
            self.f.append(val)

    def _make_tent(self):
        sum = 0.0  # Track the sum of filter values for normalization.

        # Compute the value at each position in the filter.
        for i in range(self.w):
            x = abs(i-self.r)  # Displacement from center of filter.
            val = (1.0-(x*1.0/self.r))/self.r
            self.f.append(val)
            sum += val

        # Normalize values in the filter.
        for i in range(self.w):
            self.f[i] = self.f[i] / sum

    def _make_gaussian(self):
        sum = 0.0  # Track the sum of filter values for normalization.
        sigma = (self.r - 1.0) / 3.0; # Standard dev for Gaussian distro.

        # Compute filter values.
        for i in range(self.w):
            # Calculate vale for filter at position i-radius.
            # This is the displacement from the center pixel (at index self.r).
            val = self._gauss(i-self.r, sigma)
            self.f.append(val)
            sum += val

        # Normalize values in the filter.
        for i in range(self.w):
            self.f[i] = self.f[i] / sum

    # Gaussian function.
    def _gauss(self, x, sig):
        return ((1.0/(sig*math.sqrt(2*math.pi)))*math.exp(-x*x/(2*sig*sig)))

    # Accessor Methods

    # Return the filter type.
    def get_type(self):
        return self.type

    # Return the filter radius.
    def get_radius(self):
        return self.r

    # Return the filter list.
    def get_filter(self):
        return self.f
