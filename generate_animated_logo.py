import math
from pathlib import Path

def generate_animated_logo():
    width, height = 512, 512
    cx, cy = width / 2, height / 2
    r = 200
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#1a1a2e"/>',
        # Groupe rotatif
        '<g>',
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="10s" repeatCount="indefinite"/>'
    ]
    
    # Les 20 points
    for i in range(20):
        angle = (2 * math.pi * i) / 20
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        svg.append(f'<circle cx="{x}" cy="{y}" r="8" fill="#17becf"/>')
        
    svg.append('</g>')
    
    # Le symbole Omega au centre (statique)
    svg.append(f'<text x="{cx}" y="{cy + 40}" font-family="serif" font-size="160" fill="#ffffff" text-anchor="middle">Ω</text>')
    svg.append('</svg>')
    
    out = Path("04_ARTIFACTS/logo_leu_animated.svg")
    out.parent.mkdir(exist_ok=True, parents=True)
    out.write_text("\n".join(svg))
    print(f"Logo animé généré : {out}")

if __name__ == "__main__":
    generate_animated_logo()
