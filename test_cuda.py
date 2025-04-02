import torch
import sys

try:
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device count: {torch.cuda.device_count()}")
        print(f"CUDA device name: {torch.cuda.get_device_name(0)}")
        total_memory = torch.cuda.get_device_properties(0).total_memory
        print(f"Total memory: {total_memory / (1024 ** 3):.2f} GB")

        # Try to allocate 10GB
        x = torch.zeros(1024 * 1024 * 1024 * 10 // 4, dtype=torch.float)
        x = x.cuda()
        print("Successfully allocated 10GB on CUDA")
        del x
        torch.cuda.empty_cache()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

