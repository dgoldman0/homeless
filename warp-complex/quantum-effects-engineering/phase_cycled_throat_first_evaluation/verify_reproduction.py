#!/usr/bin/env python3
from pathlib import Path
import hashlib, subprocess, sys
base=Path(__file__).resolve().parent
before={}
for sub in ['stage1_static_wormhole_qi','stage2_dynamic_throat_qi']:
    for p in (base/sub).iterdir():
        if p.suffix in ['.csv','.json','.txt']:
            before[p.relative_to(base)] = hashlib.sha256(p.read_bytes()).hexdigest()
subprocess.check_call([sys.executable, str(base/'stage1_static_wormhole_qi/run_stage1_static_wormhole_qi.py')])
subprocess.check_call([sys.executable, str(base/'stage2_dynamic_throat_qi/run_stage2_dynamic_throat_qi.py')])
failed=[]
for rel,h in before.items():
    p=base/rel
    h2=hashlib.sha256(p.read_bytes()).hexdigest()
    if h2 != h:
        failed.append((str(rel),h,h2))
if failed:
    print('FAILED')
    for row in failed:
        print(row)
    sys.exit(1)
print('All checked generated outputs match their recorded hashes after rerun.')
