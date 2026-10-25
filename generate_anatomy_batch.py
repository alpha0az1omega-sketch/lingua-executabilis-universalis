import json, hashlib, math
from pathlib import Path

TEMPLATE = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>L.E.U. — {name}</title>
<style>
body{{margin:0;overflow:hidden;background:#0a0a0a;font-family:'Courier New',monospace}}
#matrix-bg{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0}}
#c{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1}}
#hud{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:2;pointer-events:none}}
.p{{position:absolute;background:rgba(26,26,26,0.9);border:1px solid #17becf;border-radius:8px;padding:12px 16px;color:#17becf;font-size:12px;line-height:1.6;backdrop-filter:blur(4px)}}
.t{{color:#c0c0c0;font-weight:bold;letter-spacing:2px;margin-bottom:6px;font-size:11px}}
#tl{{top:20px;left:20px}} #tr{{top:20px;right:20px;text-align:right}}
#tc{{top:20px;left:50%;transform:translateX(-50%);text-align:center;padding:10px 30px}}
#tc .n{{font-size:24px;color:#17becf;letter-spacing:4px;font-weight:bold}}
#bl{{bottom:20px;left:20px;pointer-events:auto}} #br{{bottom:20px;right:20px;text-align:right}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head>
<body>
<canvas id="matrix-bg"></canvas><div id="c"></div>
<div id="hud">
<div class="p" id="tc"><div class="n">{name}</div><div style="font-size:11px;color:#c0c0c0">{type_upper} · ANATOMY</div></div>
<div class="p" id="tl"><div class="t">Anatomical Data (DNA)</div>
<div>Species: {name}</div>
<div>Systems: Skeletal, Muscular, Vascular</div>
<div>SHA-256: {sha}</div></div>
<div class="p" id="tr"><div class="t">Live Measurements</div>
<div>BONES: {bones}</div>
<div>MUSCLES: {muscles}</div>
<div>VESSELS: {vessels}</div>
<div>TIME: <span id="clock">--:--</span></div></div>
<div class="p" id="bl"><button onclick="playSound({freq})" style="background:#17becf;color:#000;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;font-weight:bold">▶ PLAY ({freq} Hz)</button></div>
<div class="p" id="br"><div class="t">Cryptographic Proof</div>
<div>GPG: 4ED4A15B...ADD1AEE</div>
<div>DOI: 10.5281/zenodo.23476518</div>
<div>STATE: SEALED</div></div>
</div>
<script>
// MATRIX
const mc=document.getElementById('matrix-bg'),mctx=mc.getContext('2d');mc.width=innerWidth;mc.height=innerHeight;
const letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';const fs=14;let cols=Math.floor(mc.width/fs);let drops=[];
for(let x=0;x<cols;x++)drops[x]=Math.random()*mc.height;
function drawMatrix(){{mctx.fillStyle='rgba(10,10,10,0.08)';mctx.fillRect(0,0,mc.width,mc.height);mctx.font=fs+'px monospace';
for(let i=0;i<drops.length;i++){{const txt=letters.charAt(Math.floor(Math.random()*letters.length));
mctx.fillStyle=Math.random()>0.7?'#d4af37':'#c0c0c0';mctx.fillText(txt,i*fs,drops[i]*fs);
if(drops[i]*fs>mc.height&&Math.random()>0.975)drops[i]=0;drops[i]++;}}}}
setInterval(drawMatrix,50);

// 3D SCENE
const scene=new THREE.Scene();scene.fog=new THREE.FogExp2(0x0a0a0a,0.02);
const camera=new THREE.PerspectiveCamera(60,innerWidth/innerHeight,0.1,1000);camera.position.set(0,0,15);
const renderer=new THREE.WebGLRenderer({{antialias:true,alpha:true}});renderer.setSize(innerWidth,innerHeight);
document.getElementById('c').appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0xffffff,0.6));
const pl=new THREE.PointLight(0x17becf,2,60);pl.position.set(8,8,8);scene.add(pl);

const group=new THREE.Group();scene.add(group);

// 1. BONES (White cylinders)
{bones_code}

// 2. MUSCLES (Red translucent capsules)
{muscles_code}

// 3. VESSELS (Blue and Red thin tubes)
{vessels_code}

function animate(){{requestAnimationFrame(animate);group.rotation.y+=0.005;renderer.render(scene,camera);}}
animate();
function updateClock(){{document.getElementById('clock').textContent=new Date().toISOString().split('T')[1].split('.')[0];}}
setInterval(updateClock,1000);updateClock();
function playSound(freq){{var ctx=new(window.AudioContext||window.webkitAudioContext)();if(ctx.state==='suspended')ctx.resume();
var o=ctx.createOscillator(),g=ctx.createGain();o.type="sine";o.frequency.setValueAtTime(freq,ctx.currentTime);
g.gain.setValueAtTime(0.2,ctx.currentTime);o.connect(g);g.connect(ctx.destination);
o.start();o.stop(ctx.currentTime+0.6);}}
</script></body></html>'''

# Horse anatomy (simplified but detailed)
BONES_HORSE = """
const boneMat = new THREE.MeshStandardMaterial({color:0xffffff, roughness:0.8});
const boneGeo = new THREE.CylinderGeometry(0.15,0.15,1,8);
// Spine
for(let i=0;i<8;i++){ const b=new THREE.Mesh(boneGeo,boneMat); b.position.set(-3.5+i,0,0); b.rotation.z=Math.PI/2; group.add(b); }
// Head
const head=new THREE.Mesh(new THREE.SphereGeometry(0.8,16,16),boneMat); head.position.set(5,1,0); group.add(head);
// Legs (4)
for(let s=0;s<4;s++){
  const x = s<2?3:-3; const z = s%2===0?1.5:-1.5;
  const leg=new THREE.Mesh(new THREE.CylinderGeometry(0.12,0.12,3,8),boneMat); leg.position.set(x,-1.5,z); group.add(leg);
}
"""
MUSCLES_HORSE = """
const muscleMat = new THREE.MeshStandardMaterial({color:0xff4444, transparent:true, opacity:0.4, roughness:0.6});
const muscleGeo = new THREE.CapsuleGeometry(0.4,1.5,4,8);
// Body muscle
const bodyMuscle=new THREE.Mesh(muscleGeo,muscleMat); bodyMuscle.position.set(0,0.2,0); bodyMuscle.rotation.z=Math.PI/2; group.add(bodyMuscle);
// Neck muscle
const neck=new THREE.Mesh(muscleGeo,muscleMat); neck.position.set(3.5,1,0); neck.rotation.z=-0.8; group.add(neck);
"""
VESSELS_HORSE = """
const arteryMat = new THREE.MeshBasicMaterial({color:0xff0000});
const veinMat = new THREE.MeshBasicMaterial({color:0x0000ff});
// Aorta (red)
const aorta = new THREE.Mesh(new THREE.CylinderGeometry(0.05,0.05,4,8), arteryMat); aorta.position.set(0,0.5,0); aorta.rotation.z=Math.PI/2; group.add(aorta);
// Vena cava (blue)
const vena = new THREE.Mesh(new THREE.CylinderGeometry(0.05,0.05,4,8), veinMat); vena.position.set(0,-0.2,0); vena.rotation.z=Math.PI/2; group.add(vena);
"""

# Tree anatomy (L-system)
BONES_TREE = """
const woodMat = new THREE.MeshStandardMaterial({color:0x8B4513, roughness:0.9});
function addBranch(pos, dir, len, depth) {
  if(depth<=0) return;
  const end = pos.clone().add(dir.clone().multiplyScalar(len));
  const geo = new THREE.CylinderGeometry(0.05*len, 0.1*len, len, 6);
  const mesh = new THREE.Mesh(geo, woodMat);
  mesh.position.copy(pos.clone().add(end).multiplyScalar(0.5));
  mesh.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), dir.clone().normalize());
  group.add(mesh);
  for(let i=0;i<2;i++){
    const newDir = dir.clone().applyAxisAngle(new THREE.Vector3(0,0,1), (i===0?0.5:-0.5));
    addBranch(end, newDir, len*0.7, depth-1);
  }
}
addBranch(new THREE.Vector3(0,-4,0), new THREE.Vector3(0,1,0), 3, 4);
"""
MUSCLES_TREE = """
// Leaves (green)
const leafMat = new THREE.MeshStandardMaterial({color:0x2ca02c, transparent:true, opacity:0.7});
const leafGeo = new THREE.SphereGeometry(0.3,8,8);
for(let i=0;i<50;i++){
  const leaf=new THREE.Mesh(leafGeo,leafMat);
  leaf.position.set((Math.random()-0.5)*6, Math.random()*6-2, (Math.random()-0.5)*6);
  group.add(leaf);
}
"""
VESSELS_TREE = """
// Sap vessels (cyan thin lines)
const sapMat = new THREE.MeshBasicMaterial({color:0x17becf});
for(let i=0;i<8;i++){
  const sap=new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.02,5,4), sapMat);
  sap.position.set((Math.random()-0.5)*2, 0, (Math.random()-0.5)*2);
  group.add(sap);
}
"""

def generate():
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    out = root / "04_ARTIFACTS" / "anatomy"
    out.mkdir(parents=True, exist_ok=True)
    
    samples = [
        ("cheval_anatomie", "Cheval (Anatomie)", "animal", "#8c564b", 220, 206, 150, 40,
         BONES_HORSE, MUSCLES_HORSE, VESSELS_HORSE),
        ("chene_anatomie", "Chêne (Anatomie)", "plant", "#2ca02c", 294, 31, 200, 16,
         BONES_TREE, MUSCLES_TREE, VESSELS_TREE)
    ]
    
    for sp_id, name, typ, color, freq, bones, muscles, vessels, b_code, m_code, v_code in samples:
        sha = hashlib.sha256(f"{sp_id}:anatomy".encode()).hexdigest()[:32]
        html = TEMPLATE.format(name=name, type_upper=typ.upper(), sha=sha,
                               bones=bones, muscles=muscles, vessels=vessels,
                               freq=freq, bones_code=b_code, muscles_code=m_code, vessels_code=v_code)
        (out / f"{sp_id}.html").write_text(html)
        print(f"✓ {name}")
    
    print(f"\n✅ Anatomies générées dans {out}")

if __name__ == "__main__":
    generate()
