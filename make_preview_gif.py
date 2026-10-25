#!/usr/bin/env python3
"""Generate a minimal animated GIF preview of the agentic glyph."""
import struct, zlib, os

# Minimal 1-frame placeholder (a real GIF would require imageio or PIL).
# For now, create a simple SVG preview instead.
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
<rect width="100%" height="100%" fill="#fafafa"/>
<text x="200" y="100" font-family="monospace" font-size="14" text-anchor="middle" fill="#222">Lingua Executabilis Universalis Agentic Glyph — Interactive Preview</text>
<text x="200" y="130" font-family="monospace" font-size="12" text-anchor="middle" fill="#666">Open glyph_agentic_v2.svg for full interaction</text>
</svg>'''
with open("04_ARTIFACTS/preview.svg", "w") as f:
    f.write(svg)
print("wrote 04_ARTIFACTS/preview.svg")
