
#####
# Upper level modules.
##########
# These are for error types and warning types.
from sparrowmonolith.error import *

#####
# Sub modules.
##########
# All modules and functions dealing with external APIs
from sparrowmonolith import api
# All modules and functions dealing with file input and output.
from sparrowmonolith import io

# All module and functions dealing with the creation of masks.
from sparrowmonolith import mask

# All modules and functions dealing with mathematics. 
from sparrowmonolith import math

# All modules and functions dealing with meta-programing.
from sparrowmonolith import meta

# All operations that deal with the manipulation of objects in 
# general, rather than any real form of computation.
from sparrowmonolith import object


#####
# Internal modules.
#####
from sparrowmonolith import _test


# In general, comments do not exceed 72, or here                    |
# In general, add code do not exceed 79, or here                            |