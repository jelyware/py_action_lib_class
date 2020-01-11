# MonitorActionStats
Small library class in Python that can be used to maintain and fetch average time statistics for an array of actions.

This class assumes that an end user will be making concurrent calls into all functions.  
Two shared data variables exist: STATS and LOCK.  I use Python's threading class, Lock, to serialize 

The two primary functions in MonitorActionStats are:
- Add Action
    ```
    addAction (string) returning error 
    ```
    This function accepts a json serialized string of the form below and maintains an average time for each action. 
    3 sample inputs:
    ```
        1) {"action":"jump", "time":100}
        2) {"action":"run", "time":75}
        3) {"action":"jump", "time":200} 
    ```
    It is assumed that an end user will be making concurrent calls into this function.
    
- Get Statistics
    ```
    getStats () returning string
    ```
    This function accepts no input and returns a serialized json array of the average time for each action that has 
    been provided to the addAction function. Example output after the above 3 sample calls: 
    ```python
            [ 
                {"action":"jump", "avg":150}, 
                {"action":"run", "avg":75}   ]
    ``` 
    It is assumed that an end user will be making concurrent calls into this function. 

### Language
- Python 3.7.6

### Assumptions:
- For each action, total time per action does not exceed the size of an integer. 
- This library class will be run on a single process where a single interpreter is handling multiple threads.
- Performance improvements can be integrated after deployment to production.
- Python 3.7.6 installed in the environment where this library class will be integrated.
- This class will reside in a /lib directory when integrated.
- Developers integrating this class are good with tabs preset to 4 spaces. :)

### Knowns:
- Integers in Python 3 have unlimited precision (replacing long int).

## Instructions
- Install Python 3.7.x if not already installed (Python 2.7.x legacy support is not included).
- Add this class to your /lib directory along with its test module: test_MonitorActionStats.py.
- To use the class, import it from your lib directory and instantiate it: 
    ```python
    from lib.monitorActionStats import MonitorActionStats
    ...
    mas = MonitorActionStats()
    ...
    mas.addAction(newAction)
    mas.getStats()
    ```
- To run the test module, open a command prompt and run the following:
  > C:\Code\GitHub\dev\lib\>python test_MonitorActionStats.py
  
## Future Improvements
- Add and use a logging class in lieu of cluttering debug statements
- Improve time efficiency through more sophisticated concurrent programming.
