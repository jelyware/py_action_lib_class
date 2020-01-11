import concurrent.futures
from monitorActionStats import MonitorActionStats
from random import randint
from time import sleep
from threading import Thread

SUCCESS = 0
FAILED = 1

RNG_START = 100
RNG_END = 200

VERBOSE = False     ### TODO: Implement logging class

def generateActionStatsToAdd():
    actionNames = ('run', 'jump', 'fly', 'fight')
    # Randomize occurence of each action in actions list
    actions = [action for action in actionNames for i in range(randint(1,9))]
    if VERBOSE:
        print("Initial list of actions:\n", actions)

    newActJsnFmt = '{"action":"%s", "time":%d}'
    return [buildJsonFmtActStat(newActJsnFmt, action) for action in actions]

def buildJsonFmtActStat(fmt, action):
    return fmt % (action, randint(RNG_START, RNG_END))

def testAddAction(newAction):
    mas = MonitorActionStats()
    rng = 10
    x = 0
    while x < rng:
        mas.addAction(newAction)
        sleep(1)
        x += 1

def testGetStats():
    if VERBOSE:
        print("Running testGetStats()")
    mas = MonitorActionStats()
    rng = 10
    x = 0
    while x < rng:
        print("==============> ACTION STATISTICS:\n", mas.getStats())
        sleep(1)
        x += 1

def generateAddActionThreadPool():
    numThreads = 5
    actionStats = generateActionStatsToAdd()
    print("Generating ADD ACTION THREAD POOL (%d threads) " % numThreads \
        + "to add the following action stats = %s\n" % actionStats)

    # Execute thread pool using with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=numThreads) as executor:
        # Ready-Set-Go Method (not used here):
        #   Start the load operations and mark each future with its action
        #   future_to_action = {executor.submit(MonitorActionStats.addAction, actStat): actStat for actStat in actionStats}

        # Execute addAction() concurrently using threads on the actionStats iterable.
        # Optional: Set timeout so addAction() must complete within specified duration.
        executor.map(testAddAction, actionStats)

def generateGetStatsThreadPool():
    numThreads = 10
    print("Generating GET STATS THREAD POOL (%d threads)" % numThreads)
    myThreads = []
    for i in range( numThreads ):
        myThread = Thread( target=testGetStats )
        myThreads.append( myThread )
        myThread.start()

def generateAddActionAndGetStatsThreadPool():
    numThreads = 10
    print("Generating ADD ACTION + GET STATS THREAD POOL (%d threads)" % numThreads)

    # Prep to select actions at random
    actionStats = generateActionStatsToAdd()
    end_rng = len(actionStats)-1
    randomActions = []

    # Generate thread pool
    addActAndGetStatThreads = []
    for i in range( numThreads ):
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
    generateAddActionThreadPool()
    generateGetStatsThreadPool()
    generateAddActionAndGetStatsThreadPool()
    MonitorActionStats.getStats()
    print("TEST COMPLETED: MONITOR ACTION STATS")

if __name__ == '__main__':
    main()
