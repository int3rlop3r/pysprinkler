pysprinkler
===========
A small python library that helps you write co-routines
in an event-driven way. In short it 'sprinkles' data passed
to the '.sprinkle' function to all sub-classes of 'Task' in
a round robin manner.

Install:

    pip install pysprinkler

A simple example:

    from pysprinkler import Task, Sprinkler

    class RemoteDBHandler(Task):
    
        def __init__(self):
            print("Started RemoteDBHandler")
    
        def on_data(self, data):
            print("RemoteDBHandler: {}".format(data))
    
        def on_end(self):
            print("Closing RemoteDBHandler")
     
    
    class LocalDBHandler(Task):
    
        def __init__(self):
            print("Started LocalDBHandler")
    
        def on_data(self, data):
            print("LocalDBHandler: {}".format(data))
    
        def on_end(self):
            print("Closing LocalDBHandler")
    
    class STNHandler(Task):
    
        def __init__(self):
            print("Started STNHandler")
    
        def on_data(self, data):
            print("STNHandler: {}".format(data))
    
        def on_end(self):
            print("Closing STNHandler")

    rdb_handler = RemoteDBHandler()
    ldb_handler = LocalDBHandler()
    stn_handler = STNHandler()

    s = Sprinkler([rdb_handler, ldb_handler, stn_handler])
    s.start()

    lines = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]
    for line in lines:
        # sends 'line' to all 'Task's in a 
        # round robin manner
        s.sprinkle(line)
    s.close()

Output:

            Started RemoteDBHandler
            Started LocalDBHandler
            Started STNHandler
            RemoteDBHandler: Line 1
            LocalDBHandler: Line 1
            STNHandler: Line 1
            RemoteDBHandler: Line 2
            LocalDBHandler: Line 2
            STNHandler: Line 2
            RemoteDBHandler: Line 3
            LocalDBHandler: Line 3
            STNHandler: Line 3
            RemoteDBHandler: Line 4
            LocalDBHandler: Line 4
            STNHandler: Line 4
            RemoteDBHandler: Line 5
            LocalDBHandler: Line 5
            STNHandler: Line 5
            Closing RemoteDBHandler
            Closing LocalDBHandler
            Closing STNHandler

