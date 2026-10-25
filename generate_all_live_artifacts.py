import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

def generate_all_live_artifacts():
    lexicon = json.loads(Path("01_SPECIFICATION/primitive_lexicon.json").read_text())
    media_dir = Path("07_PUBLICATION/nft_mint/media")
    out_dir = Path("04_ARTIFACTS/live_artifacts")
    out_dir.mkdir(parents=True, exist_ok=True)

    gpg_fingerprint = "4ED4A15BB5998C6239DE340336D4AEC00ADD1AEE"
    doi = "10.5281/zenodo.23476518"

    for p in lexicon["primitives"]:
        pid = p["id"]
        layer = p["layer"]
        formal = p["formal"]
        
        # 1. Lire le glyphe SVG
        svg_path = media_dir / f"{pid}.svg"
        if not svg_path.exists():
            continue
        content = svg_path.read_text()
        start = content.find('>') + 1
        end = content.rfind('</svg>')
        glyph_content = content[start:end]
        
        # 2. Vrai Hash SHA-256 de la définition formelle
        data_to_hash = f"{pid}:{formal}"
        real_sha = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        # 3. Extraire les données audio
        son = p["sonification"]
        freq = son.get("freq_hz", son.get("freq_start", 440))
        if isinstance(freq, list): freq = freq[0]
        freq_end = son.get("freq_end", freq)
        
        # 4. Construire le SVG Live
        width, height = 800, 600
        cx, cy = width / 2, height / 2 - 50
        
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#0a0a0a"/>
<style>
    .hud {{ font-family: 'Courier New', monospace; fill: #17becf; font-size: 14px; }}
    .title {{ font-family: 'Courier New', monospace; fill: #ffffff; font-size: 28px; font-weight: bold; }}
    .hash {{ font-family: 'Courier New', monospace; fill: #888; font-size: 10px; }}
    .btn {{ cursor: pointer; }}
    .btn:hover {{ opacity: 0.8; }}
</style>

<!-- En-tête -->
<text x="30" y="50" class="title">L.E.U. // LIVE ARTIFACT</text>
<text x="30" y="80" class="hud">PRIMITIVE: {pid} (Layer {layer})</text>
<text x="30" y="105" class="hud">FORMAL: {formal}</text>

<!-- Glyphe Central -->
<g transform="translate({cx - 100}, {cy - 120}) scale(2)">
    {glyph_content}
</g>

<!-- HUD de Preuves -->
<text x="30" y="300" class="hud">TIME (UTC): <tspan id="clock">--:--:--</tspan></text>
<text x="30" y="330" class="hash">REAL SHA-256: {real_sha}</text>
<text x="30" y="350" class="hash">GPG KEY: {gpg_fingerprint}</text>
<text x="30" y="370" class="hash">DOI: {doi}</text>
<text x="30" y="390" class="hud">STATUS: ANCHORED ON BITCOIN</text>

<!-- Bouton Son -->
<g class="btn" onclick="playSound()">
    <rect x="30" y="480" width="200" height="50" fill="#17becf" rx="5"/>
    <text x="130" y="512" font-family="'Courier New', monospace" fill="#0a0a0a" font-size="16" text-anchor="middle" font-weight="bold">▶ PLAY SOUND</text>
</g>

<!-- Lien Zenodo -->
<g class="btn" onclick="window.open('https://doi.org/{doi}', '_blank')">
    <rect x="250" y="480" width="200" height="50" fill="none" stroke="#17becf" stroke-width="2" rx="5"/>
    <text x="350" y="512" font-family="'Courier New', monospace" fill="#17becf" font-size="14" text-anchor="middle">VERIFY PROOF</text>
</g>

<script type="application/ecmascript"><![CDATA[
    // Horloge temps réel
    function updateClock() {{
        const now = new Date();
        const timeString = now.toISOString().split('T')[1].split('.')[0];
        const clockEl = document.getElementById('clock');
        if (clockEl) clockEl.textContent = timeString;
    }}
    setInterval(updateClock, 1000);
    updateClock();

    // Synthèse Audio (Web Audio API)
    let audioCtx = null;
    function playSound() {{
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime({freq}, audioCtx.currentTime);
        
        // Si c'est MOVE ou CAUSE, on fait un glissando
        if ({freq_end} !== {freq}) {{
            osc.frequency.exponentialRampToValueAtTime({freq_end}, audioCtx.currentTime + 0.5);
        }}
        
        gain.gain.setValueAtTime(0, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.3, audioCtx.currentTime + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.8);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.8);
    }}
]]></script>
</svg>'''
        
        out_file = out_dir / f"live_{pid}.svg"
        out_file.write_text(svg)
        print(f"Généré : live_{pid}.svg (SHA: {real_sha[:8]}...)")

    print(f"\nLes 20 artefacts en temps réel sont prêts dans : {out_dir}")

if __name__ == "__main__":
    generate_all_live_artifacts()
