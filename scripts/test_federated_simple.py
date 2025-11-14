"""
Simple test script to verify federated learning setup
"""
import subprocess
import sys
import time
from pathlib import Path

print("Testing federated learning setup...")
print("=" * 60)

# Test 1: Check data split
print("\n1. Checking data split...")
try:
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from flower_client.data_loader import DataLoaderClient
    
    for client_id in [1, 2, 3]:
        loader = DataLoaderClient(client_id, "output")
        df = loader.load_data()
        print(f"   Client {client_id}: {len(df)} samples (patient IDs {loader.start_idx+1}-{loader.end_idx})")
    print("   OK: Data split verified")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Check model import
print("\n2. Checking model import...")
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "flower_server"))
    from model import InsuranceCostModel
    model = InsuranceCostModel(input_size=17)
    print(f"   OK: Model created with {sum(p.numel() for p in model.parameters())} parameters")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check data loading
print("\n3. Testing data loading...")
try:
    loader = DataLoaderClient(1, "output")
    train_loader, val_loader = loader.get_data_loaders(batch_size=32)
    print(f"   OK: Train batches: {len(train_loader)}, Val batches: {len(val_loader)}")
    
    # Get one batch
    features, targets = next(iter(train_loader))
    print(f"   OK: Batch shape: features {features.shape}, targets {targets.shape}")
except Exception as e:
    print(f"   ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Setup test completed!")
print("\nTo run federated learning:")
print("  python scripts/run_federated_local.py")

