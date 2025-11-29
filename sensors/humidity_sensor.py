import random
import time

class HumiditySensor:
    def __init__(self, cfg):
        self.lat = cfg["lat"]
        self.lng = cfg["lng"]

    def read_data(self):
        return {
            "type": "humidity",
            "value": round(random.uniform(30.0, 90.0), 2), 
            "unit": "%",
            "lat": self.lat,
            "lng": self.lng,
            "timestamp": time.time()
        }
