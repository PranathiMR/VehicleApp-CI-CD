import time
import sys
import os
from kuksa_client.grpc import VSSClient, Datapoint

BROKER_HOST = os.getenv("BROKER_HOST", "localhost")
BROKER_PORT = int(os.getenv("BROKER_PORT", 55555))
SPEED_PATH = "Vehicle.Speed"

def main():
    print(f"Connecting to {BROKER_HOST}:{BROKER_PORT}...", flush=True)

    # Use 'with' context manager to handle connection automatically
    with VSSClient(BROKER_HOST, BROKER_PORT) as client:
        
        # 1. READ
        print(f"Reading {SPEED_PATH}...", flush=True)
        current_values = client.get_current_values([SPEED_PATH])
        
        if SPEED_PATH in current_values and current_values[SPEED_PATH] is not None:
            print(f"Current speed = {current_values[SPEED_PATH].value}", flush=True)
        else:
            print("Speed is currently None (not set).", flush=True)

        # 2. WRITE
        print("Setting speed = 0...", flush=True)
        client.set_current_values({
            SPEED_PATH: Datapoint(0)
        })
        
        # Allow a tiny pause for the broker to process (optional but safe)
        time.sleep(0.5)

        # 3. VERIFY
        print("Verifying new speed...", flush=True)
        updated_values = client.get_current_values([SPEED_PATH])
        new_speed = updated_values[SPEED_PATH].value
        
        print(f"New speed read from broker: {new_speed}", flush=True)

        if float(new_speed) != 0.0:
            raise RuntimeError(f"Failed to set speed! Got {new_speed}")

        print("✅ Phase 2 integration test PASSED", flush=True)

if __name__ == "__main__":
    # Simple retry loop for the whole script logic
    for attempt in range(5):
        try:
            main()
            sys.exit(0) # Exit success
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    
    print("❌ All attempts failed.")
    sys.exit(1)