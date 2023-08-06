
from qantio.sdk.public.exceptions import GeographyPointException

class GeographyPoint():
    latitude    : float = 0
    longitude   : float = 0
    elevation   : int   = 0
    
    def __init__(self, latitude:float, longitude:float, elevation:float=0):
        
        if(latitude>90 or latitude<-90):
            raise GeographyPointException("latitude", latitude, "(-90, 90)")

        if(longitude>180 or longitude<-180):
            raise GeographyPointException("longitude", longitude, "(-180, 180)")

        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation