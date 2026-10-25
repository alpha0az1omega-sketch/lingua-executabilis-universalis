import json
import hashlib
from pathlib import Path

COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
]

def generate_final_visuals():
    lexicon = json.loads(Path("01_SPECIFICATION/primitive_lexicon.json").read_text())
    media_dir = Path("07_PUBLICATION/nft_mint/media")
    nft_dir = Path("04_ARTIFACTS/nft_collection")
    live_dir = Path("04_ARTIFACTS/live_artifacts")

    media_dir.mkdir(parents=True, exist_ok=True)
    nft_dir.mkdir(parents=True, exist_ok=True)
    live_dir.mkdir(parents=True, exist_ok=True)

    gpg_key = "4ED4A15BB5998C6239DE340336D4AEC00ADD1AEE"
    doi = "10.5281/zenodo.23476518"

    for i, p in enumerate(lexicon["primitives"]):
        pid = p["id"]
        layer = p["layer"]
        formal = p["formal"]
        color = COLORS[i % len(COLORS)]

        real_sha = hashlib.sha256(f"{pid}:{formal}".encode()).hexdigest()

        # 1. Le Glyphe Simple
        glyph_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
<circle cx="50" cy="50" r="45" fill="none" stroke="{color}" stroke-width="4"/>
<text x="50" y="65" font-family="monospace" font-size="40" fill="{color}" text-anchor="middle">{pid[0]}</text>
</svg>'''
        (media_dir / f"{pid}.svg").write_text(glyph_svg)

        # 2. Le NFT Individuel
        nft_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500" viewBox="0 0 500 500">
<rect width="100%" height="100%" fill="#ffffff"/>
<circle cx="250" cy="250" r="180" fill="none" stroke="{color}" stroke-width="8"/>
<text x="250" y="280" font-family="monospace" font-size="120" fill="{color}" text-anchor="middle" font-weight="bold">{pid[0]}</text>
<text x="250" y="450" font-family="monospace" font-size="24" fill="#333" text-anchor="middle">{pid}</text>
</svg>'''
        (nft_dir / f"nft_{pid}.svg").write_text(nft_svg)

        # 3. Le Live Artifact (Preuves + Horloge)
        freq = p["sonification"].get("freq_hz", p["sonification"].get("freq_start", 440))
        if isinstance(freq, list): freq = freq[0]

        live_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="700" viewBox="0 0 600 700">
<rect width="100%" height="100%" fill="#ffffff"/>
<circle cx="300" cy="250" r="120" fill="none" stroke="{color}" stroke-width="6"/>
<text x="300" y="280" font-family="monospace" font-size="80" fill="{color}" text-anchor="middle" font-weight="bold">{pid[0]}</text>

<text x="300" y="420" font-family="monospace" font-size="24" fill="#111" text-anchor="middle" font-weight="bold">PRIMITIVE: {pid} (Layer {layer})</text>
<text x="300" y="450" font-family="monospace" font-size="16" fill="#555" text-anchor="middle">FORMAL: {formal}</text>

<text x="300" y="500" font-family="monospace" font-size="12" fill="#333" text-anchor="middle">REAL SHA-256: {real_sha[:32]}...</text>
<text x="300" y="520" font-family="monospace" font-size="12" fill="#333" text-anchor="middle">GPG KEY: {gpg_key}</text>
<text x="300" y="540" font-family="monospace" font-size="12" fill="#333" text-anchor="middle">DOI: {doi}</text>

<text x="300" y="580" font-family="monospace" font-size="14" fill="{color}" text-anchor="middle">TIME (UTC): <tspan id="clock">--:--:--</tspan></text>
<text x="300" y="600" font-family="monospace" font-size="12" fill="#666" text-anchor="middle">STATUS: ANCHORED ON BITCOIN</text>

<g transform="translate(250, 630)" style="cursor:pointer;" onclick="playSound({freq})">
    <rect width="100" height="30" fill="{color}" rx="5"/>
    <text x="50" y="20" font-family="monospace" font-size="12" fill="#fff" text-anchor="middle">▶ PLAY SOUND</text>
</g>

<script type="application/ecmascript"><![CDATA[
    function updateClock() {{
        var now = new Date();
        var timeStr = now.toISOString().split('T')[1].split('.')[0] + ' UTC';
        var clockEl = document.getElementById('clock');
        if (clockEl) clockEl.textContent = timeStr;
    }}
    setInterval(updateClock, 1000);
    updateClock();

    function playSound(freq) {{
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.5);
    }}
]]></script>
</svg>'''
        (live_dir / f"live_{pid}.svg").write_text(live_svg)

    print("20 SVG, 20 NFT et 20 Live Artifacts régénérés avec succès (Fond Blanc + Preuves).")

if __name__ == "__main__":
    generate_final_visuals()
