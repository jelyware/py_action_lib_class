import json
from copy import deepcopy
from threading import Lock, get_ident
from traceback import print_exc

SUCCESS = 0
FAILED = 1

DEBUG = False   # Enable for testing only

class ActionStats:
    '''
        Static class for shared data:
            STATS:  Action statistics, a list of action stat dictionaries.
            LOCK:   Used to serialize access to STATS.
    '''
    STATS = []
    LOCK = Lock()

class MonitorActionStats:
    '''
        Monitor action statistics by maintaining the average execution time
        of various actions.  Provides a statistics getter function.  Accounts
        for concurrent end user calls to all public functions using Lock().
    '''

    #---------------------------------------------------------------------------#
    def addAction(self, newAction):
        '''
            Adds newAction, a serialized JSON string containing action and
            time, e.g. {'action':'jump', 'time':100}. Tracks total time for
            each action (total time is used to calculate avg time).
        '''
        status = FAILED
        try:
            newActionStat = self._getNewActionStatDict(newAction)
            if DEBUG:
                print("In addAction(): New action stat = ", newActionStat)
            if newActionStat != {} and self._validateNewActionStat(newActionStat) == SUCCESS:
                action = newActionStat['action']
                newTime = newActionStat['time']
                if ActionStats.LOCK.acquire():
                    actStatIdx = self._searchStats(ActionStats.STATS, len(ActionStats.STATS), action)
                    if actStatIdx != None:
                        if DEBUG:
                            print("EXISTING ACTION NEEDS UPDATED")
                            print("ACQUIRING LOCK to update existing action.")
                        currTime = ActionStats.STATS[actStatIdx]['time']
                        ActionStats.STATS[actStatIdx]['count'] += 1
                        ActionStats.STATS[actStatIdx]['time'] = int(currTime + newTime)
                        ActionStats.LOCK.release()
                        if DEBUG:
                            print("LOCK RELEASED: Done updating existing action.")
                        status = SUCCESS
                    else:
                        if DEBUG:
                            print("NEW ACTION NEEDS ADDED")
                            print("ACQUIRING LOCK to add new action.")
                        #if ActionStats.LOCK.acquire():
                        newActionStat['time'] = int(newActionStat['time'])
                        ActionStats.STATS.append(newActionStat)
                        ActionStats.LOCK.release()
                        if DEBUG:
                            print("LOCK RELEASED - Done adding new action.")
                        status = SUCCESS
        except Exception as exc:
            print("addAction() EXCEPTION: ", exc)
            print_exc()

        if DEBUG:
            print("EXITING ADD ACTION with status: %d, thread: %d", (status, get_ident()))
        return status

    #---------------------------------------------------------------------------#
    def getStats(self):
        '''
            Returns actions and their average times in serialized JSON.
        '''
        jsonifiedCopy = []
        try:
            if DEBUG:
                print("ACQUIRING LOCK TO GET STATS")
            if ActionStats.LOCK.acquire():
                actionStatsCopy = deepcopy(ActionStats.STATS)
                ActionStats.LOCK.release()
                if DEBUG:
                    print("RELEASING LOCK TO GET STATS")
                # Calculate avg time per action and cleanup 'count'
                for stat in actionStatsCopy:
                    stat['time'] = stat['time'] / stat['count']
                    stat.pop('count')
                if DEBUG:
                    print("actionStatsCopy", actionStatsCopy)
                jsonifiedCopy = json.dumps(actionStatsCopy)
            else:
                print("getStats(): Failed to acquire ActionStats.LOCK.")
        except Exception as exc:
            print("getStats() EXCEPTION: ", exc)
            print_exc()

        if DEBUG:
            print("EXITING GET STATS with status: %d, thread: %d", (status, get_ident()))
        return jsonifiedCopy

    #---------------------------------------------------------------------------#
    def _searchStats(self, arr, n, elem):
        '''
            Search action statistics for specified action (elem).
            Worst time complexity: O(n/2)
            Reference: https://www.geeksforgeeks.org/front-and-back-search-in-unsorted-array/
        '''
        front = 0
        back = n - 1
        found = False
        elemIdx = None
        # Keep searching while two indexes do not cross.
        while (front <= back):
            if (arr[front]['action'] == elem):
                elemIdx = front
            elif (arr[back]['action'] == elem):
                elemIdx = back
            if elemIdx is not None:
                break
            front += 1
            back -= 1
        if DEBUG:
            print("EXITING SEARCH STATS with status: %d, thread: %d", (status, get_ident()))
        return elemIdx

    #---------------------------------------------------------------------------#
    def _validateNewActionStat(self, stat):
        '''
            Validate new action stat dictionary after actionAdd() argument
            deserialized. TODO: Create/use custom error codes or error classes
            to remove print statement clutter.
        '''
        status = FAILED
        # Check for valid dict type of stat arg
        if isinstance(stat, dict):
            # Check for action and time keys
            if 'action' in stat and 'time' in stat:
                # Check for valid action and time value types
                if isinstance(stat['action'], str) \
                and isinstance(stat['time'], int):
                    status = SUCCESS
                elif isinstance(stat['action'], str) \
                and isinstance(stat['time'], str):
                    try:
                        stat['time'] = int(stat['time'])
                        status = SUCCESS
                    except TypeError as ec:
                        print("[_validateNewActionStat() Failed] " \
                            + "Invalid type for time value:", ec)
                else:
                    print("[_validateNewActionStat() Failed] " \
                        + "Invalid type for action and/or time values.")
                    print("Type of 'action' value: ", type(stat['action']))
                    print("Type of 'time' value: ", type(stat['time']))
            else:
                print("[_validateNewActionStat() Failed] " \
                    + "Missing necessary dictionary keys. " \
                    + "New action stat dictionary = ", repr(stat))
        else:
            print("[_validateNewActionStat() Failed] " \
                + "Invalid type - new action stat should be dict type: ", repr(stat))
            print("New action stat type: ", type(stat))

        if DEBUG:
            print("EXITING VALIDATION with status: %d, thread: %d", (status, get_ident()))
        return status

    #---------------------------------------------------------------------------#
    def _getNewActionStatDict(self, newAction):
        '''
            Deserializes newAction, a serialized JSON string. Returns dictionary
            that contains action to add, example: {'action':'run', 'time': 100, 'count': 1}.
            Count added to track duplicate actions - used to calculate avg time.
        '''
        newActionStat = {}
        if not newAction:
            print("[_getNewActionStatDict() Failed] " \
                + "Invalid or emtpy addAction() argument: ", repr(newAction))
        try:
            # Deserialize JSON string containing new action stat dict.
            newActionStat = json.loads(newAction)
            # Add count and initialize to 1.
            newActionStat['count'] = 1
        except Exception as ec:
            print("[_getNewActionStatDict() Failed] " \
                + "Could not deserialize addAction() argument: ", ec)
        return newActionStat
