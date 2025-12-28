import time
import sys
from kuksa_client import KuksaClient

BROKER = "kuksa-databroker"
PORT = 55555

SIGNAL = "Vehicle.Cabin.Seat.Row1.PosX"

def fail(msg):
    print(f"❌ {msg}")
    sys.exit(1)

def ok(msg):
    print(f"✅ {msg}")

print("Connecting to Kuksa Databroker...")

client = KuksaClient(host=BROKER, port=PORT)
client.connect()

# Write value
ok("Writing seat position")
client.set_value(SIGNAL, 42)

time.sleep(1)

# Read value
value = client.get_value(SIGNAL)

if value != 42:
    fail(f"Expected 42, got {value}")

ok("Seat position updated correctly")
ok("INTEGRATION TEST PASSED")

client.disconnect()
sys.exit(0)
