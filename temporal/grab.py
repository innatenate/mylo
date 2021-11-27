from temporal.longterm import friends
from temporal.longterm import nate
from temporal.longterm import profiles
from temporal.longterm import self
from temporal.longterm import weather
from temporal.longterm import lists
from temporal import shortterm

def requestMemory(type, context, returnMem=False):
    '''context dict
    type
    path friends daigen or self howmade
    check'''
    if type == "longterm":
        if context['type'] == 'weather':
            return weather.memories[context['path']]
        if context['type'] == 'brain' and returnMem:
            if context['path'] == 'nate':
                return nate.memories
            elif context['path'] == 'friends':
                return friends.memories
            elif context['path'] == 'self':
                return self.memories
            elif context['path'] == 'weather':
                return weather.memories
            elif context['path'] == 'profiles':
                return profiles.memories
        if context['type'] == 'fold':
            if context['path'][0] == 'friends':
                if context['check'] in friends.memories:
                    if returnMem:
                        return friends.memories[context['path'][1]]
                    else:
                        return True
                else:
                    return False
            if context['path'][0] == 'nate':
                if context['check'] in nate.memories:
                    if returnMem:
                        return nate.memories[context['path']]
                    else:
                        return True               
                else:
                    return False
            if context['path'][0] == 'profiles':
                if context['check'] in profiles.memories:
                    if returnMem:
                        return profiles.memories[context['path'][1]]
                    else:
                        return True                
                else:
                    return False
            if context['path'][0] == 'self':
                if context['check'] in self.memories:
                    if returnMem:
                        return self.memories[context['path'][1]]
                    else:
                        return True                
                else:
                    return False
        elif context['type'] == 'cell':
            if context['path'][0] == 'friends':
                if context['check'] in friends.memories[context['path'][1]]:
                    if returnMem:
                        return friends.memories[context['path'][1]][context['path'][2]]
                    else:
                        return True                 
                else:
                    return False
            if context['path'][0] == 'nate':
                if context['check'] in nate.memories[context['path'][1]]:
                    if returnMem:
                        return nate.memories[context['path'][1]][context['path'][2]]
                    else:
                        return True                 
                else:
                    return False
            if context['path'][0] == 'profiles':
                if context['check'] in profiles.memories[context['path'][1]]:
                    if returnMem:
                        return profiles.memories[context['path'][1]][context['path'][2]]
                    else:
                        return True                 
                else:
                    return False
            if context['path'][0] == 'self':
                if context['check'] in self.memories[context['path'][1]]:
                    if returnMem:
                        return self.memories[context['path'][1]][context['path'][2]]
                    else:
                        return True                
                else:
                    return False       
        elif 'neuron' in context['type'] and 'exist' in context['type']:
            if context['path'][0] == 'friends':
                if context['check'] in friends.memories[context['path'][1]][context['path'][2]]:
                    return True
                else:
                    return False
            if context['path'][0] == 'nate':
                if context['check'] in nate.memories[context['path'][1]][context['path'][2]]:
                    return True
                else:
                    return False
            if context['path'][0] == 'profiles':
                if context['check'] in profiles.memories[context['path'][1]][context['path'][2]]:
                    return True
                else:
                    return False
            if context['path'][0] == 'self':
                if context['check'] in self.memories[context['path'][1]][context['path'][2]]:
                    return True
                else:
                    return False        
        elif 'neuron' in context['type'] and 'value' in context['type']:
            if context['path'][0] == 'friends':
                if context['check'] in friends.memories[context['path'][1]][context['path'][2]]:
                    return friends.memories[context['path'][1]][context['path'][2]][context['path'][3]]
                else:
                    return False
            if context['path'][0] == 'nate':
                if context['check'] in nate.memories[context['path'][1]][context['path'][2]]:
                    return nate.memories[context['path'][1]][context['path'][2]][context['path'][3]]
                else:
                    return False
            if context['path'][0] == 'profiles':
                if context['check'] in profiles.memories[context['path'][1]][context['path'][2]]:
                    return profiles.memories[context['path'][1]][context['path'][2]][context['path'][3]]
                else:
                    return False
            if context['path'][0] == 'self':
                if context['check'] in self.memories[context['path'][1]][context['path'][2]]:
                    return self.memories[context['path'][1]][context['path'][2]][context['path'][3]]
                else:
                    return False           
    elif type == "shortterm":
        if context in shortterm.memories:
            if returnMem:
                return shortterm.memories[context]
            else:
                return True
        else:
            return False