#!/usr/bin/env python3
# Rebuild paper figures from compact CSV data.
from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
print("Compact data tables live in", ROOT/"data")
print("The shipped figures were generated from these CSV summaries.")
