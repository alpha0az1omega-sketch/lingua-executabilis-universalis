import hashlib, math
from pathlib import Path

# Atom colors (CPK coloring standard)
ATOM_COLORS = {
    "H": "#ffffff", "C": "#303030", "N": "#3050f8", "O": "#ff0d0d",
    "S": "#ffff30", "P": "#ff8000", "Cl": "#1ff01f", "Na": "#ab5cf2",
    "K": "#8f40d4", "Ca": "#3dff00", "Fe": "#e06633", "Zn": "#7d80b0",
    "Mg": "#8aff00", "Cu": "#c88033", "Au": "#ffd123", "He": "#d9ffff",
    "Ne": "#b3e3f5", "Ar": "#80d1e3", "F": "#90e050", "Br": "#a62929",
    "I": "#940094", "B": "#ffb5b5", "Si": "#f0c8a0", "Se": "#ffa100"
}

# Geometries: (atom_positions_normalized)
# Each molecule: (id, name, formula, geometry_type, atoms_positions, bonds, freq, mass_molar)
MOLECULES = [
    # Diatomic (linear)
    ("H2", "Dihydrogène", "H₂", "linear", [("H",-1,0,0),("H",1,0,0)], [(0,1)], 440, 2.016),
    ("O2", "Dioxygène", "O₂", "linear", [("O",-1.2,0,0),("O",1.2,0,0)], [(0,1)], 330, 32.00),
    ("N2", "Diazote", "N₂", "linear", [("N",-1.1,0,0),("N",1.1,0,0)], [(0,1)], 294, 28.01),
    ("CO", "Monoxyde de carbone", "CO", "linear", [("C",-0.6,0,0),("O",0.6,0,0)], [(0,1)], 262, 28.01),
    ("HCl", "Acide chlorhydrique", "HCl", "linear", [("H",-0.7,0,0),("Cl",0.7,0,0)], [(0,1)], 392, 36.46),
    ("F2", "Difluor", "F₂", "linear", [("F",-0.7,0,0),("F",0.7,0,0)], [(0,1)], 523, 38.00),
    # Triatomic linear
    ("CO2", "Dioxyde de carbone", "CO₂", "linear_tri", [("C",0,0,0),("O",-1.16,0,0),("O",1.16,0,0)], [(0,1),(0,2)], 262, 44.01),
    ("HCN", "Acide cyanhydrique", "HCN", "linear_tri", [("H",-1.06,0,0),("C",0,0,0),("N",1.15,0,0)], [(0,1),(1,2)], 349, 27.03),
    # Triatomic bent (H2O type)
    ("H2O", "Eau", "H₂O", "bent", [("O",0,0.4,0),("H",-0.76,-0.3,0),("H",0.76,-0.3,0)], [(0,1),(0,2)], 523, 18.02),
    ("H2S", "Sulfure d'hydrogène", "H₂S", "bent", [("S",0,0.5,0),("H",-1.0,-0.4,0),("H",1.0,-0.4,0)], [(0,1),(0,2)], 440, 34.08),
    ("SO2", "Dioxyde de soufre", "SO₂", "bent", [("S",0,0.5,0),("O",-1.2,-0.5,0),("O",1.2,-0.5,0)], [(0,1),(0,2)], 392, 64.07),
    ("NO2", "Dioxyde d'azote", "NO₂", "bent", [("N",0,0.4,0),("O",-1.1,-0.4,0),("O",1.1,-0.4,0)], [(0,1),(0,2)], 466, 46.01),
    ("O3", "Ozone", "O₃", "bent", [("O",0,0.6,0),("O",-1.2,-0.4,0),("O",1.2,-0.4,0)], [(0,1),(0,2)], 587, 48.00),
    # Trigonal planar (120°)
    ("BF3", "Trifluorure de bore", "BF₃", "trigonal", [("B",0,0,0),("F",1.3,0,0),("F",-0.65,1.13,0),("F",-0.65,-1.13,0)], [(0,1),(0,2),(0,3)], 330, 67.81),
    ("SO3", "Trioxyde de soufre", "SO₃", "trigonal", [("S",0,0,0),("O",1.4,0,0),("O",-0.7,1.21,0),("O",-0.7,-1.21,0)], [(0,1),(0,2),(0,3)], 294, 80.06),
    ("NO3", "Nitrate", "NO₃⁻", "trigonal", [("N",0,0,0),("O",1.24,0,0),("O",-0.62,1.07,0),("O",-0.62,-1.07,0)], [(0,1),(0,2),(0,3)], 262, 62.00),
    # Tetrahedral (109.5°)
    ("CH4", "Méthane", "CH₄", "tetrahedral", [("C",0,0,0),("H",0.63,0.63,0.63),("H",-0.63,-0.63,0.63),("H",-0.63,0.63,-0.63),("H",0.63,-0.63,-0.63)], [(0,1),(0,2),(0,3),(0,4)], 440, 16.04),
    ("NH4", "Ammonium", "NH₄⁺", "tetrahedral", [("N",0,0,0),("H",0.65,0.65,0.65),("H",-0.65,-0.65,0.65),("H",-0.65,0.65,-0.65),("H",0.65,-0.65,-0.65)], [(0,1),(0,2),(0,3),(0,4)], 392, 18.04),
    ("CCl4", "Tétrachlorométhane", "CCl₄", "tetrahedral", [("C",0,0,0),("Cl",1.1,1.1,1.1),("Cl",-1.1,-1.1,1.1),("Cl",-1.1,1.1,-1.1),("Cl",1.1,-1.1,-1.1)], [(0,1),(0,2),(0,3),(0,4)], 220, 153.8),
    ("SiH4", "Silane", "SiH₄", "tetrahedral", [("Si",0,0,0),("H",0.9,0.9,0.9),("H",-0.9,-0.9,0.9),("H",-0.9,0.9,-0.9),("H",0.9,-0.9,-0.9)], [(0,1),(0,2),(0,3),(0,4)], 330, 32.12),
    # Trigonal pyramidal (107°)
    ("NH3", "Ammoniac", "NH₃", "pyramidal", [("N",0,0.5,0),("H",1.0,-0.4,0),("H",-0.5,-0.4,0.87),("H",-0.5,-0.4,-0.87)], [(0,1),(0,2),(0,3)], 466, 17.03),
    ("PH3", "Phosphine", "PH₃", "pyramidal", [("P",0,0.5,0),("H",1.1,-0.4,0),("H",-0.55,-0.4,0.95),("H",-0.55,-0.4,-0.95)], [(0,1),(0,2),(0,3)], 349, 34.00),
    # Octahedral (90°)
    ("SF6", "Hexafluorure de soufre", "SF₆", "octahedral", [("S",0,0,0),("F",1.6,0,0),("F",-1.6,0,0),("F",0,1.6,0),("F",0,-1.6,0),("F",0,0,1.6),("F",0,0,-1.6)], [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6)], 175, 146.1),
    ("PF6", "Hexafluorophosphate", "PF₆⁻", "octahedral", [("P",0,0,0),("F",1.6,0,0),("F",-1.6,0,0),("F",0,1.6,0),("F",0,-1.6,0),("F",0,0,1.6),("F",0,0,-1.6)], [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6)], 196, 145.0),
    # Small organic
    ("C2H2", "Acétylène", "C₂H₂", "linear_tri", [("H",-1.06,0,0),("C",-0.6,0,0),("C",0.6,0,0),("H",1.06,0,0)], [(0,1),(1,2),(2,3)], 392, 26.04),
    ("C2H4", "Éthylène", "C₂H₄", "planar", [("C",-0.67,0,0),("C",0.67,0,0),("H",-1.24,0.93,0),("H",-1.24,-0.93,0),("H",1.24,0.93,0),("H",1.24,-0.93,0)], [(0,1),(0,2),(0,3),(1,4),(1,5)], 440, 28.05),
    ("C2H6", "Éthane", "C₂H₆", "tetrahedral", [("C",-0.77,0,0),("C",0.77,0,0),("H",-1.2,0.9,0),("H",-1.2,-0.9,0),("H",-1.2,0,0.9),("H",1.2,0.9,0),("H",1.2,-0.9,0),("H",1.2,0,-0.9)], [(0,1),(0,2),(0,3),(0,4),(1,5),(1,6),(1,7)], 349, 30.07),
    ("CH3OH", "Méthanol", "CH₃OH", "tetrahedral", [("C",0,0,0),("H",-0.6,0.6,0.6),("H",-0.6,-0.6,0.6),("H",-0.6,0.6,-0.6),("O",1.1,0,0),("H",1.7,0.5,0)], [(0,1),(0,2),(0,3),(0,4),(4,5)], 294, 32.04),
    ("C2H5OH", "Éthanol", "C₂H₅OH", "tetrahedral", [("C",-1,0,0),("C",0,0.8,0),("O",1.2,0,0),("H",1.8,0.5,0),("H",-1.5,0.6,0),("H",-1.5,-0.6,0),("H",-1.5,0,0.6),("H",-0.3,1.4,0),("H",0.3,1.4,0)], [(0,1),(1,2),(2,3),(0,4),(0,5),(0,6),(1,7),(1,8)], 262, 46.07),
    ("CH3COOH", "Acide acétique", "CH₃COOH", "tetrahedral", [("C",-0.8,0,0),("C",0.7,0,0),("O",1.4,1,0),("O",1.4,-1,0),("H",2.0,-1.3,0),("H",-1.4,0.9,0),("H",-1.4,-0.9,0),("H",-1.4,0,0.9)], [(0,1),(1,2),(1,3),(3,4),(0,5),(0,6),(0,7)], 233, 60.05),
    ("C6H6", "Benzène", "C₆H₆", "planar_hex", [("C",1.4,0,0),("C",0.7,1.21,0),("C",-0.7,1.21,0),("C",-1.4,0,0),("C",-0.7,-1.21,0),("C",0.7,-1.21,0),("H",2.5,0,0),("H",1.25,2.16,0),("H",-1.25,2.16,0),("H",-2.5,0,0),("H",-1.25,-2.16,0),("H",1.25,-2.16,0)], [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),(0,6),(1,7),(2,8),(3,9),(4,10),(5,11)], 220, 78.11),
    ("C6H12O6", "Glucose", "C₆H₁₂O₆", "complex", [("C",0,0,0),("C",1.5,0,0),("C",1.5,1.5,0),("C",0,1.5,0),("C",-0.5,0.75,1.2),("O",0.75,0.75,1.5),("O",-1.5,0.75,0),("O",2.5,0.75,0),("O",0.75,-1,0),("O",0.75,2.5,0),("C",-0.5,-0.5,-0.5),("C",2.5,1.5,0.5)], [(0,1),(1,2),(2,3),(3,0),(0,10),(5,11),(1,8),(2,9),(3,6),(1,7),(5,4)], 165, 180.16),
    # Inorganic essentials
    ("H2O2", "Peroxyde d'hydrogène", "H₂O₂", "bent", [("O",-0.7,0,0),("O",0.7,0,0),("H",-1.1,0.7,0),("H",1.1,-0.7,0)], [(0,1),(0,2),(1,3)], 370, 34.01),
    ("N2O", "Protoxyde d'azote", "N₂O", "linear_tri", [("N",-1.1,0,0),("N",0,0,0),("O",1.1,0,0)], [(0,1),(1,2)], 294, 44.01),
    ("NO", "Monoxyde d'azote", "NO", "linear", [("N",-0.6,0,0),("O",0.6,0,0)], [(0,1)], 330, 30.01),
    ("HNO3", "Acide nitrique", "HNO₃", "planar", [("N",0,0,0),("O",1.2,0,0),("O",-0.6,1.04,0),("O",-0.6,-1.04,0),("H",-1.3,-1.4,0)], [(0,1),(0,2),(0,3),(3,4)], 262, 63.01),
    ("H2SO4", "Acide sulfurique", "H₂SO₄", "tetrahedral", [("S",0,0,0),("O",1.4,0,0),("O",-1.4,0,0),("O",0,1.4,0),("O",0,-1.4,0),("H",0.8,-2,0),("H",-0.8,-2,0)], [(0,1),(0,2),(0,3),(0,4),(4,5),(4,6)], 196, 98.08),
    ("NaOH", "Hydroxyde de sodium", "NaOH", "linear_tri", [("Na",-1.5,0,0),("O",0,0,0),("H",0.6,0.7,0)], [(0,1),(1,2)], 262, 40.00),
    ("KCl", "Chlorure de potassium", "KCl", "linear", [("K",-1.5,0,0),("Cl",1.5,0,0)], [(0,1)], 220, 74.55),
    ("NaCl", "Chlorure de sodium", "NaCl", "linear", [("Na",-1.3,0,0),("Cl",1.3,0,0)], [(0,1)], 233, 58.44),
    ("CaCO3", "Carbonate de calcium", "CaCO₃", "planar", [("Ca",0,1.5,0),("C",0,-0.3,0),("O",1.3,-0.9,0),("O",-1.3,-0.9,0),("O",0,-1.9,0)], [(0,1),(1,2),(1,3),(1,4)], 175, 100.09),
    ("Fe2O3", "Oxyde de fer(III)", "Fe₂O₃", "complex", [("Fe",-1.5,0,0),("O",0,0,0),("Fe",1.5,0,0),("O",0,1.2,0),("O",0,-1.2,0)], [(0,1),(1,2),(1,3),(1,4)], 131, 159.69),
    ("ZnO", "Oxyde de zinc", "ZnO", "linear", [("Zn",-1.1,0,0),("O",1.1,0,0)], [(0,1)], 247, 81.38),
    ("CuSO4", "Sulfate de cuivre", "CuSO₄", "tetrahedral", [("Cu",0,1.5,0),("S",0,-0.5,0),("O",1.4,-0.8,0),("O",-1.4,-0.8,0),("O",0,-1.8,0),("O",0,-0.5,-1.4)], [(0,1),(1,2),(1,3),(1,4),(1,5)], 147, 159.61),
    # Biologically relevant
    ("ATP", "Adénosine triphosphate", "ATP", "complex", [("P",0,0,0),("P",1.5,0,0),("P",3,0,0),("O",-1,0,0),("O",0.7,-1,0),("O",2.2,-1,0),("O",3.7,-0.7,0),("O",3.7,0.7,0),("O",2.2,1,0),("O",0.7,1,0)], [(0,1),(1,2),(0,3),(0,4),(1,5),(2,6),(2,7),(2,8),(1,9)], 117, 507.18),
    ("ADP", "Adénosine diphosphate", "ADP", "complex", [("P",0,0,0),("P",1.5,0,0),("O",-1,0,0),("O",0.7,-1,0),("O",2.2,-0.7,0),("O",2.2,0.7,0),("O",0.7,1,0)], [(0,1),(0,2),(0,3),(1,4),(1,5),(1,6)], 130, 427.20),
    ("Urea", "Urée", "CO(NH₂)₂", "planar", [("C",0,0,0),("O",0,1.2,0),("N",1.2,-0.7,0),("N",-1.2,-0.7,0),("H",1.2,0.5,0),("H",2,0.5,0),("H",-1.2,0.5,0),("H",-2,0.5,0)], [(0,1),(0,2),(0,3),(2,4),(2,5),(3,6),(3,7)], 196, 60.06),
    ("Creatine", "Créatine", "C₄H₉N₃O₂", "complex", [("N",0,0,0),("C",1,0.8,0),("C",2.3,0.3,0),("C",3.1,1.5,0),("N",2,2.3,0),("C",3.4,0.5,0.7),("O",4.5,0.7,0.7),("O",3.4,-0.5,0.7),("C",-1,0.8,0),("N",-1.8,0,0)], [(0,1),(1,2),(2,3),(3,4),(4,1),(2,5),(5,6),(5,7),(0,8),(8,9)], 110, 131.13),
    ("Caffeine", "Caféine", "C₈H₁₀N₄O₂", "complex", [("C",0,0,0),("N",1.3,0,0),("C",2.6,0.6,0),("N",3,2,0),("C",2,2.6,0),("N",0.7,2.4,0),("C",-0.3,1.3,0),("C",2.3,-0.7,0.7),("O",3.4,-1,0.7),("O",-0.8,2.3,0),("C",1.4,3.8,0)], [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,0),(2,7),(7,8),(5,9),(0,10)], 87, 194.19),
]

TEMPLATE = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>L.E.U. — {name}</title>
<style>
body{{margin:0;overflow:hidden;background:#0a0a0a;font-family:'Courier New',monospace}}
#matrix-bg{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0}}
#c{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1}}
#hud{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:2;pointer-events:none}}
.p{{position:absolute;background:rgba(26,26,26,0.88);border:1px solid #17becf;border-radius:8px;padding:12px 16px;color:#17becf;font-size:12px;line-height:1.6;backdrop-filter:blur(4px)}}
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
<div class="p" id="tc"><div class="n">{name}</div><div style="font-size:11px;color:#c0c0c0">{formula} · {geometry_upper}</div></div>
<div class="p" id="tl"><div class="t">Molecular Data (DNA)</div>
<div>Formula: {formula}</div>
<div>Geometry: {geometry_upper}</div>
<div>Molar Mass: {mass} g/mol</div>
<div>SHA-256: {sha}...</div></div>
<div class="p" id="tr"><div class="t">Scientific Measurements</div>
<div>ATOMS: {n_atoms}</div>
<div>BONDS: {n_bonds}</div>
<div>ANGLE: {angle}°</div>
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

// 3D
const scene=new THREE.Scene();scene.fog=new THREE.FogExp2(0x0a0a0a,0.02);
const camera=new THREE.PerspectiveCamera(60,innerWidth/innerHeight,0.1,1000);camera.position.set(0,0,12);
const renderer=new THREE.WebGLRenderer({{antialias:true,alpha:true}});renderer.setSize(innerWidth,innerHeight);
document.getElementById('c').appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0xffffff,0.6));
const pl=new THREE.PointLight(0x17becf,2,60);pl.position.set(8,8,8);scene.add(pl);

const atoms={atoms_js};
const bonds={bonds_js};
const atomColors={atom_colors_js};
const atomMeshes=[];

// Create atoms
atoms.forEach(a=>{{
    const geo=new THREE.SphereGeometry(0.5,32,32);
    const color=new THREE.Color(atomColors[a.element]||'#ffffff');
    const mat=new THREE.MeshStandardMaterial({{color:color,emissive:color,emissiveIntensity:0.3,roughness:0.4,metalness:0.2}});
    const mesh=new THREE.Mesh(geo,mat);
    mesh.position.set(a.x,a.y,a.z);
    mesh.userData={{element:a.element,baseY:a.y,phase:Math.random()*Math.PI*2}};
    scene.add(mesh);atomMeshes.push(mesh);
}});

// Create bonds
const bondGroup=new THREE.Group();scene.add(bondGroup);
bonds.forEach(b=>{{
    const a1=atoms[b[0]],a2=atoms[b[1]];
    const start=new THREE.Vector3(a1.x,a1.y,a1.z);
    const end=new THREE.Vector3(a2.x,a2.y,a2.z);
    const dir=new THREE.Vector3().subVectors(end,start);
    const len=dir.length();
    const geo=new THREE.CylinderGeometry(0.1,0.1,len,12);
    const mat=new THREE.MeshStandardMaterial({{color:0x888888,metalness:0.6,roughness:0.3}});
    const cyl=new THREE.Mesh(geo,mat);
    cyl.position.copy(start.clone().add(end).multiplyScalar(0.5));
    cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),dir.clone().normalize());
    bondGroup.add(cyl);
}});

function animate(){{
    requestAnimationFrame(animate);
    const t=Date.now()*0.001;
    atomMeshes.forEach(m=>{{m.position.y=m.userData.baseY+Math.sin(t+m.userData.phase)*0.05;}});
    scene.rotation.y+=0.003;
    renderer.render(scene,camera);
}}
animate();
function updateClock(){{document.getElementById('clock').textContent=new Date().toISOString().split('T')[1].split('.')[0];}}
setInterval(updateClock,1000);updateClock();
function playSound(freq){{var ctx=new(window.AudioContext||window.webkitAudioContext)();if(ctx.state==='suspended')ctx.resume();
var o=ctx.createOscillator(),g=ctx.createGain();o.type="sine";o.frequency.setValueAtTime(freq,ctx.currentTime);
g.gain.setValueAtTime(0.2,ctx.currentTime);o.connect(g);g.connect(ctx.destination);
o.start();o.stop(ctx.currentTime+0.6);}}
</script></body></html>'''

def generate():
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    out = root / "04_ARTIFACTS" / "molecules"
    out.mkdir(parents=True, exist_ok=True)
    
    geometry_angles = {"linear":180, "linear_tri":180, "bent":104.5, "trigonal":120,
                       "tetrahedral":109.5, "pyramidal":107, "octahedral":90,
                       "planar":120, "planar_hex":120, "complex":0}
    
    for mol_id, name, formula, geom, atoms, bonds, freq, mass in MOLECULES:
        sha = hashlib.sha256(f"{mol_id}:{formula}".encode()).hexdigest()[:32]
        atoms_js = "[" + ",".join(
            f'{{element:"{a[0]}",x:{a[1]},y:{a[2]},z:{a[3]}}}' for a in atoms
        ) + "]"
        bonds_js = "[" + ",".join(f"[{b[0]},{b[1]}]" for b in bonds) + "]"
        colors_js = "{" + ",".join(
            f'"{el}":"{ATOM_COLORS.get(el, "#ffffff")}"' for el in set(a[0] for a in atoms)
        ) + "}"
        angle = geometry_angles.get(geom, 0)
        
        html = TEMPLATE.format(
            name=name, formula=formula, geometry_upper=geom.upper(),
            mass=mass, sha=sha, n_atoms=len(atoms), n_bonds=len(bonds),
            angle=angle, freq=freq, atoms_js=atoms_js, bonds_js=bonds_js,
            atom_colors_js=colors_js
        )
        (out / f"{mol_id}.html").write_text(html)
        print(f"✓ {mol_id:10s} {formula:15s} {geom}")
    
    print(f"\n✅ {len(MOLECULES)} molecules generated in {out}")

if __name__ == "__main__":
    generate()
