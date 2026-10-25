import json
import hashlib
import random
import sys
from pathlib import Path

def make_html(sp_id, name, sp_type, color, freq, eq, sha, morph_code):
    return f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>L.E.U. — {name}</title>
<style>
body{{margin:0;overflow:hidden;background:#0a0a0a;font-family:'Courier New',monospace}}
#matrix-bg{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0}}
#c{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1}}
#hud{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:2;pointer-events:none}}
.p{{position:absolute;background:rgba(26,26,26,0.85);border:1px solid {color};border-radius:8px;padding:12px 16px;color:{color};font-size:12px;line-height:1.6;backdrop-filter:blur(4px)}}
.t{{color:#c0c0c0;font-weight:bold;letter-spacing:2px;margin-bottom:6px;font-size:11px}}
#tl{{top:20px;left:20px}} #tr{{top:20px;right:20px;text-align:right}}
#tc{{top:20px;left:50%;transform:translateX(-50%);text-align:center;padding:10px 30px}}
#tc .n{{font-size:24px;color:{color};letter-spacing:4px;font-weight:bold}}
#bl{{bottom:20px;left:20px;pointer-events:auto}}
#br{{bottom:20px;right:20px;text-align:right}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head>
<body>
<canvas id="matrix-bg"></canvas>
<div id="c"></div>
<div id="hud">
<div class="p" id="tc"><div class="n">{name}</div><div style="font-size:10px;color:#c0c0c0">{sp_type.upper()}</div></div>
<div class="p" id="tl"><div class="t">Genetic Code (DNA)</div>
<div>SHA-256: {sha[:32]}...</div>
<div>GPG: 4ED4A15BB5998C6239DE340336D4AEC00ADD1AEE</div>
<div>DOI: 10.5281/zenodo.23476518</div>
<div>EQ: {eq}</div></div>
<div class="p" id="tr"><div class="t">Live Telemetry</div>
<div>TIME: <span id="clock">--:--:--</span></div>
<div>STATE: LIVING</div></div>
<div class="p" id="bl"><button onclick="playSound({freq})" style="background:{color};color:#000;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;font-weight:bold">▶ PLAY ({freq} Hz)</button></div>
<div class="p" id="br"><div class="t">Scientific Measurements</div>
<div id="measures" style="font-size:11px">calculating...</div></div>
</div>
<script>
// ===== 1. MATRIX BACKGROUND =====
const mc = document.getElementById('matrix-bg');
const mctx = mc.getContext('2d');
mc.width = innerWidth; mc.height = innerHeight;
const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*EXISTCAUSEPARTSAMEONEALLNOTIFDOHAPPENKNOWSEEBIGLIVEDIEMOVETHINKSAYTRUEGOOD';
const fs = 14; let cols = Math.floor(mc.width / fs); let drops = [];
for (let x=0; x<cols; x++) drops[x] = Math.random()*mc.height;
function drawMatrix() {{
    mctx.fillStyle = 'rgba(10,10,10,0.08)'; mctx.fillRect(0,0,mc.width,mc.height);
    mctx.font = fs + 'px monospace';
    for (let i=0; i<drops.length; i++) {{
        const txt = letters.charAt(Math.floor(Math.random()*letters.length));
        mctx.fillStyle = Math.random() > 0.7 ? '#d4af37' : '#c0c0c0'; // Or et Argent
        mctx.fillText(txt, i*fs, drops[i]*fs);
        if (drops[i]*fs > mc.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
    }}
}}
setInterval(drawMatrix, 50);

// ===== 2. THREE.JS SCENE =====
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x0a0a0a, 0.03);
const camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
camera.position.z = 15;
const renderer = new THREE.WebGLRenderer({{antialias:true,alpha:true}});
renderer.setSize(innerWidth, innerHeight);
document.getElementById('c').appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0xffffff,0.5));
const pl = new THREE.PointLight({color.replace('#','0x')},2,60); pl.position.set(8,8,8); scene.add(pl);
const C = {color.replace('#','0x')};

{morph_code}

function animate(){{requestAnimationFrame(animate); animateMorph(); renderer.render(scene,camera);}}
animate();
function updateClock(){{document.getElementById('clock').textContent = new Date().toISOString().split('T')[1].split('.')[0]+' UTC';}}
setInterval(updateClock,1000); updateClock();
function playSound(freq){{var ctx=new(window.AudioContext||window.webkitAudioContext)();if(ctx.state==='suspended')ctx.resume();var o=ctx.createOscillator(),g=ctx.createGain();o.type="sine";o.frequency.setValueAtTime(freq,ctx.currentTime);g.gain.setValueAtTime(0.2,ctx.currentTime);o.connect(g);g.connect(ctx.destination);o.start();o.stop(ctx.currentTime+0.8);}}
function updateMeasures(txt){{document.getElementById('measures').innerHTML = txt;}}
</script></body></html>'''

# ==== MORPHOLOGIES (codes Three.js distincts) ====

MORPH_ATOM = """
const nucleusGeo = new THREE.SphereGeometry(0.8, 32, 32);
const nucleus = new THREE.Mesh(nucleusGeo, new THREE.MeshStandardMaterial({color:C, emissive:C, emissiveIntensity:0.8}));
scene.add(nucleus);
const orbits = [];
for (let i = 0; i < 3; i++) {
  const orbitGeo = new THREE.TorusGeometry(3 + i*0.8, 0.04, 8, 80);
  const orbit = new THREE.Mesh(orbitGeo, new THREE.MeshBasicMaterial({color:C, transparent:true, opacity:0.4}));
  orbit.rotation.x = Math.PI/2; orbit.rotation.y = i*Math.PI/3;
  scene.add(orbit); orbits.push(orbit);
  const eGeo = new THREE.SphereGeometry(0.2, 16, 16);
  const electron = new THREE.Mesh(eGeo, new THREE.MeshStandardMaterial({color:0xffffff, emissive:0xffffff, emissiveIntensity:0.5}));
  scene.add(electron); orbit.userData = {electron};
}
function animateMorph(){ orbits.forEach((o,i)=>{ o.rotation.z += 0.01*(i+1); const e=o.userData.electron; if(e){ e.position.set(Math.cos(Date.now()*0.001*(i+1))*(3+i*0.8), Math.sin(Date.now()*0.001*(i+1))*(3+i*0.8), 0); e.applyMatrix4(o.matrix); } }); nucleus.rotation.y += 0.01; updateMeasures('ELEMENTS: 3<br>ORBITS: 3<br>ELECTRONS: 3'); }
"""

MORPH_ADN = """
const helixGroup = new THREE.Group(); scene.add(helixGroup);
const strandGeo = new THREE.SphereGeometry(0.25, 16, 16);
const strandMat = new THREE.MeshStandardMaterial({color:C, emissive:C, emissiveIntensity:0.5});
for (let i = 0; i < 40; i++) {
  const t = i * 0.4; const y = i * 0.4 - 8;
  const s1 = new THREE.Mesh(strandGeo, strandMat); s1.position.set(Math.cos(t)*2, y, Math.sin(t)*2); helixGroup.add(s1);
  const s2 = new THREE.Mesh(strandGeo, strandMat); s2.position.set(Math.cos(t+Math.PI)*2, y, Math.sin(t+Math.PI)*2); helixGroup.add(s2);
  if (i % 2 === 0) { const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.05,0.05,4,8), new THREE.MeshStandardMaterial({color:0xffffff})); bar.position.set(0,y,0); bar.rotation.z = Math.PI/2; bar.rotation.y = t; helixGroup.add(bar); }
}
function animateMorph(){ helixGroup.rotation.y += 0.01; updateMeasures('BASE PAIRS: 40<br>TORSION: '+(Date.now()*0.0001).toFixed(2)+'<br>RADIUS: 2.0'); }
"""

MORPH_ANIMAL = """
const body = new THREE.Group(); scene.add(body);
// Corps (Cylindre au lieu de Capsule pour compatibilité r128)
const bodyGeo = new THREE.CylinderGeometry(1.2, 1.2, 3, 16);
const bodyMesh = new THREE.Mesh(bodyGeo, new THREE.MeshStandardMaterial({color:C, roughness:0.4}));
bodyMesh.rotation.z = Math.PI/2; scene.add(bodyMesh);
// Tête (Sphère)
const headGeo = new THREE.SphereGeometry(0.9, 24, 24);
const head = new THREE.Mesh(headGeo, new THREE.MeshStandardMaterial({color:C}));
head.position.set(2.8, 0.5, 0); scene.add(head);
// Pattes (Cylindres)
const legGeo = new THREE.CylinderGeometry(0.15, 0.15, 2.5, 8);
for (let i = 0; i < 4; i++) { const leg = new THREE.Mesh(legGeo, new THREE.MeshStandardMaterial({color:C})); leg.position.set(-1.5 + i*1.5, -1.8, (i%2===0?0.6:-0.6)); scene.add(leg); }
// Queue (Cylindre)
const tail = new THREE.Mesh(new THREE.CylinderGeometry(0.08,0.08,1.5,8), new THREE.MeshStandardMaterial({color:C})); tail.position.set(-3.3, 0.5, 0); tail.rotation.z = -0.5; scene.add(tail);
function animateMorph(){ bodyMesh.rotation.z += 0.002; head.position.y = 0.5 + Math.sin(Date.now()*0.003)*0.1; updateMeasures('SEGMENTS: 6<br>MASS EST: 450 kg<br>VELOCITY: '+(Math.sin(Date.now()*0.001)*3+5).toFixed(2)+' m/s'); }
"""

MORPH_HUMAN = """
const skeleton = new THREE.Group(); scene.add(skeleton);
const headM = new THREE.Mesh(new THREE.SphereGeometry(0.7, 24, 24), new THREE.MeshStandardMaterial({color:C, emissive:C, emissiveIntensity:0.2}));
headM.position.y = 4; skeleton.add(headM);
const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.8, 3, 12), new THREE.MeshStandardMaterial({color:C, wireframe:true}));
torso.position.y = 1.8; skeleton.add(torso);
for (let side of [-1,1]) {
  const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.15,0.15,2.2,8), new THREE.MeshStandardMaterial({color:C}));
  arm.position.set(side*1.2, 2, 0); arm.rotation.z = side*0.3; skeleton.add(arm);
  const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.2,0.2,2.5,8), new THREE.MeshStandardMaterial({color:C}));
  leg.position.set(side*0.4, -0.5, 0); skeleton.add(leg);
}
const nGeo = new THREE.SphereGeometry(0.08, 8, 8);
for (let i = 0; i < 30; i++) { const n = new THREE.Mesh(nGeo, new THREE.MeshBasicMaterial({color:0xffffff})); n.position.set((Math.random()-0.5)*2, Math.random()*4-1, (Math.random()-0.5)*1); skeleton.add(n); }
function animateMorph(){ skeleton.rotation.y += 0.005; updateMeasures('NEURONS: 30<br>HEIGHT: 1.8m<br>SYNAPSES: '+(30*Math.sin(Date.now()*0.001)+50).toFixed(0)); }
"""

MORPH_NETWORK = """
const net = new THREE.Group(); scene.add(net);
const nodes = [];
const nGeo = new THREE.SphereGeometry(0.3, 16, 16);
for (let i = 0; i < 25; i++) {
  const n = new THREE.Mesh(nGeo, new THREE.MeshStandardMaterial({color:C, emissive:C, emissiveIntensity:0.8}));
  n.position.set((Math.random()-0.5)*10, (Math.random()-0.5)*10, (Math.random()-0.5)*10);
  net.add(n); nodes.push(n);
}
const edges = [];
for (let i = 0; i < 40; i++) {
  const a = nodes[Math.floor(Math.random()*nodes.length)], b = nodes[Math.floor(Math.random()*nodes.length)];
  if (a === b) continue;
  const geo = new THREE.BufferGeometry().setFromPoints([a.position, b.position]);
  const line = new THREE.Line(geo, new THREE.LineBasicMaterial({color:C, transparent:true, opacity:0.3}));
  net.add(line); edges.push({line, a, b});
}
function animateMorph(){ net.rotation.y += 0.003; net.rotation.x += 0.002; updateMeasures('NODES: 25<br>EDGES: 40<br>DEGREE: '+(2*40/25).toFixed(2)); }
"""

MORPH_PARTICLE = """
const particles = [];
const pGeo = new THREE.SphereGeometry(0.15, 8, 8);
for (let i = 0; i < 200; i++) {
  const p = new THREE.Mesh(pGeo, new THREE.MeshBasicMaterial({color:C, transparent:true, opacity:0.8}));
  p.position.set((Math.random()-0.5)*8, (Math.random()-0.5)*8, (Math.random()-0.5)*8);
  p.userData.vel = new THREE.Vector3((Math.random()-0.5)*0.05, (Math.random()-0.5)*0.05, (Math.random()-0.5)*0.05);
  scene.add(p); particles.push(p);
}
function animateMorph(){ particles.forEach(p => { p.position.add(p.userData.vel); if (p.position.length() > 6) p.userData.vel.multiplyScalar(-1); }); updateMeasures('PARTICLES: 200<br>ENERGY: '+(particles.reduce((s,p)=>s+p.userData.vel.lengthSq(),0)).toFixed(2)+'<br>ENTROPY: '+Math.random().toFixed(3)); }
"""

MORPH_MOLECULE = """
const mol = new THREE.Group(); scene.add(mol);
const atomGeo = new THREE.SphereGeometry(0.5, 24, 24);
const O = new THREE.Mesh(atomGeo, new THREE.MeshStandardMaterial({color:0xff0000, emissive:0xff0000, emissiveIntensity:0.3}));
mol.add(O);
for (let i = 0; i < 2; i++) {
  const H = new THREE.Mesh(atomGeo, new THREE.MeshStandardMaterial({color:0xffffff})); H.scale.setScalar(0.6);
  H.position.set(Math.cos(i*Math.PI*2/2 + Math.PI/2)*1.5, 0, Math.sin(i*Math.PI*2/2 + Math.PI/2)*1.5);
  mol.add(H);
  const bond = new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.1,1.5,8), new THREE.MeshStandardMaterial({color:C}));
  bond.position.copy(H.position).multiplyScalar(0.5); bond.lookAt(H.position); bond.rotateX(Math.PI/2); mol.add(bond);
}
function animateMorph(){ mol.rotation.y += 0.01; updateMeasures('ATOMS: 3<br>BONDS: 2<br>ANGLE: 104.5°<br>RADIUS: 1.5'); }
"""

MORPH_CONCEPT = """
const concept = new THREE.Group(); scene.add(concept);
const geo = new THREE.TorusKnotGeometry(2, 0.4, 128, 16, 3, 4);
const mat = new THREE.MeshStandardMaterial({color:C, wireframe:true, emissive:C, emissiveIntensity:0.5});
const knot = new THREE.Mesh(geo, mat); concept.add(knot);
function animateMorph(){ knot.rotation.x += 0.005; knot.rotation.y += 0.01; updateMeasures('KNOT: (3,4)<br>DIMENSION: 2.7<br>ENTROPY: '+(Math.random()*0.5+0.5).toFixed(3)); }
"""

MORPH_PLANT = """
function branch(start, dir, len, depth, group) {
  if (depth <= 0) return;
  const end = start.clone().add(dir.clone().multiplyScalar(len));
  const geo = new THREE.CylinderGeometry(0.1*len/2, 0.15*len/2, len, 6);
  const mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({color:C}));
  mesh.position.copy(start.clone().add(end).multiplyScalar(0.5));
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), dir.clone().normalize());
  group.add(mesh);
  for (let i = 0; i < 2; i++) {
    const newDir = dir.clone().applyAxisAngle(new THREE.Vector3(0,0,1), (i===0?0.5:-0.5));
    branch(end, newDir, len*0.7, depth-1, group);
  }
}
const tree = new THREE.Group(); scene.add(tree);
branch(new THREE.Vector3(0,-5,0), new THREE.Vector3(0,1,0), 3, 4, tree);
function animateMorph(){ tree.rotation.y += 0.003; updateMeasures('DEPTH: 4<br>BRANCHES: '+(2**5-1)+'<br>HEIGHT: 8'); }
"""

MORPH_CODES = {
    "atom": MORPH_ATOM, "adn": MORPH_ADN, "animal": MORPH_ANIMAL,
    "humain": MORPH_HUMAN, "reseau": MORPH_NETWORK, "particule": MORPH_PARTICLE,
    "molecule": MORPH_MOLECULE, "concept": MORPH_CONCEPT, "plante": MORPH_PLANT
}

def generate(N):
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    out = root / "04_ARTIFACTS" / "morphologies"
    out.mkdir(parents=True, exist_ok=True)
    
    samples = [
        ("atome_hydrogene", "Atome d'Hydrogène", "atom", "#1f77b4", 440, "EXIST(atom) AND PART(proton, atom)"),
        ("adn_humain", "ADN Humain", "adn", "#2ca02c", 330, "LIVE(dna) AND CAUSE(dna, protein)"),
        ("cheval", "Cheval", "animal", "#8c564b", 220, "LIVE(horse) AND MOVE(horse, field)"),
        ("docteur", "Docteur", "humain", "#17becf", 554, "LIVE(doc) AND KNOW(doc, medicine) AND DO(doc, care)"),
        ("reseau_internet", "Réseau Internet", "reseau", "#9467bd", 660, "EXIST(net) AND PART(node, net)"),
        ("particule_quantique", "Particule Quantique", "particule", "#d62728", 880, "EXIST(particle) AND MOVE(particle, space)"),
        ("eau", "Eau (H2O)", "molecule", "#17becf", 523, "EXIST(water) AND PART(h, water) AND PART(o, water)"),
        ("fer", "Fer (Fe)", "molecule", "#7f7f7f", 330, "EXIST(fe) AND BIG(atom, fe)"),
        ("conscience", "Conscience", "concept", "#9467bd", 587, "THINK(mind) AND KNOW(self)"),
        ("chene", "Chêne", "plante", "#2ca02c", 294, "LIVE(oak) AND PART(root, oak)")
    ]
    
    for sp_id, name, morph, color, freq, eq in samples:
        sha = hashlib.sha256(f"{sp_id}:{eq}".encode()).hexdigest()
        code = MORPH_CODES[morph]
        html = make_html(sp_id, name, morph, color, freq, eq, sha, code)
        (out / f"{sp_id}.html").write_text(html)
        print(f"✓ {name} ({morph})")
    
    print(f"\n{len(samples)} morphologies générées dans {out}")

if __name__ == "__main__":
    generate(10)
