import random
import time

class PressureSensor:
    def __init__(self, cfg):
        self.lat = cfg["lat"]
        self.lng = cfg["lng"]

    def read_data(self):
        return {
            "type": "pressure",
            "value": round(random.uniform(980.0, 1040.0), 2),  # hPa
            "unit": "hPa",
            "lat": self.lat,
            "lng": self.lng,
            "timestamp": time.time()
        }
