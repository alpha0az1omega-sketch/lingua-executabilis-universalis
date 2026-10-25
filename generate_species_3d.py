import json
import hashlib
from pathlib import Path

def generate_species_3d():
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    seed_file = root / "01_SPECIFICATION" / "species_seed.json"
    out_dir = root / "04_ARTIFACTS" / "species_3d"
    out_dir.mkdir(parents=True, exist_ok=True)

    species_list = json.loads(seed_file.read_text())
    gpg = "4ED4A15BB5998C6239DE340336D4AEC00ADD1AEE"
    doi = "10.5281/zenodo.23476518"

    for sp in species_list:
        sp_id = sp["id"]
        name = sp["name"]
        sp_type = sp["type"]
        eq = sp["equation"]
        color_hex = sp["color"].replace("#", "0x")
        freq = sp.get("freq_hz", 440)
        traits = ", ".join(sp["l0_l4_traits"])
        real_sha = hashlib.sha256(f"{sp_id}:{eq}".encode()).hexdigest()

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>L.E.U. Species — {name}</title>
    <style>
        body {{ margin: 0; overflow: hidden; background-color: #1a1a1a; font-family: 'Courier New', monospace; }}
        #three-container {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }}
        #hud {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; pointer-events: none; }}
        .hud-panel {{
            position: absolute; background: rgba(26, 26, 26, 0.85); border: 1px solid {sp["color"]};
            border-radius: 8px; padding: 12px 16px; color: {sp["color"]};
            font-size: 12px; line-height: 1.6; backdrop-filter: blur(4px);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
        }}
        .hud-title {{ color: #c0c0c0; font-weight: bold; letter-spacing: 2px; margin-bottom: 6px; font-size: 11px; text-transform: uppercase; }}
        #hud-tl {{ top: 20px; left: 20px; }}
        #hud-tr {{ top: 20px; right: 20px; text-align: right; }}
        #hud-center-top {{
            top: 20px; left: 50%; transform: translateX(-50%);
            text-align: center; padding: 10px 30px; background: rgba(26, 26, 26, 0.95);
            border: 2px solid {sp["color"]};
        }}
        #hud-center-top .name {{ font-size: 24px; color: {sp["color"]}; letter-spacing: 4px; font-weight: bold; }}
        #hud-center-top .type {{ font-size: 10px; color: #c0c0c0; letter-spacing: 2px; }}
        #hud-bl {{ bottom: 20px; left: 20px; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="three-container"></div>
    <div id="hud">
        <div class="hud-panel" id="hud-center-top">
            <div class="name">{name}</div>
            <div class="type">{sp_type.upper()}</div>
        </div>
        <div class="hud-panel" id="hud-tl">
            <div class="hud-title">Genetic Code (DNA)</div>
            <div>SHA-256: <span id="sha">{real_sha[:32]}...</span></div>
            <div>GPG: {gpg}</div>
            <div>DOI: {doi}</div>
            <div>EQUATION: {eq}</div>
            <div>TRAITS: {traits}</div>
        </div>
        <div class="hud-panel" id="hud-tr">
            <div class="hud-title">Live Telemetry</div>
            <div>TIME (UTC): <span id="clock">--:--:--</span></div>
            <div>STATE: <span style="color:#17becf;">LIVING</span></div>
            <div>TYPE: {sp_type.upper()}</div>
        </div>
        <div class="hud-panel" id="hud-bl">
            <div class="hud-title">Sonification</div>
            <button onclick="playSound({freq})" style="background:{sp["color"]};color:#000;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;font-weight:bold;">▶ PLAY FREQUENCY ({freq} Hz)</button>
        </div>
    </div>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 15;
        const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('three-container').appendChild(renderer.domElement);

        const ambient = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambient);
        const pointLight = new THREE.PointLight({color_hex}, 2, 50);
        pointLight.position.set(5, 5, 5);
        scene.add(pointLight);

        // Le noyau 3D (ADN visuel)
        const geometry = new THREE.IcosahedronGeometry(4, 1);
        const material = new THREE.MeshStandardMaterial({{
            color: {color_hex},
            wireframe: true,
            emissive: {color_hex},
            emissiveIntensity: 0.5
        }});
        const core = new THREE.Mesh(geometry, material);
        scene.add(core);

        // Particules autour (le "nuage" de données)
        const particlesGeo = new THREE.BufferGeometry();
        const particlesCount = 500;
        const posArray = new Float32Array(particlesCount * 3);
        for(let i = 0; i < particlesCount * 3; i++) {{
            posArray[i] = (Math.random() - 0.5) * 15;
        }}
        particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particlesMat = new THREE.PointsMaterial({{ size: 0.05, color: {color_hex} }});
        const particles = new THREE.Points(particlesGeo, particlesMat);
        scene.add(particles);

        let time = 0;
        function animate() {{
            requestAnimationFrame(animate);
            time += 0.01;
            core.rotation.x += 0.005;
            core.rotation.y += 0.01;
            particles.rotation.y -= 0.002;
            
            renderer.render(scene, camera);
        }}
        animate();

        function updateClock() {{
            var now = new Date();
            document.getElementById('clock').textContent = now.toISOString().split('T')[1].split('.')[0] + ' UTC';
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
            osc.stop(ctx.currentTime + 0.8);
        }}
    </script>
</body>
</html>'''

        file_path = out_dir / f"species_{sp_id}.html"
        file_path.write_text(html)
        print(f"Généré en 3D : {sp_id} ({name})")

    print(f"\nTous les artefacts 3D sont dans : {out_dir}")

if __name__ == "__main__":
    generate_species_3d()
