from frontal.uni import functions
from temporal import induct
from temporal import grab
from stem import callosum
from frontal.memory import activequeries

import datetime

class Query(object):
    def __init__(self, queryName, queryKeys, querySTContext=None, whitelist=None, require=None):
        self.name = queryName,
        self.keys = queryKeys,
        self.STContext = querySTContext
        self.whitelist = whitelist
        self.require = require

        if querySTContext is not None:
            self.context = True
        else:
            self.context = False
    
    def trace(self, boolean=True):
        if not boolean:
            print(f"Success performing command {self.name}.")
        else:
            induct.stCommit({'savename':self.name,'save':self.STContext})
            print(f"Success performing and saving command {self.name}.")

    def fire(self, obj, keywords, literal, profile):
        print(obj)
        success = obj.func(keywords, literal, profile)
        if success:
            Query.trace(self, self.context)
            return True
        else:
            raise Exception(f"Failed to fire function {self.name}")
    def func():
        pass
    def grade(self, literal, profile, override=False):
        truePass = False
        keyword = literal.lower()
        keyword = literal.split(" ")
        print(str(keyword))
        for key in self.keys:
            print(key)
            for kword in key:
                points = 0
                for word in keyword:
                    if self.require is not None and word in self.require:
                        points += 1.5
                        truePass = True
                    if self.whitelist is not None and word in self.whitelist:
                        points -= 5
                    if word in kword:
                        points += 1
                print(str(points) + " " + str(kword))
                if (points > (len(keyword) * .74) or points > (len(kword) * .74)) or (override and points > (len(keyword) * 0.5)):
                    print("yessir")
                    if truePass and self.require is not None:
                        self.fire(self, keyword,literal,profile)
                        return True
                    elif not truePass and self.require is None:
                        print("yes")
                        self.fire(self, keyword,literal,profile)
                        return True
        return False

def timeFunction(keywords, literal, profile):
    now = datetime.datetime.now()
    phrase = functions.decision([f"The current time is {now.strftime('%I:%M %p')}.",
                             f"It's currently {now.strftime('%I:%M %p')}.",
                             f"The time now is {now.strftime('%I:%M %p')}.",
                             now.strftime('%I:%M %p'),
                             f"It is currently {now.strftime('%I:%M %p')}."])
    callosum.lastProcessed = {"phrase":phrase, "type":"basic"}
    return True

def process(literal, profile, override=False):
    keyword = literal.lower()
    keyword = literal.split(" ")
    nate = grab.requestMemory('longterm', {'type': 'brain', 'path': 'nate'}, True)
    friend = grab.requestMemory('longterm', {'type': 'brain', 'path': 'friends'}, True)
    self = grab.requestMemory('longterm', {'type': 'brain', 'path': 'self'}, True)
    chunks = [nate, friend, self]
    for chunk in chunks:
        for fold in chunk:
            for cell in chunk[fold]:
                for neuron in chunk[fold][cell]:
                    for key in chunk[fold][neuron]['keys']:
                        for kword in key:
                            points = 0
                            for word in keyword:
                                if chunk[fold][neuron]['require'] is not None and word in chunk[fold][neuron]['require']:
                                    points += 1.5
                                    truePass = True
                                if chunk[fold][neuron]['whitelist'] is not None and word in chunk[fold][neuron]['whitelist']:
                                    points -= 5
                                    truePass = False
                                if word in kword:
                                    points += 1
                            print(str(points) + " " + str(kword))
                            if (points > (len(keyword) * .74) or points > (len(kword) * .74)) or (override and points > (len(keyword) * 0.5)):
                                if truePass and chunk[fold][neuron]['require'] is not None:
                                    neuron['fire'](self, keyword,literal,profile)
                                    return True
                                elif not truePass and chunk[fold][neuron]['require'] is None:
                                    neuron['fire'](self, keyword,literal,profile)
                                    return True