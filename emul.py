import json
import time
import threading
from sensors.temperature_sensor import TemperatureSensor
from sensors.noise_sensor import NoiseSensor
from sensors.light_sensor import LightSensor
from utils.rest_client import send_data


def start_sensor(name, config, sensor_class, stop_event):
    sensor = sensor_class(config)
    interval_ms = config.get("interval_ms")
    if not isinstance(interval_ms, (int, float)) or interval_ms <= 0:
        raise ValueError(f"Invalid or missing 'interval_ms' in config for sensor '{name}'")
    interval = interval_ms / 1000.0

    while not stop_event.is_set():
        data = sensor.read_data()
        data["sensor_name"] = name
        send_data(data)
        if stop_event.wait(interval):
            break


def main():
    try:
        with open("config.json") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        print("Error: 'config.json' file not found.")
        return
    except json.JSONDecodeError:
        print("Error: 'config.json' contains invalid JSON.")
        return

    sensor_cfg = cfg.get("sensors", cfg)

    sensor_types = [
    ("temperature", TemperatureSensor),
    ("pressure", PressureSensor),
    ("humidity", HumiditySensor)
]

    threads = []
    stop_event = threading.Event()

    for name, cls in sensor_types:
        conf = sensor_cfg.get(name)
        if conf is None:
            print(f"Warning: no config for sensor '{name}', skipping.")
            continue
        t = threading.Thread(target=start_sensor, args=(name, conf, cls, stop_event), daemon=True)
        threads.append(t)
        t.start()

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(0.5)
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        stop_event.set()
        for t in threads:
            t.join()


if __name__ == "__main__":
    main()
