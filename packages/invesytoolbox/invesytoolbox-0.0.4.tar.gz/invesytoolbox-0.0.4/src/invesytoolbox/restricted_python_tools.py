# -*- coding: utf-8 -*-
"""
This module implements functionality missig in restricted Python
"""


##  Check if a list is contained in another list
#
#   'all' is not available in restricted Python
#
#   @param contained: the list to check if its contained
#   @param container: the list to check it it containes the other one
def contains_all(
    container: list,
    contained: list
) -> bool:

    return all(el in container for el in contained)


##  Check if at list one element of a list is contained in another list
#
#   'any' is not available in restricted Python
#
#   @param contained: the list to check if its contained
#   @param container: the list to check it it containes the other one
def contains_any(
    container: list,
    contained: list
) -> bool:

    return any(el in container for el in contained)


##  Removes duplicates from a list
#
#   restricted Python does not allow sets
def remove_duplicates(lst: list) -> list:
    return list(set(lst))
