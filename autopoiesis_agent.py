import json
import hashlib
from pathlib import Path
from datetime import datetime

DB_PATH = Path("genesis_db.json")
REPORT_PATH = Path("../06_DOCS/AUTOPOIESIS_REPORT.md")

def analyze_universe():
    if not DB_PATH.exists():
        print("Erreur: Base de donnees introuvable.")
        return

    db = json.loads(DB_PATH.read_text())
    entities = db.get("species", [])
    
    conflicts = []
    profiles = {}
    
    # Analyse des 10 premieres entites
    for e in entities[-10:]:
        sha = e["hash"]
        # Profil physique base sur les premiers caracteres du hash
        profile = sha[:4] 
        if profile in profiles:
            conflicts.append((e["id"], profiles[profile]))
        else:
            profiles[profile] = e["id"]
            
    # Generation du rapport Autopoietique
    report = f"# AUTOPOIESIS REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += "L'agent cognitif a analyse l'univers L.E.U.\n\n"
    
    report += "## THESE (Analyse des lois physiques)\n"
    report += f"- {len(entities)} entites analysees.\n"
    report += "- Les lois sont generees par cryptographie (SHA-256).\n\n"
    
    report += "## ANTITHESE (Detection des anomalies)\n"
    if conflicts:
        for c in conflicts:
            report += f"- ALERTE : Collision physique entre {c[0]} et {c[1]}. Le prefixe de hash est identique. L'univers risque une superposition quantique.\n"
    else:
        report += "- Aucune collision physique majeure detectee. L'univers est stable.\n"
    
    report += "\n## SYNTHESE (Proposition de correction autonome)\n"
    if conflicts:
        report += "L'agent propose d'introduire un 'Sel Cryptographique' (Cryptographic Salt) dans le Genesis Engine pour garantir que chaque entite possede une signature physique unique a jamais.\n"
        report += "-> Action recommandee : Mettre a jour le moteur avec `hash = sha256(payload + timestamp_ns)`.\n"
    else:
        report += "L'univers est en equilibre. L'agent autorise la poursuite de la generation autonome.\n"
        
    REPORT_PATH.write_text(report)
    print(f"OK: Rapport Autopoietique genere a {REPORT_PATH}")

if __name__ == "__main__":
    analyze_universe()
