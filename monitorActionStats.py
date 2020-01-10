import json
from threading import Lock

SUCCESS = 1
FAILED = 0

DEBUG = 0

class MonitorActionStats:
    '''
        Monitor action statistics by maintaining the average execution time
        of various actions.  Provides a statistics getter function.  Accounts
        for concurrent end user calls to all public functions using Lock().
    '''
    ActionStats = []
    ActionStatsLock = Lock()

    def addAction(self, newAction):
        '''
            Adds newAction, a serialized JSON string containing action and
            time, e.g. {'action':'jump', 'time':100}. Tracks total time for
            each action (total time is used to calculate avg time).
        '''
        status = FAILED
        newActionStat = getNewActionStatDict(newAction)
        if newActionStat != {} and _validateNewActionStat(newActionStat):
            action = newActionStat['action']
            newTime = newActionStat['time']
            actStatIdx = self._search(ActionStats, len(ActionStats), action)
            if actStatIdx:
                if ActionStatsLock.acquire():
                    currTime = ActionStats[actStatIdx]['time']
                    newActionStat['count'] += 1
                    ActionStats[actStatIdx]['time'] = long(currTime + newTime)
                    ActionStatsLock.release()
                    status = SUCCESS
            else:
                if ActionStatsLock.acquire():
                    newActionStat['count'] = 1
                    newActionStat['time'] = long(newActionStat['time'])
                    ActionStats.append(newActionStat)
                    ActionStatsLock.release()
                    status = SUCCESS
        return status

    def getStats(self):
        ''' Returns actions and their average times in serialized JSON'''
        jsonCopy = []
        if ActionStatsLock.acquire():
            actionStatsCopy = list(ActionStats)
            ActionStatsLock.release()
            for stat in actionStatsCopy:
                stat['time'] = stat['time'] / stat['count']
                stat.pop(stat['count'])
            if DEBUG:
                print(actionStatsCopy)
            jsonifiedCopy = json.dumps(actionStatsCopy)
        else:
            print("getStats Failed: Failed to acquire ActionStatsLock.")
        return jsonifiedCopy


    def _search(self, arr, n, elem):
        '''
            Use to achieve O(n/2) complexity when searching action statistics dictionary.
            Reference: https://www.geeksforgeeks.org/front-and-back-search-in-unsorted-array/
        '''
        front = 0
        back = n - 1
        found = False
        elemIdx = None

        # Keep searching while two indexes do not cross.
        while (front <= back):
            if (arr[front] == elem or arr[back] == elem):
                found = True
            front += 1
            back -= 1

        if found:
            elemIdx = ActionStats.index(elem)

        return elemIdx


    def _validateNewActionStat(stat):
        '''
            Validate new action stat dictionary after actionAdd() argument
            deserialized. TODO: Create/use custom error codes or error classes to
            remove print statement clutter.
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

        return status


    def _getNewActionStatDict(newAction):
        '''
            Deserializes newAction, a serialized JSON string. Returns dictionary
            that contains action to add.
        '''
        newActionStat = {}
        if not newAction:
            print("[_getNewActionStatDict() Failed] " \
                + "Invalid or emtpy addAction() argument: ", repr(newAction))
        try:
            # Deserialize JSON string containing new action stat dictionary
            newActionStat = json.loads(newAction)
        except Exception as ec:
            print("[_getNewActionStatDict() Failed] " \
                + "Could not deserialize addAction() argument: ", ec)
        return newActionStat
