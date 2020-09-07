
"""
This module is where all masking functions are contained within.
That is, it creates a boolean mask depending on the inputs and
parameters to some data array.

Follows Numpy convention where True is masked and False is not 
masked.
"""

# Masking functions that are common.
from sparrowmonolith.mask.common import *
# All masks should be in this single name-space as it does not
# makes sense to split them up other than for file organization.
from sparrowmonolith.mask.geometric import *
from sparrowmonolith.mask.invalid import *
from sparrowmonolith.mask.value import *