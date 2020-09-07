
import sparrowmonolith as mono

def ravel_dictionary(dictionary, conflict):
    """ This function unravels a dictionary, un-nesting
    nested dictionaries into a single dictionary. If
    conflicts arise, then the conflict rule is used.
    
    The keys of dictionary entries that have dictionary
    values are discarded.
    
    Parameters
    ----------
    dictionary : dictionary
        The dictionary to be unraveled.
    conflict : string
        The conflict rule. It may be one of these:
        
        * 'raise'
            If a conflict is detected, a 
            sparrowmonolith.DataError will be raised.
        * 'superior'
            If there is a conflict, the least 
            nested dictionary takes precedence. Equal
            levels will prioritize via alphabetical. 
        * 'inferior'
            If there is a conflict, the most
            nested dictionary takes precedence. Equal
            levels will prioritize via anti-alphabetical.
        
    Returns
    -------
    raveled_dictionary : dictionary
        The unraveled dictionary. Conflicts were replaced
        using the conflict rule.
    """
    # Reaffirm that this is a dictionary.
    if (not isinstance(dictionary, dict)):
        dictionary = dict(dictionary)
    else:
        # All good.
        pass
    # Ensure the conflict is a valid conflict type.
    conflict = str(conflict).lower()
    if (conflict not in ('raise', 'superior', 'inferior')):
        raise mono.InputError("The conflict parameter must be one the "
                              "following: 'raise', 'superior', 'inferior'.")
        
    # The unraveled dictionary.
    raveled_dictionary = dict()
    # Sorted current dictionary. This sorting helps
    # with priorities prescribed by `conflict`.
    sorted_dictionary = dict(sorted(dictionary.items()))
    for keydex, itemdex in sorted_dictionary.items():
        # If this entry is a dictionary, then 
        # recursively go through it like a tree search.
        if (isinstance(itemdex, dict)):
            temp_dict = ravel_dictionary(
                dictionary=itemdex, conflict=conflict)
        else:
            # It is a spare item, create a dictionary.
            temp_dict = {keydex:itemdex}
        # Combine the dictionary, but, first, check for
        # intersection conflicts.
        if (len(raveled_dictionary.keys() & temp_dict.keys()) != 0):
            # There are intersections. Handle them based 
            # on `conflict`.
            if (conflict == 'raise'):
                raise mono.DataError("There are conflicts in these two "
                                     "dictionaries: \n"
                                     "Temp : {temp} \n Ravel : {ravel}"
                                     .format(temp=temp_dict, 
                                             ravel=raveled_dictionary))
            elif (conflict == 'superior'):
                # Preserve the previous entries as they are
                # either higher up in the tree or are
                # ahead alphabetically.
                raveled_dictionary = {**temp_dict, **raveled_dictionary}
            elif (conflict == 'inferior'):
                # Preserve the new entires as they are
                # either lower in the tree or are behind
                # alphabetically.
                raveled_dictionary = {**raveled_dictionary, **temp_dict}
            else:
                # The code should not get here.
                raise mono.BrokenLogicError("The input checking of conflict "
                                            "should have caught this.")
        else:
            # They can just be combined as normal. Taking superior
            # as the default.
            raveled_dictionary = {**temp_dict, **raveled_dictionary}
            
    # All done.
    return raveled_dictionary





    