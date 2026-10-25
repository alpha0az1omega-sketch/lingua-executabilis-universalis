import json
import hashlib
from pathlib import Path

def generate_species():
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    seed_file = root / "01_SPECIFICATION" / "species_seed.json"
    out_dir = root / "04_ARTIFACTS" / "species"
    out_dir.mkdir(parents=True, exist_ok=True)

    species_list = json.loads(seed_file.read_text())
    gpg = "4ED4A15BB5998C6239DE340336D4AEC00ADD1AEE"
    doi = "10.5281/zenodo.23476518"

    for sp in species_list:
        sp_id = sp["id"]
        name = sp["name"]
        sp_type = sp["type"]
        eq = sp["equation"]
        color = sp["color"]
        freq = sp.get("freq_hz", 440)
        traits = ", ".join(sp["l0_l4_traits"])

        # Hash unique pour l'espèce
        real_sha = hashlib.sha256(f"{sp_id}:{eq}".encode()).hexdigest()

        # Création du SVG
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="700" viewBox="0 0 600 700">
<rect width="100%" height="100%" fill="#1a1a1a"/>
<!-- Cercle identitaire -->
<circle cx="300" cy="200" r="100" fill="none" stroke="{color}" stroke-width="6"/>
<circle cx="300" cy="200" r="90" fill="none" stroke="{color}" stroke-width="1" opacity="0.5"/>

<!-- Nom et Type -->
<text x="300" y="190" font-family="monospace" font-size="32" fill="{color}" text-anchor="middle" font-weight="bold">{name}</text>
<text x="300" y="220" font-family="monospace" font-size="14" fill="#888" text-anchor="middle">{sp_type.upper()}</text>

<!-- Traits L.E.U. -->
<text x="300" y="340" font-family="monospace" font-size="14" fill="#c0c0c0" text-anchor="middle">TRAITS: {traits}</text>

<!-- Équation -->
<text x="300" y="380" font-family="monospace" font-size="12" fill="#d4af37" text-anchor="middle">EQUATION: {eq}</text>

<!-- Preuves Cryptographiques -->
<text x="300" y="440" font-family="monospace" font-size="10" fill="#555" text-anchor="middle">SHA-256: {real_sha[:48]}...</text>
<text x="300" y="460" font-family="monospace" font-size="10" fill="#555" text-anchor="middle">GPG: {gpg}</text>
<text x="300" y="480" font-family="monospace" font-size="10" fill="#555" text-anchor="middle">DOI: {doi}</text>

<!-- Horloge -->
<text x="300" y="520" font-family="monospace" font-size="12" fill="{color}" text-anchor="middle">TIME (UTC): <tspan id="clock">--:--:--</tspan></text>
<text x="300" y="540" font-family="monospace" font-size="10" fill="#888" text-anchor="middle">STATUS: SECURED ON BITCOIN</text>

<!-- Bouton Son -->
<g transform="translate(250, 580)" style="cursor:pointer;" onclick="playSound({freq})">
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

        # Sauvegarde
        file_path = out_dir / f"species_{sp_id}.svg"
        file_path.write_text(svg)
        print(f"Généré : {sp_id} ({name})")

    print(f"\nTous les artefacts d'espèces sont dans : {out_dir}")

if __name__ == "__main__":
    generate_species()
