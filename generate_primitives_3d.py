import json, hashlib
from pathlib import Path

TEMPLATE = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>L.E.U. — {pid}</title>
<style>
body{{margin:0;overflow:hidden;background:#0a0a0a;font-family:'Courier New',monospace}}
#matrix-bg{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0}}
#c{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1}}
#hud{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:2;pointer-events:none}}
.p{{position:absolute;background:rgba(26,26,26,0.9);border:2px solid {color};border-radius:8px;padding:12px 16px;color:{color};font-size:12px;line-height:1.6}}
.t{{color:#c0c0c0;font-weight:bold;letter-spacing:2px;margin-bottom:6px;font-size:11px}}
#tc{{top:20px;left:50%;transform:translateX(-50%);text-align:center;padding:12px 40px}}
#tc .n{{font-size:32px;color:{color};letter-spacing:4px;font-weight:bold}}
#tl{{top:20px;left:20px}} #tr{{top:20px;right:20px;text-align:right}}
#bl{{bottom:20px;left:20px;pointer-events:auto}} #br{{bottom:20px;right:20px;text-align:right}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head>
<body>
<canvas id="matrix-bg"></canvas><div id="c"></div>
<div id="hud">
<div class="p" id="tc"><div class="n">{pid}</div><div style="font-size:11px;color:#c0c0c0">LAYER {layer} · {formal}</div></div>
<div class="p" id="tl"><div class="t">Cryptographic Proof</div>
<div>SHA-256: {sha}...</div>
<div>GPG: 4ED4A15B...ADD1AEE</div>
<div>DOI: 10.5281/zenodo.23476518</div></div>
<div class="p" id="tr"><div class="t">Live Telemetry</div>
<div>TIME: <span id="clock">--:--</span></div>
<div>STATE: SEALED</div><div>FPS: <span id="fps">--</span></div></div>
<div class="p" id="bl"><button onclick="playSound({freq})" style="background:{color};color:#000;border:none;padding:10px 20px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:14px">▶ PLAY ({freq} Hz)</button></div>
<div class="p" id="br"><div class="t">Measurements</div>
<div>ATOMS: 20</div><div>ENERGY: <span id="energy">0</span></div><div>COHERENCE: <span id="coherence">0</span></div></div>
</div>
<script>
const mc=document.getElementById('matrix-bg'),mctx=mc.getContext('2d');mc.width=innerWidth;mc.height=innerHeight;
const letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';const fs=14;let cols=Math.floor(mc.width/fs);let drops=[];
for(let x=0;x<cols;x++)drops[x]=Math.random()*mc.height;
function drawMatrix(){{mctx.fillStyle='rgba(10,10,10,0.08)';mctx.fillRect(0,0,mc.width,mc.height);mctx.font=fs+'px monospace';
for(let i=0;i<drops.length;i++){{const txt=letters.charAt(Math.floor(Math.random()*letters.length));
mctx.fillStyle=Math.random()>0.7?'#d4af37':'#c0c0c0';mctx.fillText(txt,i*fs,drops[i]*fs);
if(drops[i]*fs>mc.height&&Math.random()>0.975)drops[i]=0;drops[i]++;}}}}
setInterval(drawMatrix,50);

const scene=new THREE.Scene();scene.fog=new THREE.FogExp2(0x0a0a0a,0.02);
const camera=new THREE.PerspectiveCamera(60,innerWidth/innerHeight,0.1,1000);camera.position.set(0,0,15);
const renderer=new THREE.WebGLRenderer({{antialias:true,alpha:true}});renderer.setSize(innerWidth,innerHeight);
document.getElementById('c').appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0xffffff,0.5));
const pl=new THREE.PointLight({color_hex},2,60);pl.position.set(8,8,8);scene.add(pl);
const C={color_hex};

// Central glyph (icosahedron wireframe with {pid} letter inside)
const geo=new THREE.IcosahedronGeometry(4,1);
const mat=new THREE.MeshStandardMaterial({{color:C,wireframe:true,emissive:C,emissiveIntensity:0.6}});
const glyph=new THREE.Mesh(geo,mat);scene.add(glyph);

// 20 electrons orbiting
const electrons=[];const eGeo=new THREE.SphereGeometry(0.25,16,16);
for(let i=0;i<20;i++){{
const e=new THREE.Mesh(eGeo,new THREE.MeshStandardMaterial({{color:0xffffff,emissive:0xffffff,emissiveIntensity:0.8}}));
e.userData={{angle:(i/20)*Math.PI*2,speed:0.01+i*0.001,radius:6+Math.random()*1}};
scene.add(e);electrons.push(e);
}}

// Stars
const starGeo=new THREE.BufferGeometry();const starPos=new Float32Array(600*3);
for(let i=0;i<600*3;i++)starPos[i]=(Math.random()-0.5)*200;
starGeo.setAttribute('position',new THREE.BufferAttribute(starPos,3));
scene.add(new THREE.Points(starGeo,new THREE.PointsMaterial({{size:0.15,color:0xc0c0c0}})));

let lastFrame=performance.now(),frames=0;
function animate(){{
requestAnimationFrame(animate);
glyph.rotation.x+=0.005;glyph.rotation.y+=0.01;
const t=Date.now()*0.001;
electrons.forEach(e=>{{e.userData.angle+=e.userData.speed;const r=e.userData.radius;
e.position.set(Math.cos(e.userData.angle)*r,Math.sin(e.userData.angle)*r*0.5,Math.sin(e.userData.angle)*r);}});
const now=performance.now();frames++;
if(now-lastFrame>1000){{document.getElementById('fps').textContent=frames;frames=0;lastFrame=now;}}
document.getElementById('energy').textContent=(electrons.reduce((s,e)=>s+e.userData.speed*e.userData.speed,0)*10000).toFixed(2);
document.getElementById('coherence').textContent=(0.7+0.2*Math.sin(t*0.1)).toFixed(3);
renderer.render(scene,camera);
}}
animate();
function updateClock(){{document.getElementById('clock').textContent=new Date().toISOString().split('T')[1].split('.')[0];}}
setInterval(updateClock,1000);updateClock();
function playSound(freq){{var ctx=new(window.AudioContext||window.webkitAudioContext)();if(ctx.state==='suspended')ctx.resume();
var o=ctx.createOscillator(),g=ctx.createGain();o.type="sine";o.frequency.setValueAtTime(freq,ctx.currentTime);
g.gain.setValueAtTime(0.2,ctx.currentTime);o.connect(g);g.connect(ctx.destination);
o.start();o.stop(ctx.currentTime+0.8);}}
</script></body></html>'''

COLORS = ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf","#aec7e8","#ffbb78","#98df8a","#ff9896","#c5b0d5","#c49c94","#f7b6d2","#c7c7c7","#dbdb8d","#9edae5"]

def generate():
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    lexicon = json.loads((root / "01_SPECIFICATION" / "primitive_lexicon.json").read_text())
    out = root / "04_ARTIFACTS" / "primitives_3d"
    out.mkdir(parents=True, exist_ok=True)
    for i, p in enumerate(lexicon["primitives"]):
        pid = p["id"]; layer = p["layer"]; formal = p["formal"]
        son = p["sonification"]
        freq = son.get("freq_hz", son.get("freq_start", 440))
        if isinstance(freq, list): freq = freq[0]
        color = COLORS[i % len(COLORS)]
        sha = hashlib.sha256(f"{pid}:{formal}".encode()).hexdigest()[:48]
        html = TEMPLATE.format(pid=pid, layer=layer, formal=formal, sha=sha,
                                freq=freq, color=color, color_hex=color.replace("#","0x"))
        (out / f"{pid}.html").write_text(html)
        print(f"✓ {pid}")
    print(f"\n✅ 20 primitives 3D générées dans {out}")

if __name__ == "__main__":
    generate()
