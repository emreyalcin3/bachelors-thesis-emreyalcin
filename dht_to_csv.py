import sys, os, csv, time
from datetime import datetime, timezone
import Adafruit_DHT

SENSOR = Adafruit_DHT.DHT22
PIN = 4
SAMPLE_EVERY_SEC = 2
OUT_DIR = "/home/emreyalcin/logs"  

os.makedirs(OUT_DIR, exist_ok=True)
csv_path = os.path.join(OUT_DIR, f"dht22_{datetime.now().strftime('%Y%m%d')}.csv")

new_file = not os.path.exists(csv_path)
f = open(csv_path, "a", newline="")
w = csv.writer(f)
if new_file:
    w.writerow(["timestamp_iso", "temperature_c", "humidity_pct"])

print(f"Logging to {csv_path}. Press Ctrl+C to stop.")

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)

        ts = datetime.now(timezone.utc).astimezone().isoformat()

        if humidity is not None and temperature is not None:
            w.writerow([ts, f"{temperature:.2f}", f"{humidity:.2f}"])
            f.flush()

            print(f"{ts}  Temp: {temperature:.2f} °C  Humidity: {humidity:.2f} %")
        else:
            w.writerow([ts, "", ""])
            f.flush()
            print(f"{ts}  Failed to retrieve sensor data")

        time.sleep(SAMPLE_EVERY_SEC)

except KeyboardInterrupt:
    print("\nProgram stopped")
    f.close()
    sys.exit(0)
except Exception as e:
    print(f"\nError: {e}")
    f.close()
    sys.exit(1)
