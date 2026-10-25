import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEXICON = json.loads((ROOT / "01_SPECIFICATION" / "primitive_lexicon.json").read_text())
NFT_DIR = ROOT / "07_PUBLICATION" / "nft_mint"
META_DIR = NFT_DIR / "metadata"
MEDIA_DIR = NFT_DIR / "media"

META_DIR.mkdir(parents=True, exist_ok=True)
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Dictionnaire simplifié des glyphes (pour l'exemple, on utilise des formes basiques)
# Dans un vrai projet, on utiliserait le script build_atlas.py pour extraire les vrais SVG
GLYPHS = {
    "EXIST": '<circle cx="50" cy="50" r="30" fill="#1f77b4"/>',
    "CAUSE": '<line x1="20" y1="50" x2="80" y2="50" stroke="#d62728" stroke-width="6" marker-end="url(#arrow)"/>',
    "PART": '<circle cx="50" cy="50" r="30" fill="none" stroke="#2ca02c" stroke-width="4"/><circle cx="50" cy="50" r="12" fill="#2ca02c"/>',
    "SAME": '<rect x="20" y="35" width="25" height="30" fill="#9467bd"/><rect x="55" y="35" width="25" height="30" fill="#9467bd"/>',
    "ONE": '<circle cx="50" cy="50" r="10" fill="#8c564b"/>',
    "ALL": '<rect x="25" y="25" width="50" height="50" fill="#e377c2"/>',
    "NOT": '<circle cx="50" cy="50" r="30" fill="none" stroke="#7f7f7f" stroke-width="4"/><line x1="28" y1="72" x2="72" y2="28" stroke="#7f7f7f" stroke-width="4"/>',
    "IF": '<polygon points="50,20 80,50 50,80 20,50" fill="none" stroke="#bcbd22" stroke-width="4"/>',
    "DO": '<circle cx="50" cy="50" r="25" fill="#17becf"/>',
    "HAPPEN": '<path d="M20,50 Q35,30 50,50 T80,50" fill="none" stroke="#ff7f0e" stroke-width="4"/>',
    "KNOW": '<ellipse cx="50" cy="50" rx="35" ry="20" fill="none" stroke="#1f77b4" stroke-width="4"/><circle cx="50" cy="50" r="8" fill="#1f77b4"/>',
    "SEE": '<polygon points="50,20 80,70 20,70" fill="none" stroke="#2ca02c" stroke-width="4"/><circle cx="50" cy="55" r="8" fill="#2ca02c"/>',
    "BIG": '<circle cx="50" cy="50" r="40" fill="#d62728"/>',
    "LIVE": '<path d="M50,20 C80,30 80,70 50,80" fill="none" stroke="#2ca02c" stroke-width="4"/>',
    "DIE": '<path d="M50,20 C80,30 80,70 50,80 L55,85" fill="none" stroke="#7f7f7f" stroke-width="4"/>',
    "MOVE": '<path d="M20,50 Q50,20 80,50" fill="none" stroke="#17becf" stroke-width="6" marker-end="url(#arrow)"/>',
    "THINK": '<circle cx="35" cy="50" r="15" fill="none" stroke="#9467bd" stroke-width="4"/><circle cx="65" cy="50" r="15" fill="none" stroke="#9467bd" stroke-width="4"/><line x1="45" y1="50" x2="55" y2="50" stroke="#9467bd" stroke-width="4"/>',
    "SAY": '<rect x="20" y="35" width="60" height="30" fill="none" stroke="#ff7f0e" stroke-width="4"/><polygon points="40,65 50,80 60,65" fill="#ff7f0e"/>',
    "TRUE": '<circle cx="50" cy="50" r="30" fill="none" stroke="#1f77b4" stroke-width="4"/><circle cx="50" cy="50" r="18" fill="none" stroke="#1f77b4" stroke-width="4"/>',
    "GOOD": '<circle cx="50" cy="50" r="30" fill="none" stroke="#2ca02c" stroke-width="4"/><line x1="35" y1="50" x2="65" y2="50" stroke="#2ca02c" stroke-width="4"/><line x1="50" y1="35" x2="50" y2="65" stroke="#2ca02c" stroke-width="4"/>'
}

def generate():
    count = 0
    for p in LEXICON["primitives"]:
        pid = p["id"]
        layer = p["layer"]
        formal = p["formal"]
        
        # 1. Générer le SVG
        glyph_svg = GLYPHS.get(pid, '<circle cx="50" cy="50" r="30" fill="#ccc"/>')
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6" fill="#d62728"/></marker></defs>
<rect width="100" height="100" fill="#fafafa"/>
{glyph_svg}
</svg>'''
        svg_path = MEDIA_DIR / f"{pid}.svg"
        svg_path.write_text(svg_content)
        
        # 2. Générer le JSON (Métadonnées)
        metadata = {
            "name": f"L.E.U. Glyph - {pid}",
            "description": f"Genesis Glyph of Lingua Executabilis Universalis. Layer {layer}. Formal: {formal}.",
            "image": f"ipfs://PLACEHOLDER/{pid}.svg",
            "attributes": [
                {"trait_type": "Primitive", "value": pid},
                {"trait_type": "Layer", "value": layer},
                {"trait_type": "Formal Expression", "value": formal}
            ]
        }
        json_path = META_DIR / f"{pid}.json"
        json_path.write_text(json.dumps(metadata, indent=2))
        
        count += 1
        print(f"Généré : {pid} (SVG + JSON)")

    print(f"\nTerminé ! {count} NFT préparés dans {NFT_DIR}")

if __name__ == "__main__":
    generate()
