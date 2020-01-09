import json
#TODO import myLock
#TODO import validate

SUCCESS = 0
FAILED = 1

DEBUG = 0

class MonitorActionStats:
    ActionStats = []

    def __init__(self):
        pass

    def addAction(JSONstring):
        '''
            Adds actions and maintains their avg time.
            Param(s): serialized JSON string
        '''
        if not JSONstring:
            print("addAction Failed: Invalid or empty argument")
            if DEBUG:
                print("addAction argument = %s" % repr(JSONstring))
            return FAILED

        newActionStat = json.loads(JSONstring)
        ###TODO validate.actStat(newActionStat)

        action = newActionStat['action']
        newTime = newActionStat['time']
        actStatIdx = self._search(ActionStats, len(ActionStats), action)
        if actStatIdx:
            currTime = ActionStats[actStatIdx]['time']
            newActionStat['count'] += 1
            ActionStats[actStatIdx]['time'] = long(currTime + newTime)
        else:
            newActionStat['count'] = 1
            newActionStat['time'] = long(newActionStat['time'])
            ActionStats.append(newActionStat)
        return status

    def getStats(self):
        ''' Returns actions and their average times in serialized JSON'''
        actionStatsCopy = list(ActionStats)
        for stat in actionStatsCopy:
            stat['time'] = stat['time'] / stat['count']
            stat.pop(stat['count'])
        if DEBUG:
            print(actionStatsCopy)
        return json.dumps(actionStatsCopy)


    def _search(self, arr, n, elem):
        ''' Reference: https://www.geeksforgeeks.org/front-and-back-search-in-unsorted-array/'''
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
