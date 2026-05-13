#!/usr/bin/env python3
from pathlib import Path
from run_stage1_radial_nulls import run_stage1
from run_stage2_bundle_screen import run_stage2

def main():
    root = Path(__file__).resolve().parents[1]
    data = root/"data"
    run_stage1(data)
    run_stage2(data)
    print(f"Wrote data products to {data}")
if __name__ == "__main__":
    main()
