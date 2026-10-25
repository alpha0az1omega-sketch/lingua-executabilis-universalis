import math
from pathlib import Path

def load_glyphs():
    # On lit les SVG que vous avez déjà générés dans nft_mint
    media_dir = Path("07_PUBLICATION/nft_mint/media")
    glyphs = {}
    for svg_file in sorted(media_dir.glob("*.svg")):
        pid = svg_file.stem
        # On extrait juste le contenu interne (sans la balise <svg>)
        content = svg_file.read_text()
        start = content.find('>') + 1
        end = content.rfind('</svg>')
        if start != -1 and end != -1:
            glyphs[pid] = content[start:end]
    return glyphs

def generate_individual_nft(pid, glyph_content):
    # Version NFT Individuel : Fond sombre, glyphe centré, nom en bas
    width, height = 500, 500
    cx, cy = width / 2, height / 2
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#1a1a2e"/>
<g transform="translate({cx - 50}, {cy - 80}) scale(1)">
    {glyph_content}
</g>
<text x="{cx}" y="{cy + 150}" font-family="monospace" font-size="40" fill="#ffffff" text-anchor="middle" font-weight="bold">{pid}</text>
</svg>'''
    
    out = Path(f"04_ARTIFACTS/nft_collection/nft_{pid}.svg")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)

def generate_grid(glyphs):
    # Version Grille (Carré Magique) : 4 colonnes x 5 lignes
    width, height = 800, 1000
    cols, rows = 4, 5
    cell_w, cell_h = width / cols, height / rows
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="#fafafa"/>']
    
    for i, (pid, content) in enumerate(glyphs.items()):
        row = i // cols
        col = i % cols
        x = col * cell_w + cell_w / 2
        y = row * cell_h + cell_h / 2
        
        # Ligne de la grille
        svg.append(f'<rect x="{col*cell_w}" y="{row*cell_h}" width="{cell_w}" height="{cell_h}" fill="none" stroke="#ddd"/>')
        
        # Glyphe
        svg.append(f'<g transform="translate({x - 50}, {y - 60})">')
        svg.append(content)
        svg.append('</g>')
        
        # Texte
        svg.append(f'<text x="{x}" y="{y + 60}" font-family="monospace" font-size="20" fill="#1a1a2e" text-anchor="middle">{pid}</text>')
    
    svg.append('</svg>')
    
    out = Path("04_ARTIFACTS/nft_collection/magic_square.svg")
    out.write_text("\n".join(svg))

def generate_circle(glyphs):
    # Version Cercle (sans Omega)
    width, height = 800, 800
    cx, cy = width / 2, height / 2
    radius = 300
    
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="#1a1a2e"/>',
           '<g>',
           f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="20s" repeatCount="indefinite"/>']
    
    for i, (pid, content) in enumerate(glyphs.items()):
        angle = (2 * math.pi * i) / len(glyphs)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        
        svg.append(f'<g transform="translate({x - 50}, {y - 50})">')
        svg.append(content)
        svg.append('</g>')
    
    svg.append('</g>')
    svg.append('</svg>')
    
    out = Path("04_ARTIFACTS/nft_collection/glyphs_circle.svg")
    out.write_text("\n".join(svg))

if __name__ == "__main__":
    print("Chargement des 20 glyphes...")
    glyphs = load_glyphs()
    print(f"{len(glyphs)} glyphes chargés.")
    
    print("Génération des NFT individuels...")
    for pid, content in glyphs.items():
        generate_individual_nft(pid, content)
        
    print("Génération du Carré Magique...")
    generate_grid(glyphs)
    
    print("Génération du Cercle...")
    generate_circle(glyphs)
    
    print("\nTout est prêt dans : 04_ARTIFACTS/nft_collection/")
