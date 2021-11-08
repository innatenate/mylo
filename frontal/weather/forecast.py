import requests
import datetime
import calendar
import time
from uni import functions as uni

secondaryData = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/73724?unitGroup=us&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"
secondaryDataPulled = None
weatherData = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/74012?unitGroup=us&key=BHFCCKY362XGLDYMK3FRKYZHB&include=fcst%2Cstats%2Calerts%2Ccurrent"
weatherDataPulled = None

def tagPressure(day):
    higherAverage = 1017
    highestAverage = 1020
    lowerAverage = 1013
    lowestAverage = 1009
    average = 1015

    if day['details']['pressure'] >= highestAverage:
        day['tags']['pressure'] = "very high"
    elif day['details']['pressure'] < highestAverage and day['details']['pressure'] > higherAverage:
        day['tags']['pressure'] = 'high'
    elif day['details']['pressure'] <= higherAverage and day['details']['pressure'] > lowerAverage:
        day['tags']['pressure'] = 'average'
    elif day['details']['pressure'] <= average and day['details']['pressure'] > lowestAverage:
        day['tags']['pressure'] = 'low'
    elif day['details']['pressure'] <= lowestAverage:
        day['tags']['pressure'] = 'very low'

    return day

def tagWind(day):
    if day['details']['windspeed'] >= 0 and day['details']['windspeed'] < 10:
        day['tags']['windspeed'] = 'low'
    if day['details']['windspeed'] >= 10 and day['details']['windspeed'] < 15:
        day['tags']['windspeed'] = 'medium'
    if day['details']['windspeed'] >= 15:
        day['tags']['windspeed'] = 'high'
    
    return day

def tagHumidity(day):
    if day['details']['humidity'] >= 80:
        day['tags']['humidity'] = 'high'
    elif day['details']['humidity'] >= 50 and day['details']['humidity'] < 80:
        day['tags']['humidity'] = 'medium'
    elif day['details']['humidity'] >= 20 and day['details']['humidity'] < 50:
        day['tags']['humidity'] = 'low'
    elif day['details']['humidity'] < 20:
        day['tags']['humidity'] = 'none'

    return day

def tagCloudiness(day):
    if day['details']['clouds'] >= 80:
        day['tags']['clouds'] = 'high'
    elif day['details']['clouds'] >= 50 and day['details']['clouds'] < 80:
        day['tags']['clouds'] = 'medium'
    elif day['details']['clouds'] >= 20 and day['details']['clouds'] < 50:
        day['tags']['clouds'] = 'low'
    elif day['details']['clouds'] < 20:
        day['tags']['clouds'] = 'none'
    
    return day

def tagPossibleFront(day): ## Reinput for different location
    if day['tags']['pressure'] == "very high" or day['tags']['pressure'] == 'high':
        if day['tags']['windspeed'] == "none" or day['tags']['windspeed'] == 'low':
            day['tags']['fronts'] == "possible high resting"
        if day['tags']['windspeed'] == "medium" or day['tags']['windspeed'] == 'high':
            if day['details']['winddir'] == 'E' or day['details']['winddir'] == 'SE':
                day['tags']['fronts'] == 'possible high entering'
            elif day['details']['winddir'] == 'SW' or day['details']['winddir'] == 'S' or day['details']['winddir'] == 'E':
                day['tags']['fronts'] == 'possible high leaving'
            else:
                day['tags']['fronts'] == 'possible high leaving'
    if day['tags']['pressure'] == "very low" or day['tags']['pressure'] == 'low':
        if (day['tags']['windspeed'] == "none" or day['tags']['windspeed'] == 'low') or (day['tags']['pressure'] == "very low" and day['tags']['windspeed'] == 'high'):
            day['tags']['fronts'] == 'possible low resting'
        if day['tags']['windspeed'] == "medium" or day['tags']['windspeed'] == 'high':
            if day['details']['winddir'] == 'E' or day['details']['winddir'] == 'NE':
                day['tags']['fronts'] == 'possible low entering'
            elif day['details']['winddir'] == 'SW' or day['details']['winddir'] == 'S':
                day['tags']['fronts'] == 'possible low leaving'
            else:
                day['tags']['fronts'] == 'possible low leaving'
    if day['details']['pressure'] == 'average':
        if day['tags']['windspeed'] == 'none' or day['tags']['windspeed'] == 'low':
            day['tags']['fronts'] == 'possible high entering'
        elif day['tags']['windspeed'] == 'medium' or day['tags']['windspeed'] == 'high':
            day['tags']['fronts'] == 'possible low entering'
        else:
            day['tags']['fronts'] == 'inclusive or standstill'

def checkForAlerts(day):
    pass

def checkForSystems(week, week2):
    pass

def convWindDirection(day):
    degree = day['details']['winddir']
    if (degree>337.5): return 'N'
    if (degree>292.5): return 'NW'
    if(degree>247.5): return 'W'
    if(degree>202.5): return 'SW'
    if(degree>157.5): return 'S'
    if(degree>122.5): return 'SE'
    if(degree>67.5): return 'E'
    if(degree>22.5): return 'NE'
    return 'N'


def parseForecast(day, parse, forecastType='singular'):

    if type(day) is list:
        print(repr(day))
        raise Exception("Improper use of parseForecast. You might want parseForecasts instead.")

    day = {
        'details': {
            'preciptype': day['preciptype'] or None,
            'humidity': day['humidity'] or 0,
            'pressure': day['pressure'],
            "maxtemp": day['tempmax'],
            'mintemp': day['tempmin'],
            'clouds': day['cloudcover'] or 0,
            "temp": day['temp'],
            'dew': day['dew'] or 0,
            'uv': day['uvindex'] or 0,
            'dayname': day['datetimeEpoch'],
            'fl': day['feelslike'],                
            'desc': day['description'],
            'conds': day['conditions'],
            'winddir': day['winddir'],
            'windspeed': day['windspeed'],
            'precipprob': day['precipprob'],
            'severerisk': day['severerisk'] or 0,
        },
        'tags': {}
    }

    direc = convWindDirection(day)
    day['details']['winddir'] = direc
    day = tagPressure(day)
    day = tagWind(day)
    day = tagHumidity(day)
    day = tagCloudiness(day)
    day = tagPossibleFront(day)
    dayName = time.strftime('%A', time.localtime(day['dayname']))
    day['dayname'] = dayName
    
    if forecastType == "multiple":
        return day

    elif forecastType == "singular":
        beg = ""
        notes = ""
        phrasing = ""
        info = ""
        end = ""

        if (day['tags']['pressure'] == "average" or day['tags']['pressure'] == "low" or day['tags']['pressure'] == "high") and day['tags']['windspeed'] == 'low':
            if (day['tags']['pressure'] == 'high' or day['tags']['pressure'] == "average") and (day['tags']['clouds'] == "none" or day['tags']['clouds'] == "low"):
                beg = uni.decision([
                    f"Today seems fairly {uni.decision(['tame', 'clement', 'pacified', 'balmy', 'pleasant', 'refreshing'])}. The average barometric pressure is average, and clouds are minimal.",
                    f"I am expecting a {uni.decision(['tame', 'clement', 'pacified', 'balmy', 'pleasant', 'refreshing'])} day. There is very little cloud coverage and the atmospheric pressure is average.",
                    f"For today, I'm already noticing very little cloud coverage and an average barometric pressure - both indicators of a {uni.decision(['tame', 'clement', 'pacified', 'balmy', 'pleasant', 'refreshing'])} day.",
                ])
            elif (day['tags']['pressure'] == "average" or day['tags']['pressure'] == "low") and (day['tags']['clouds'] == 'medium' or day['tags']['clouds'] == "high"): 
                beg = uni.decision([
                    "For today, I've noticed a rather low barometric pressure and a decent amount of cloud coverage. You should expect inclement weather soon.",
                    "Seems like barometric pressure is pretty low today. On top of that, there's plenty of cloud coverage.",
                    "I've noticed barometric pressure is rather low and there is a rife coverage of clouds today.",
                ])
    
        elif (day['tags']['pressure'] == "average" or day['tags']['pressure'] == "low" or day['tags']['pressure'] == "high") and (day['tags']['windspeed'] == 'medium' or day['tags']['windspeed'] == 'high'):
            if (day['tags']['pressure'] == 'high' or day['tags']['pressure'] == "average") and (day['tags']['clouds'] == "none" or day['tags']['clouds'] == "low"):
                beg = uni.decision([
                    f"Wind speeds are rather high today, as well as the barometric pressure. There could be a low pressure front moving in soon.",
                    f"For today, I've noticied that there's a spike in barometric pressure as well as wind speeds. This could indicate a low pressure front moving in shortly.",
                    f"Seems like wind speeds and barometric pressure have spiked today. I would anticipate inclement weather tomorrow or the following day. ",
                ])
            elif (day['tags']['pressure'] == "average" or day['tags']['pressure'] == "low") and (day['tags']['clouds'] == 'medium' or day['tags']['clouds'] == "high"): 
                beg = uni.decision([
                    "I'm expecting inclement weather today or soon. Barometric pressure is rather low and there's a rife coverage of clouds.",
                    "I've noticied a spike in wind speeds and cloud coverage as well as a decrease in barometric pressure. You should expect precipitation today or tomorrow.",
                    "The atmosphere is turbulent today, with wind speeds and cloud coverage being rather high and barometric pressure being rather low.",
                ])
    
        if len(beg) > 0 and len(notes) > 0:
            notes = uni.decision(["Additionally, ", "Furthermore, ", "Also, "]) + notes
        

def parseForecasts(week, week2, parse):
    pass



def processForecast(type, parse=True):
    global weatherDataPulled
    global secondaryDataPulled

    weatherDataPulled = requests.get(weatherData).json()
    secondaryDataPulled = requests.get(secondaryData).json()
    week = None
    day = None

    if type == "7day":
        week = [weatherDataPulled['days'][0], weatherDataPulled['days'][1], weatherDataPulled['days'][2], weatherDataPulled['days'][3], weatherDataPulled['days'][4], weatherDataPulled['days'][5], weatherDataPulled['days'][6]]        
        week2 = [secondaryDataPulled['days'][0], secondaryDataPulled['days'][1], secondaryDataPulled['days'][2], secondaryDataPulled['days'][3], secondaryDataPulled['days'][4], secondaryDataPulled['days'][5], secondaryDataPulled['days'][6]]        
    elif type == "5day":
        week = [weatherDataPulled['days'][0], weatherDataPulled['days'][1], weatherDataPulled['days'][2], weatherDataPulled['days'][3], weatherDataPulled['days'][4]]
        week2 = [secondaryDataPulled['days'][0], secondaryDataPulled['days'][1], secondaryDataPulled['days'][2], secondaryDataPulled['days'][3], secondaryDataPulled['days'][4]]
    elif type == "1day":
        day = weatherDataPulled['days'][0]
    elif type == "current":
        day = weatherDataPulled['currentConditions']

    if week is not None:
        newWeek = []
        newSecondWeek = []
        for day in week:
            ret = parseForecast(day, parse, 'multiple')
            newWeek.append(ret)
        for day in week2:
            ret = parseForecast(day, parse, 'multiple')
            newSecondWeek.append(ret)
        ret = parseForecasts(newWeek, newSecondWeek, parse)
    else:
        day = parseForecast(day, parse, 'singular')
