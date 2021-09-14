from datetime import datetime, timedelta

class Geolocation:
    def __init__(self, dic):
        self.dic = dic
        self.latitude = dic['latitude']
        self.longtitude = dic['longtitude']
    '''def __str__(self):
        return '{},{}'.format(self.latitude, self.longtitude)'''

class Location:
    def __init__(self, dic):
        self.dic = dic
        self.city = dic['city']
        self.state = dic['state']    
    '''def __str__(self):
        return '{},{}'.format(self.city, self.state)'''

class Zipcode:
    def __init__(self, dic):
        self.dic = dic
        self.zipcode = dic['zipcode']
        self.city = Location(dic).city
        self.state = Location(dic).state
        self.latitude = Geolocation(dic).latitude
        self.longtitude = Geolocation(dic).longtitude
        self.timezone_diff = dic['timezoneDiff']
        self.dls_bool = dic['observeDaylightSavings']
        #current time = utcnow() + timedelta(hours = time difference) utc time has the same number of the time in G.M.T
        self.current_time = str(format(datetime.utcnow() + timedelta(hours = self.timezone_diff), '%H:%M:%S'))
    def __str__(self):
        return 'zipcode: {}, city: {}, state: {}, latitude: {}, longitude: {}, timezoneDiff: {}, observeDaylightSavings: {}, currentTime: {}'.format(self.zipcode, self.city, self.state, self.latitude, self.longtitude, self.timezone_diff, self.dls_bool, self.current_time)
