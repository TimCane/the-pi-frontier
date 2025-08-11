# This file runs before main.py
import gc
import machine

# Enable garbage collection
gc.enable()

# Set CPU frequency (optional)
# machine.freq(125000000)  # 125MHz

print("Boot sequence complete")