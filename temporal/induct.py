from temporal.longterm import friends
from temporal.longterm import nate
from temporal.longterm import self
from temporal.longterm import profiles
from temporal.longterm import weather
from temporal.longterm import lists

from temporal import shortterm
from temporal import grab

import warnings

def ltCommit(request, rewrite=True):
    '''\tlongterm request format\trequest dict\tsaveplace list\tsavename str\tsavetype str\tsave\n'''

    if rewrite:
        if 'friends' in request['saveplace'][0]:
            if request['savetype'] == 'fold':
                friends.memories[request['savename']] = {}
            elif request['savetype'] == 'cell':
                if request['saveplace'][1] not in friends.memories:
                    friends.memories[request['saveplace'][1]] = {}
                    warnings.warn(f"[WARN] Couldn't find original fold. Making a new one under {request['saveplace'][1]}.")
                friends.memories[request['saveplace'][1]][request['savename']] = {}
            elif request['savetype'] == 'neuron':
                if request['saveplace'][1] not in friends.memories:
                    friends.memories[request['saveplace'][1]] = {}
                    warnings.warn(f"[WARN] Couldn't find original fold. Making a new one under {request['saveplace'][1]}.")                
                if request['saveplace'][1][request['saveplace'][2]] not in friends.memories:
                    friends.memories[request['saveplace'][1]][request['saveplace'][2]] = {}
                    warnings.warn(f"[WARN] Couldn't find original cell. Making a new one under {request['saveplace'][2]}.")
                friends.memories[request['saveplace'][1]][request['saveplace'][2]][request['savename']] = request['save']
        elif 'profiles' in request['saveplace'][0]:
            if request['savetype'] == 'fold':
                profiles.memories[request['savename']] = {}
            elif request['savetype'] == 'cell':
                if request['saveplace'][1] not in profiles.memories:
                    profiles.memories[request['saveplace'][1]] = {}
                    warnings.warn(f"[WARN] Couldn't find original fold. Making a new one under {request['saveplace'][1]}.")
                profiles.memories[request['saveplace'][1]][request['savename']] = {}
            elif request['savetype'] == 'neuron':
                if request['saveplace'][1] not in profiles.memories:
                    profiles.memories[request['saveplace'][1]] = {}
                    warnings.warn(f"[WARN] Couldn't find original fold. Making a new one under {request['saveplace'][1]}.")                
                if request['saveplace'][1][request['saveplace'][2]] not in profiles.memories:
                    profiles.memories[request['saveplace'][1]][request['saveplace'][2]] = {}
                    warnings.warn(f"[WARN] Couldn't find original cell. Making a new one under {request['saveplace'][2]}.")
                profiles.memories[request['saveplace'][1]][request['saveplace'][2]][request['savename']] = request['save']
        elif 'nate' in request ['saveplace'][0]:
            if request['savetype'] == 'fold':
                nate.memories[request['savename']] = {}
            elif request['savetype'] == 'cell':
                if request['saveplace'][1] not in nate.memories:
                    nate.memories[request['saveplace'][1]] = {}
                    warnings.warn(f"[WARN] Couldn't find original fold. Making a new one under {request['saveplace'][1]}.")
                nate.memories[request['saveplace'][1]][request['savename']] = {}
            elif request['savetype'] == 'neuron':
                if request['saveplace'][1] not in nate.memories:
                    nate.memories[request['saveplace'][1]] = {}
                    warnings.warn(f"[WARN] Couldn't find original fold. Making a new one under {request['saveplace'][1]}.")                
                if request['saveplace'][1][request['saveplace'][2]] not in nate.memories:
                    nate.memories[request['saveplace'][1]][request['saveplace'][2]] = {}
                    warnings.warn(f"[WARN] Couldn't find original cell. Making a new one under {request['saveplace'][2]}.")
                nate.memories[request['saveplace'][1]][request['saveplace'][2]][request['savename']] = request['save']     
        elif 'self' in request ['saveplace'][0]:
            if request['savetype'] == 'fold':
                self.memories[request['savename']] = {}
            elif request['savetype'] == 'cell':
                if request['saveplace'][1] not in self.memories:
                    self.memories[request['saveplace'][1]] = {}
                    warnings.warn(f"[WARN] Couldn't find original fold. Making a new one under {request['saveplace'][1]}.")
                self.memories[request['saveplace'][1]][request['savename']] = {}
            elif request['savetype'] == 'neuron':
                if request['saveplace'][1] not in self.memories:
                    self.memories[request['saveplace'][1]] = {}
                    warnings.warn(f"[WARN] Couldn't find original fold. Making a new one under {request['saveplace'][1]}.")                
                if request['saveplace'][1][request['saveplace'][2]] not in self.memories:
                    self.memories[request['saveplace'][1]][request['saveplace'][2]] = {}
                    warnings.warn(f"[WARN] Couldn't find original cell. Making a new one under {request['saveplace'][2]}.")
                self.memories[request['saveplace'][1]][request['saveplace'][2]][request['savename']] = request['save']          
        elif 'weather' in request ['saveplace'][0]:
            weather.memories[request['savetype']] = request['save']



def inituser(name):
    if type(name) is dict:
        return name
    success = grab.requestMemory('longterm',{'type':'fold','path':['profiles',name], 'check':name}, returnMem=True)
    if success:
        return success
    else:
        ltCommit({'saveplace':['profiles', name, 'info'], 'savetype':'neuron', 'savename':'prefname', 'save':name})
        success = grab.requestMemory('longterm',{'type':'fold','path':['profiles',name], 'check':name}, returnMem=True)
        print(success)
        return success
        
def stCommit(request, rewrite=True):
    '''short term request format\trequest dict\tsavename str\tsave'''
    shortterm.memories[request['savename']] = request['save']
    if len(shortterm.memories) > 15:
        shortterm.memories.pop(len(shortterm.memories)-1)