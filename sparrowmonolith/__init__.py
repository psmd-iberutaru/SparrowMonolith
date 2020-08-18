
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

# All operations that deal with string manipulation or formatting.
from sparrowmonolith import string


#####
# Internal modules.
#####
from sparrowmonolith import _tests