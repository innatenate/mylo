from frontal.uni import functions
from temporal import induct
from temporal import grab
from stem import callosum
from frontal.memory import activequeries

import datetime
from serpapi import GoogleSearch

queries = []
serpkey = ""
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
                             f"The time now is {now.strftime('%I:%M %p')}",
                             now.strftime('%I:%M %p'),
                             f"It is currently {now.strftime('%I:%M %p')}"])
    callosum.lastProcessed = {"phrase":phrase, "type":"basic"}
    return True

def repeatFunction(keywords, literal, profile):
    phrase = grab.requestMemory(type='shortterm',context=f'lastProcessed{profile["info"]["prefname"]}', returnMem=True)
    phrase = phrase['phrase']
    beginning = functions.decision([
        "To repeat, I said ",
        "I said, ",
        "What I was saying was, ",
        "Yeah. I can repeat that. What I was saying was, ",
        "What I said was, ",
        "What I had said was, "
    ])
    phrase = beginning + phrase
    callosum.lastProcessed = {"phrase":phrase, "type":"basic"}
    return True

def dateFunction(keywords, literal, profile):
    now = datetime.datetime.now()
    phrase = functions.decision([
        f"The current date is {now.strftime('%A, %B %d, %Y')}.",
        f"Today is {now.strftime('%A, %B %d, %Y')}",
        f"Today's date is {now.strftime('%A, %B %d, %Y')}.",
        f"The date for today is {now.strftime('%A, %B %d, %Y')}."])
    callosum.lastProcessed = {"phrase":phrase, "type":"basic"}
    return True

def howFunction(keywords, literal, profile):
    decide = functions.decision([
        'adroit',
        'concomitant',
        'effulgent',
        'good',
        'fair',
        'excellent',
        'A1',
        'swell',
    ])
    phrase = functions.decision([
        f"I'm feeling {decide}. How about you?",
        f"I'm feeling pretty {decide}. How about you?",
        f"I think I feel {decide}. How about yourself?",
        f"Not too bad, {profile['info']['name']}. How about yourself?",
        f"I feel pretty {decide}, {profile['info']['name']}. How about you?",
        f"I feel {decide}. How about you, {profile['info']['name']}?"
    ])
    query = {
        'keys':['good', 'fair', 'excellent', 'great', 'thanks', 'thank', 'wonderful', 'you'],
        'func': None,
        'type': 'key-specific',
    }
    def sendQuery(keywords, literal, profile):
        if 'thank' in keywords or 'thanks' in keywords:
            phrase = functions.decision([
                f'Glad to hear it, {profile["info"]["name"]}. If you need anything, just let me know.',
                f'Good to hear, {profile["info"]["name"]}. If you need anything, just ask me.',
                f'If you need anything {profile["info"]["name"]}, just let me know.'
            ])
        else:
            phrase = functions.decision([
                'Good to hear. Talk to me if you need anything.',
                'Glad to hear it. If you need anything, just let me know.',
                'Good to hear. If you need anything, just let me know.'
            ])
        callosum.lastProcessed = {"phrase":phrase, "type":"basic"}
        return True
    query['func'] = sendQuery
    activequeries.add(query, profile['info']['name'])
    callosum.lastProcessed = {"phrase":phrase, "type":"query"}
    return True

def searchFunction(keywords, literal, profile):
    literal = literal.replace("search", "")
    parms = {
        "engine": "google",
        "q": literal,
        "api_key": serpkey,
        "location": "Broken Arrow"
    }
    result = GoogleSearch(parms)
    result = result.get_dict()
    result = result['organic_results']
    if "answer_box" in result:
        rbt = result['answer_box']['type']
        if "population_result" == rbt:
            result = {'type': rbt, 'result': result['answer_box']['population']}
        elif 'google_flights' == rbt:
            results = []
            for flight in result['answer_box']['flights']:
                results.append(result['answer_box']['flights'][flight]['flight_info'])
            result = {'type': rbt, 'result': results}
        elif 'hotels' == rbt:
            results = []
            for hotel in result['answer_box']['hotels']:
                results.append(result['answer_box']['hotels'][hotel])
            result = {'type': rbt, 'result': results}
        elif "dictionary_results" == rbt:
            if len(result['answer_box']['definitions']) > 1:
                results = []                
                for term in result['answer_box']['definitions']:
                    results.append(result['answer_box']['definitions'][term])
                result = {'type':rbt, 'result':results}
        elif "organic_result" == rbt and "list" in result['answer_box']:
                results = []                
                for item in result['answer_box']['list']:
                    results.append(result['answer_box']['list'][item])
                result = {'type':rbt, 'result':results}  
        elif "organic_result" == rbt and "answer" in result['answer_box']:
            if 'snippet' in result['answer_box']:
                result = {'type':rbt, 'result':result['answer_box']['answer'], 'moreinfo': result['answer_box']['snippet']}
            else:
                result = {'type':rbt, 'result':result['answer_box']['answer']}
        elif 'result' in result['answer_box']:
            result = result['answer_box']['result']
        else:
            result = "none"
    elif "knowledge_graph" in result:
        if 'description' in result['knowledge_graph']: 
            result = {'type':'knowledge_graph', 'result': result['knowledge_graph']['description']}
        else:
            result = "none"


def addGroceryFunction(keywords, literal, profile):
    ##https://serpapi.com/walmart-search-api

time = Query(queryName="time", queryKeys=["what time is it", "what is the time", "what time", "what the time"], require=["time"])
time.func = timeFunction
queries.append(time)

repeat = Query(queryName="repeat", queryKeys=["could you repeat that", "what did you say", "what was that", "i couldnt hear you", "repeat that please", "will you repeat that", "i didnt hear that"])
repeat.func = repeatFunction
queries.append(repeat)

date = Query(queryName="date", queryKeys=["what year is it", "what is the year", "what is the month", "what month is it", "what is todays date", "what is the date", "what date", "what is today date", "what is the date for today"], require=["date", "year", "month"])
date.func = dateFunction
queries.append(date)

how = Query(queryName="how", queryKeys=["how are you", "whats up", "how you", "how have you been", "hows everything", "whats going on"])
how.func = howFunction
queries.append(how)

def process(literal, profileInfo, override=False):
    for obj in queries:
        print(obj)
        success = obj.grade(literal, profileInfo, override)
        if success:
            return True