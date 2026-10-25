import json
import hashlib
import random
from datetime import datetime
from pathlib import Path

# Simule la base de donnees Cloudflare D1
DB_PATH = Path("genesis_db.json")
PRIMITIVES = ["EXIST", "CAUSE", "PART", "SAME", "ONE", "ALL", "NOT", "IF", "DO", "HAPPEN", "KNOW", "SEE", "BIG", "LIVE", "DIE", "MOVE", "THINK", "SAY", "TRUE", "GOOD"]

def load_db():
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text())
    return {"species": []}

def generate_entity(index, parent_hash=None):
    # Choix de 3 a 5 primitives
    traits = random.sample(PRIMITIVES, k=random.randint(3, 5))
    eq = " AND ".join([f"{t}(x)" for t in traits])
    
    # Deterministic hash based on traits and index
    payload = f"{index}:{eq}:{parent_hash}"
    sha = hashlib.sha256(payload.encode()).hexdigest()
    
    return {
        "id": f"ENTITY_{index:06d}",
        "traits": traits,
        "equation": eq,
        "hash": sha,
        "parent_hash": parent_hash,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "status": "VERIFIABLE"
    }

def run_genesis_cycle(count=10):
    db = load_db()
    existing_count = len(db["species"])
    
    last_hash = db["species"][-1]["hash"] if existing_count > 0 else None
    
    new_entities = []
    for i in range(count):
        idx = existing_count + i + 1
        entity = generate_entity(idx, last_hash)
        new_entities.append(entity)
        last_hash = entity["hash"]
        
    db["species"].extend(new_entities)
    DB_PATH.write_text(json.dumps(db, indent=2))
    
    print(f"[{datetime.utcnow().isoformat()}] Genesis Cycle: {count} new entities generated.")
    for e in new_entities:
        print(f"  -> {e['id']} | {e['equation']} | SHA: {e['hash'][:16]}...")
        
    # Generation du rapport quotidien (These/Antithese/Synthese)
    report_path = Path("../06_DOCS/DAILY_GENESIS_LOG.md")
    with report_path.open("a") as f:
        f.write(f"\n## Genesis Cycle - {datetime.utcnow().strftime('%Y-%m-%d')}\n")
        for e in new_entities:
            f.write(f"- **{e['id']}**: {e['equation']} (Hash: `{e['hash'][:16]}...`)\n")
            
    print(f"Log appended to {report_path}")

if __name__ == "__main__":
    run_genesis_cycle()
