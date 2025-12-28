import time
import sys
import os
from kuksa_client.grpc import VSSClient, Datapoint

# --- Configuration ---
BROKER_HOST = os.getenv("BROKER_HOST", "kuksa-databroker")
BROKER_PORT = int(os.getenv("BROKER_PORT", 55555))

# VSS Signals (Standard VSS 5.x paths)
SPEED_SIGNAL = "Vehicle.Speed"
SEAT_POS_SIGNAL = "Vehicle.Cabin.Seat.Row1.Pos1.Position"  # 0-100%

def main():
    print(f"🔄 Connecting to Databroker at {BROKER_HOST}:{BROKER_PORT}...", flush=True)

    with VSSClient(BROKER_HOST, BROKER_PORT) as client:
        
        # --- PHASE 1: PRE-CONDITION (SAFETY CHECK) ---
        print(f"1️⃣  Setting {SPEED_SIGNAL} to 0 (Vehicle Stopped)...", flush=True)
        client.set_current_values({
            SPEED_SIGNAL: Datapoint(0)
        })
        time.sleep(0.5) # Allow signal to propagate
        
        # Verify Speed is 0
        speed_val = client.get_current_values([SPEED_SIGNAL])[SPEED_SIGNAL].value
        if float(speed_val) != 0.0:
            raise RuntimeError(f"❌ Failed to stop vehicle! Speed is {speed_val}")
        print("   ✅ Vehicle is stopped.", flush=True)

        # --- PHASE 2: ACTION (MOVE SEAT) ---
        target_pos = 50
        print(f"2️⃣  Moving Seat ({SEAT_POS_SIGNAL}) to {target_pos}%...", flush=True)
        
        client.set_current_values({
            SEAT_POS_SIGNAL: Datapoint(target_pos)
        })
        time.sleep(1) # Wait for the 'mechanical' movement (simulated)

        # --- PHASE 3: VALIDATION ---
        print("3️⃣  Verifying Seat Position...", flush=True)
        current_values = client.get_current_values([SEAT_POS_SIGNAL])
        
        if SEAT_POS_SIGNAL not in current_values or current_values[SEAT_POS_SIGNAL] is None:
             raise RuntimeError(f"❌ Seat signal {SEAT_POS_SIGNAL} not found in Databroker!")

        actual_pos = current_values[SEAT_POS_SIGNAL].value
        print(f"   📊 Read Position: {actual_pos}%", flush=True)

        if int(actual_pos) == target_pos:
            print("   ✅ SUCCESS: Seat position set correctly!", flush=True)
        else:
            raise RuntimeError(f"❌ FAILURE: Expected {target_pos}, but got {actual_pos}")

if __name__ == "__main__":
    # Retry loop to handle container startup timing
    start_time = time.time()
    timeout_seconds = 30
    
    while time.time() - start_time < timeout_seconds:
        try:
            main()
            sys.exit(0) # Exit with Success
        except Exception as e:
            print(f"⚠️  Test failed: {e}. Retrying in 2s...", flush=True)
            time.sleep(2)
            
    print("❌ All attempts failed. Integration test crashed.")
    sys.exit(1)