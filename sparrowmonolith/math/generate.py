
"""
Number generators of all types are provided here. From special
random numbers or discrete number sequences. 
"""

import oeis

import sparrowmonolith as mono

# Integer sequences
##########

# All integer sequences rely on the OEIS for their correctness.
def _extract_oeis_values(sequence_key, index, count):
    """ This uses the OEIS and obtains values from it according to
    the values provided.

    Parameters
    ----------
    sequence_key : string
        The name of the sequence that will be used. If it is not 
        an OEIS sequence, an error is raised.
    index : integer
        The 0-indexed index of the location within the sequence 
        that the index should start from.
    count : integer
        The number of values including the index that should be 
        obtained.

    Return
    ------
    oeis_sequence : list
        The sequence from the OEIS.
    """
    if (index < 0):
        # Reverse indexing are not allowed as many OEIS sequences 
        # are infinity long.
        raise mono.InputError("The index from which the sequence will start "
                              "from must be greater than 0.")
    if (count < 1):
        raise mono.InputError("The number count of prime numbers "
                              "returned must be greater than one.")

    # Obtain the OEIS sequence.
    oeis_sequence = getattr(oeis, str(sequence_key), None)
    # Test that the sequence is valid.
    if (oeis_sequence is None):
        raise mono.InputError("The OEIS sequence name is not a valid "
                              "sequence.")
    else:
        # It should be a valid sequence, extract the numbers.
        return oeis_sequence[index:index+count]
    # The code should not reach here.
    raise mono.BrokenLogicError
    return None

def prime_numbers(index, count=1):
    """ This returns a list of prime numbers based on the indexing
    location and the count of numbers to return, in order.

    This function scrapes the numbers from the OEIS and returns
    it based on the user's specifications.

    Parameters
    ----------
    index : integer
        The 0-indexed index of the location within the sequence 
        that the index should start from.
    count : integer
        The number of values including the index that should be 
        obtained.
    
    Return
    ------
    prime_numbers : list
        The sequence of integer numbers.
    """
    # The OEIS sequence name for prime numbers.
    sequence_key = 'A000040'
    # Obtaining the numbers.
    prime_numbers = _extract_oeis_values(sequence_key=sequence_key, 
                                         index=index, count=count)
    # All done.
    return prime_numbers
