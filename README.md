# py_action_lib_class
Small library class in Python that can be used to maintain and fetch average time statistics for an array of actions.
This class assumes that an end user will be making concurrent calls into all functions.


Assumptions:
- total time will not exceed the size of a uint long
- a single process where a single interpreter is handling multiple threads
