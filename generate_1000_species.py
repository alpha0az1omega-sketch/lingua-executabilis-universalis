import json
import hashlib
import random
from pathlib import Path

def generate_1000_species():
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    out_dir = root / "04_ARTIFACTS" / "species_3d"
    out_dir.mkdir(parents=True, exist_ok=True)

    primitives = ["EXIST", "SAME", "ONE", "ALL", "NOT", "IF", "TRUE", "CAUSE", "PART", "BIG", "DO", "HAPPEN", "MOVE", "KNOW", "SEE", "THINK", "SAY", "LIVE", "DIE", "GOOD"]
    types = ["animal", "plant", "human", "concept", "element"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    for i in range(1000):
        sp_id = f"species_{i:04d}"
        name = f"Organism-{i:04d}"
        sp_type = random.choice(types)
        
        # Choisir 3 à 5 traits aléatoires
        traits = random.sample(primitives, k=random.randint(3, 5))
        
        # Construire une équation factice
        eq = " AND ".join([f"{t}({sp_id})" for t in traits[:2]])
        
        color = random.choice(colors)
        freq = random.randint(100, 1000)
        real_sha = hashlib.sha256(f"{sp_id}:{eq}".encode()).hexdigest()

        # (Le code HTML 3D est le même que précédemment, on l'injecte ici)
        # ... (je garde le HTML court pour l'exemple, il faut réutiliser le template complet)
        html = f"<html><body style='background:#1a1a1a;color:{color};font-family:monospace;'><h1>{name} ({sp_type})</h1><p>Equation: {eq}</p><p>SHA: {real_sha}</p></body></html>"
        
        (out_dir / f"{sp_id}.html").write_text(html)
        
    print(f"1000 espèces générées dans {out_dir}")

if __name__ == "__main__":
    generate_1000_species()
