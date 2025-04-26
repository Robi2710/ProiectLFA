class State:
    def __init__(self):
        self.transitions = {}

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept