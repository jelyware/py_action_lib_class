import json
#TODO import myLock
#TODO import validate

SUCCESS = 0
FAILED = 1

DEBUG = 0

class MonitorActionStats:
    def __init__(self):
        self.actionStats = []

    def addAction(JSONstring):
    '''
        Adds actions and maintains their avg time.
        Param(s): serialized JSON string
    '''
        if not JSONstring:
            print("addAction Failed: No argument provided.")
            return FAILED

        newActionStat = json.loads(JSONstring)
        ###TODO validate.actStat(newActionStat)

        action = newActionStat['action']
        newTime = newActionStat['time']
        actStatIdx = self.search(self.actionStats, len(self.actionStats), action)
        if actStatIdx:
            currAvgTime = self.actionStats[actStatIdx]['time']
            newActionStat['count'] += 1
            self.actionStats[actStatIdx]['time'] = (currAvgTime + newTime) / newActionStat['count']
        else:
            newActionStat['count'] = 1
            self.actionStats.append(newActionStat)
        return status

    def getStats(self):
    ''' Returns actions and their average times in serialized JSON'''
        actionStatsCopy = list(self.actionStats)
        for stat in actionStatsCopy:
            stat.pop(stat['count'])
        if DEBUG:
            print(actionStatsCopy)
        return json.dumps(actionStatsCopy)


    def search(self, arr, n, elem):
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
            elemIdx = self.actionStats.index(elem)

        return elemIdx
