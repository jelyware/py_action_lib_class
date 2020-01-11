import concurrent.futures
from monitorActionStats import MonitorActionStats
from random import randint


def generateActionStatsToAdd():
    range_start = 100
    range_end = 200
    actionNames = ('run', 'jump', 'fly', 'fight')
    actions = [action for i in randint(0,9) for action in actionNames]
    print("Initial list of actions:\n", actions)
    action_stat_json_fmt_str = '{"action":"%s", "time":%d}'
    return [buildJsonFmtActStat(action) % for action in actions]

def buildJsonFmtActStat(action):
    return action_stat_json_fmt_str % (action, randint(range_start,range_end))


def testAddAction():
    mas = MonitorActionStats()
    while True:
        mas.addAction()
        sleep(1)

def generateAddActionThreadPool():
    # Execute thread pool using with statement to ensure threads are cleaned up promptly
    actionStats = generateActionStatsToAdd()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its action
        # future_to_action = {executor.submit(MonitorActionStats.addAction, actStat): actStat for actStat in actionStats}

        # Execute addAction() concurrently using threads on the actionStats iterable.
        # Set timeout so addAction() must complete within 5 seconds
        future_to_action = executor.map(testAddAction, actionStats)
        for future in concurrent.futures.as_completed(future_to_action):
            action = future_to_action[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%s generated an exception: %s' % (action, exc))
            else:
                print('%s page is %d bytes' % (action, len(data)))


def testGetStats():
    mas = MonitorActionStats()
    while True:
        mas.getStats()
        sleep(1)

def generateGetStatsThreadPool():
    from threading import sleep, Thread
    myThreads = []
    for i in range( 10 ):
        myThread = Thread( target=testGetStat )
        myThreads.append( myThread )
        myThread.run()
