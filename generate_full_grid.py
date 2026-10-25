import json
from pathlib import Path

def generate_full_grid():
    media_dir = Path("07_PUBLICATION/nft_mint/media")
    out_file = Path("04_ARTIFACTS/nft_collection/magic_square.svg")

    # On force la liste exacte des 20 primitives pour être sûr qu'il n'en manque aucune
    primitives = [
        "EXIST", "CAUSE", "PART", "SAME", "ONE",
        "ALL", "NOT", "IF", "DO", "HAPPEN",
        "KNOW", "SEE", "BIG", "LIVE", "DIE",
        "MOVE", "THINK", "SAY", "TRUE", "GOOD"
    ]

    width, height = 800, 1000
    cols, rows = 4, 5
    cell_w, cell_h = width / cols, height / rows

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="#fafafa"/>']

    for i, pid in enumerate(primitives):
        row = i // cols
        col = i % cols
        x = col * cell_w + cell_w / 2
        y = row * cell_h + cell_h / 2

        # Lire le SVG correspondant
        svg_path = media_dir / f"{pid}.svg"
        if svg_path.exists():
            content = svg_path.read_text()
            start = content.find('>') + 1
            end = content.rfind('</svg>')
            glyph_content = content[start:end] if start != -1 and end != -1 else ""
        else:
            # Si jamais un fichier manque, on met un cercle gris (au cas où)
            glyph_content = '<circle cx="50" cy="50" r="30" fill="#ccc"/>'

        # Dessiner la case, le glyphe et le texte
        svg.append(f'<rect x="{col*cell_w}" y="{row*cell_h}" width="{cell_w}" height="{cell_h}" fill="none" stroke="#ddd"/>')
        svg.append(f'<g transform="translate({x - 50}, {y - 60})">')
        svg.append(glyph_content)
        svg.append('</g>')
        svg.append(f'<text x="{x}" y="{y + 60}" font-family="monospace" font-size="20" fill="#1a1a2e" text-anchor="middle">{pid}</text>')

    svg.append('</svg>')
    out_file.write_text("\n".join(svg))
    print(f"Grille de 20 glyphes regénérée avec succès : {out_file}")

if __name__ == "__main__":
    generate_full_grid()
