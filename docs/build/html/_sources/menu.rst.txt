menu Function
=============

The ``menu`` function displays a list of selectable options to the user and returns the index of the chosen option.
This function is useful in CLI applications where user interaction is required to choose between different actions.

.. autofunction:: evdspy.menu

Function Details
----------------

.. autofunction:: evdspy.menu

Parameters
----------
options : list of str
    A list of strings that represent the choices available to the user.

Returns
-------
int
    The index of the option selected by the user, where the first option is indexed as 0.

Raises
------
ValueError
    If the user's input is not a valid option index.

Example Usage
-------------
Here is a simple usage example that demonstrates how to use the ``menu`` function:

.. code-block:: python

    from evdspy import menu
    menu()

This example will display a menu with three options. After the user selects an option, the function will print the selected option.

