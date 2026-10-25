#!/usr/bin/env python3
"""Generate a static JSON status file for all OTS proofs."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = ROOT / "00_MANIFEST"
OUT = ROOT / "07_PUBLICATION" / "website" / "public" / "ots_status.json"

def check_proof(ots_path):
    try:
        # Timeout de 3 secondes pour éviter de bloquer si le réseau est lent
        out = subprocess.run(
            ["ots", "verify", str(ots_path)],
            capture_output=True, text=True, timeout=3
        ).stdout
        if "Bitcoin block" in out:
            return {"status": "confirmed", "detail": out.strip()}
        if "Pending" in out:
            return {"status": "pending", "detail": "Awaiting Bitcoin confirmation"}
        return {"status": "unknown", "detail": out.strip()}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "detail": "Network timeout checking OTS"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def main():
    results = {}
    for ots in sorted(MANIFEST_DIR.glob("*.ots")):
        results[ots.name] = check_proof(ots)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))
    print(f"wrote {OUT} ({len(results)} proofs)")

if __name__ == "__main__":
    main()
