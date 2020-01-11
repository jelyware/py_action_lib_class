import concurrent.futures
from monitorActionStats import MonitorActionStats
from random import randint
from time import sleep
from threading import Thread

SUCCESS = 0
FAILED = 1

RNG_START = 100
RNG_END = 200

def generateActionStatsToAdd():
    actionNames = ('run', 'jump', 'fly', 'fight')
    # Randomize occurence of each action in actions list
    actions = [action for action in actionNames for i in range(randint(1,9))]
    print("Initial list of actions:\n", actions)

    newActJsnFmt = '{"action":"%s", "time":%d}'
    return [buildJsonFmtActStat(newActJsnFmt, action) for action in actions]

def buildJsonFmtActStat(fmt, action):
    return fmt % (action, randint(RNG_START, RNG_END))

def testAddAction(newAction):
    print("in testAddAction")
    mas = MonitorActionStats()
    print("         entering while from testAddAction")
    x=0
    while x<1:
        print("calling addAction(newAction),newAction=",newAction)
        mas.addAction(newAction)
        sleep(1)
        x+=1

def testGetStats():
    print("in testGetStats")
    mas = MonitorActionStats()
    print("         entering while from testGetStats")
    x=0
    while x<1:
        print("calling get stats")
        print("################# ACTION STATISTICS:\n", mas.getStats())
        sleep(1)
        x+=1

def generateAddActionThreadPool():
    # Execute thread pool using with statement to ensure threads are cleaned up promptly
    actionStats = generateActionStatsToAdd()
    numThreads = 5
    print("Generating ADD ACTION THREAD POOL (%d threads) to add the following action stats = %s\n" % (numThreads, ACTION_STATS))
    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        # Ready Set GoStart the load operations and mark each future with its action
        # future_to_action = {executor.submit(MonitorActionStats.addAction, actStat): actStat for actStat in actionStats}

        # Execute addAction() concurrently using threads on the actionStats iterable.
        # Optional: Set timeout so addAction() must complete within specified duration.
        executor.map(testAddAction, ACTION_STATS)

def generateGetStatsThreadPool():
    myThreads = []
    print("Generating GET STATS THREAD POOL")
    for i in range( 10 ):
        myThread = Thread( target=testGetStats )
        myThreads.append( myThread )
        myThread.start()

def generateAddActionAndGetStatsThreadPool():
    print("Generating ADD ACTION + GET STATS THREAD POOL")

    # Prep to select actions at random
    actionStats = generateActionStatsToAdd()
    end_rng = len(actionStats)-1
    randomActions = []

    # Generate thread pool
    addActAndGetStatThreads = []
    for i in range( 10 ):
        newAction = actionStats[randint(0,end_rng)]
        addActThread = Thread( target=testAddAction, args=(newAction,) )
        randomActions.append(newAction)
        getStatThread = Thread( target=testGetStats )
        addActAndGetStatThreads.extend( [addActThread, getStatThread] )
    print("RANDOM-SELECTED ACTION LIST = ", randomActions)
    for thread in addActAndGetStatThreads:
        thread.start()

def main():
    print("START TEST: MONITOR ACTION STATS")
    #generateAddActionThreadPool()
    #generateGetStatsThreadPool()
    generateAddActionAndGetStatsThreadPool()
    MonitorActionStats.getStats()
    print("TEST COMPLETED: MONITOR ACTION STATS")

if __name__ == '__main__':
    main()
