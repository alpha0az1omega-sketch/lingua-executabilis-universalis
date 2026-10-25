import json
import hashlib
import random
import sys
from pathlib import Path

def generate_universe(N):
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    out_dir = root / "04_ARTIFACTS" / "species_3d"
    out_dir.mkdir(parents=True, exist_ok=True)
    index = []

    primitives = ["EXIST", "SAME", "ONE", "ALL", "NOT", "IF", "TRUE", "CAUSE", "PART", "BIG", "DO", "HAPPEN", "MOVE", "KNOW", "SEE", "THINK", "SAY", "LIVE", "DIE", "GOOD"]
    types = ["animal", "plant", "human", "concept", "element"]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    
    # On fixe la seed pour que l'univers soit reproductible
    random.seed(42)
    gpg = "4ED4A15BB5998C6239DE340336D4AEC00ADD1AEE"
    doi = "10.5281/zenodo.23476518"

    for i in range(N):
        sp_id = f"species_{i:06d}"
        sp_type = random.choice(types)
        name = f"Organism-{i:06d}"
        traits = random.sample(primitives, k=random.randint(3, 5))
        eq = " AND ".join([f"{t}(x)" for t in traits[:2]])
        color = random.choice(colors)
        freq = random.randint(100, 1000)
        real_sha = hashlib.sha256(f"{sp_id}:{eq}".encode()).hexdigest()

        index.append({"id": sp_id, "name": name, "type": sp_type, "color": color, "sha": real_sha, "eq": eq})

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>L.E.U. — {name}</title>
    <style>
        body {{ margin:0; overflow:hidden; background:#1a1a1a; font-family:'Courier New',monospace; }}
        #c {{ position:fixed; top:0; left:0; width:100%; height:100%; z-index:1; }}
        #hud {{ position:fixed; top:0; left:0; width:100%; height:100%; z-index:2; pointer-events:none; }}
        .p {{ position:absolute; background:rgba(26,26,26,0.85); border:1px solid {color}; border-radius:8px; padding:12px 16px; color:{color}; font-size:12px; line-height:1.6; }}
        .t {{ color:#c0c0c0; font-weight:bold; letter-spacing:2px; margin-bottom:6px; font-size:11px; }}
        #tl {{ top:20px; left:20px; }} #tr {{ top:20px; right:20px; text-align:right; }}
        #tc {{ top:20px; left:50%; transform:translateX(-50%); text-align:center; padding:10px 30px; }}
        #tc .n {{ font-size:24px; color:{color}; letter-spacing:4px; font-weight:bold; }}
        #bl {{ bottom:20px; left:20px; pointer-events:auto; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="c"></div>
    <div id="hud">
        <div class="p" id="tc"><div class="n">{name}</div><div style="font-size:10px;color:#c0c0c0;">{sp_type.upper()}</div></div>
        <div class="p" id="tl">
            <div class="t">Genetic Code (DNA)</div>
            <div>SHA-256: {real_sha[:32]}...</div>
            <div>GPG: {gpg}</div>
            <div>DOI: {doi}</div>
            <div>EQUATION: {eq}</div>
        </div>
        <div class="p" id="tr">
            <div class="t">Telemetry</div>
            <div>TIME: <span id="clock">--:--:--</span></div>
            <div>STATE: LIVING</div>
        </div>
        <div class="p" id="bl">
            <button onclick="playSound({freq})" style="background:{color};color:#000;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;font-weight:bold;">▶ PLAY FREQUENCY ({freq} Hz)</button>
        </div>
    </div>
    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
        camera.position.z = 15;
        const renderer = new THREE.WebGLRenderer({{ antialias:true, alpha:true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('c').appendChild(renderer.domElement);
        scene.add(new THREE.AmbientLight(0xffffff, 0.5));
        const pl = new THREE.PointLight({color.replace('#','0x')}, 2, 50); pl.position.set(5,5,5); scene.add(pl);
        const geo = new THREE.IcosahedronGeometry(4, 1);
        const mat = new THREE.MeshStandardMaterial({{ color:{color.replace('#','0x')}, wireframe:true, emissive:{color.replace('#','0x')}, emissiveIntensity:0.5 }});
        const core = new THREE.Mesh(geo, mat); scene.add(core);
        const pGeo = new THREE.BufferGeometry();
        const pCount = 500; const pos = new Float32Array(pCount*3);
        for(let i=0;i<pCount*3;i++) pos[i] = (Math.random()-0.5)*15;
        pGeo.setAttribute('position', new THREE.BufferAttribute(pos,3));
        const particles = new THREE.Points(pGeo, new THREE.PointsMaterial({{ size:0.05, color:{color.replace('#','0x')} }}));
        scene.add(particles);
        function animate() {{ requestAnimationFrame(animate); core.rotation.x += 0.005; core.rotation.y += 0.01; particles.rotation.y -= 0.002; renderer.render(scene, camera); }}
        animate();
        function updateClock() {{ document.getElementById('clock').textContent = new Date().toISOString().split('T')[1].split('.')[0] + ' UTC'; }}
        setInterval(updateClock, 1000); updateClock();
        function playSound(freq) {{
            var ctx = new (window.AudioContext || window.webkitAudioContext)();
            if (ctx.state === 'suspended') ctx.resume();
            var osc = ctx.createOscillator(); var gain = ctx.createGain();
            osc.type = "sine"; osc.frequency.setValueAtTime(freq, ctx.currentTime);
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            osc.connect(gain); gain.connect(ctx.destination);
            osc.start(); osc.stop(ctx.currentTime + 0.8);
        }}
    </script>
</body>
</html>'''
        (out_dir / f"{sp_id}.html").write_text(html)

    # Sauvegarde de l'index global
    (out_dir / "index.json").write_text(json.dumps(index, indent=2))
    print(f"{N} espèces générées avec succès dans {out_dir}")
    print(f"Index global sauvegardé : {out_dir / 'index.json'}")

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    generate_universe(N)
