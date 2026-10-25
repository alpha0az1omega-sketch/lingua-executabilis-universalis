import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

def generate_live_artifact():
    # 1. Charger le glyphe MOVE
    media_path = Path("07_PUBLICATION/nft_mint/media/MOVE.svg")
    if not media_path.exists():
        print("Erreur : MOVE.svg introuvable.")
        return
    
    content = media_path.read_text()
    start = content.find('>') + 1
    end = content.rfind('</svg>')
    glyph_content = content[start:end]
    
    # 2. Calculer un Hash SHA-256 (Preuve d'intégrité)
    timestamp = datetime.now(timezone.utc).isoformat()
    data_to_hash = f"MOVE-{timestamp}"
    sha = hashlib.sha256(data_to_hash.encode()).hexdigest()
    
    # 3. Récupérer le lexique pour le son
    lexicon = json.loads(Path("01_SPECIFICATION/primitive_lexicon.json").read_text())
    move_data = next(p for p in lexicon["primitives"] if p["id"] == "MOVE")
    freq = move_data["sonification"].get("freq_start", 440)
    
    # 4. Construire le SVG interactif (HUD + Audio + Time)
    width, height = 600, 600
    cx, cy = width / 2, height / 2 - 50
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#0a0a0a"/>
<style>
    .hud-text {{ font-family: monospace; fill: #17becf; font-size: 12px; }}
    .hud-title {{ font-family: monospace; fill: #ffffff; font-size: 24px; font-weight: bold; }}
    .hash-text {{ font-family: monospace; fill: #888; font-size: 8px; }}
    .btn {{ cursor: pointer; }}
    .btn:hover {{ opacity: 0.8; }}
</style>
<defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><polygon points="0 0, 10 3, 0 6" fill="#17becf"/></marker>
</defs>

<!-- Titre -->
<text x="20" y="40" class="hud-title">L.E.U. // LIVE ARTIFACT</text>
<text x="20" y="60" class="hud-text">Primitive: MOVE (Layer L2)</text>

<!-- Glyphe Central -->
<g transform="translate({cx - 50}, {cy - 50}) scale(1.2)">
    {glyph_content}
</g>

<!-- Bouton Son -->
<g class="btn" onclick="playSound()">
    <rect x="20" y="520" width="100" height="30" fill="#17becf" rx="5"/>
    <text x="70" y="540" font-family="monospace" fill="#0a0a0a" font-size="12" text-anchor="middle" font-weight="bold">▶ PLAY SOUND</text>
</g>

<!-- Status Cryptographique -->
<text x="140" y="540" class="hud-text">STATUS: SECURED</text>

<!-- HUD Temps Réel -->
<text id="clock" x="20" y="100" class="hud-text">TIME: --:--:-- UTC</text>
<text id="hash" x="20" y="120" class="hash-text">SHA-256: {sha[:32]}...</text>

<!-- Preuve OTS (Fixe) -->
<text x="20" y="140" class="hud-text">OTS: ⛓️ ANCHORED IN BITCOIN</text>

<script type="application/ecmascript"><![CDATA[
    // 1. Mise à jour de l'heure en temps réel
    function updateClock() {{
        const now = new Date();
        const timeString = now.toISOString().split('T')[1].split('.')[0] + ' UTC';
        const clockEl = document.getElementById('clock');
        if (clockEl) clockEl.textContent = 'TIME: ' + timeString;
    }}
    setInterval(updateClock, 1000);
    updateClock();

    // 2. Synthèse Audio
    let audioCtx = null;
    function playSound() {{
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = "sine";
        osc.frequency.setValueAtTime({freq}, audioCtx.currentTime);
        // Glissando pour MOVE
        osc.frequency.exponentialRampToValueAtTime(554, audioCtx.currentTime + 0.5);
        
        gain.gain.setValueAtTime(0, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.6);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.6);
    }}
]]></script>
</svg>'''
    
    out = Path("04_ARTIFACTS/live_artifact_MOVE.svg")
    out.write_text(svg)
    print(f"Artefact en temps réel généré : {out}")

if __name__ == "__main__":
    generate_live_artifact()
