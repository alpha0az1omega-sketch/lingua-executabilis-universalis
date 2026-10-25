import re
from pathlib import Path

def generate_glyph_logo():
    width, height = 800, 800
    cx, cy = width / 2, height / 2
    radius = 300
    
    # Dossier contenant les 20 SVG (ceux que vous venez de générer)
    media_dir = Path("07_PUBLICATION/nft_mint/media")
    glyphs = sorted(media_dir.glob("*.svg"))
    
    if len(glyphs) < 20:
        print(f"Attention : Seulement {len(glyphs)} glyphes trouvés dans {media_dir}")
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#1a1a2e"/>',
        # Groupe rotatif
        '<g>',
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="20s" repeatCount="indefinite"/>'
    ]
    
    import math
    
    for i, glyph_path in enumerate(glyphs):
        angle = (2 * math.pi * i) / len(glyphs)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        
        # Lire le contenu du SVG
        content = glyph_path.read_text()
        
        # Extraire uniquement ce qu'il y a entre <svg> et </svg>
        match = re.search(r'<svg[^>]*>(.*?)</svg>', content, re.DOTALL)
        if match:
            inner_content = match.group(1)
            # Positionner le glyphe (centré sur x, y)
            # On utilise un groupe avec translation
            svg.append(f'<g transform="translate({x - 50}, {y - 50})">')
            svg.append(inner_content)
            svg.append('</g>')
    
    svg.append('</g>')
    
    # Le symbole Omega au centre (statique)
    svg.append(f'<text x="{cx}" y="{cy + 60}" font-family="serif" font-size="200" fill="#ffffff" text-anchor="middle" font-weight="bold">Ω</text>')
    svg.append('</svg>')
    
    out = Path("04_ARTIFACTS/logo_leu_glyphes_anime.svg")
    out.write_text("\n".join(svg))
    print(f"Le VRAI Logo animé a été généré : {out}")

if __name__ == "__main__":
    generate_glyph_logo()
