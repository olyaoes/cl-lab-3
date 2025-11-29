import random
import time

class TemperatureSensor:
    def __init__(self, cfg):
        self.lat = cfg["lat"]
        self.lng = cfg["lng"]

    def read_data(self):
        return {
            "type": "temperature",
            "value": round(random.uniform(18.0, 32.0), 2),
            "lat": self.lat,
            "lng": self.lng,
            "timestamp": time.time()
        }
