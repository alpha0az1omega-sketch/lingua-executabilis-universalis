import hashlib
from pathlib import Path

# Category colors
CAT_COLORS = {
    "alkali_metal": "#ff6b6b", "alkaline_earth": "#feca57", "transition_metal": "#48dbfb",
    "post_transition": "#1dd1a1", "metalloid": "#c8d6e5", "nonmetal": "#ffffff",
    "halogen": "#f368e0", "noble_gas": "#9c88ff", "lanthanide": "#54a0ff", "actinide": "#5f27cd"
}

# Periodic table: Z, Symbol, Name, Mass, Category, Shells, State
ELEMENTS = [
(1,"H","Hydrogen","1.008","nonmetal",[1],"gas"),(2,"He","Helium","4.0026","noble_gas",[2],"gas"),
(3,"Li","Lithium","6.94","alkali_metal",[2,1],"solid"),(4,"Be","Beryllium","9.0122","alkaline_earth",[2,2],"solid"),
(5,"B","Boron","10.81","metalloid",[2,3],"solid"),(6,"C","Carbon","12.011","nonmetal",[2,4],"solid"),
(7,"N","Nitrogen","14.007","nonmetal",[2,5],"gas"),(8,"O","Oxygen","15.999","nonmetal",[2,6],"gas"),
(9,"F","Fluorine","18.998","halogen",[2,7],"gas"),(10,"Ne","Neon","20.180","noble_gas",[2,8],"gas"),
(11,"Na","Sodium","22.990","alkali_metal",[2,8,1],"solid"),(12,"Mg","Magnesium","24.305","alkaline_earth",[2,8,2],"solid"),
(13,"Al","Aluminium","26.982","post_transition",[2,8,3],"solid"),(14,"Si","Silicon","28.085","metalloid",[2,8,4],"solid"),
(15,"P","Phosphorus","30.974","nonmetal",[2,8,5],"solid"),(16,"S","Sulfur","32.06","nonmetal",[2,8,6],"solid"),
(17,"Cl","Chlorine","35.45","halogen",[2,8,7],"gas"),(18,"Ar","Argon","39.948","noble_gas",[2,8,8],"gas"),
(19,"K","Potassium","39.098","alkali_metal",[2,8,8,1],"solid"),(20,"Ca","Calcium","40.078","alkaline_earth",[2,8,8,2],"solid"),
(21,"Sc","Scandium","44.956","transition_metal",[2,8,9,2],"solid"),(22,"Ti","Titanium","47.867","transition_metal",[2,8,10,2],"solid"),
(23,"V","Vanadium","50.942","transition_metal",[2,8,11,2],"solid"),(24,"Cr","Chromium","51.996","transition_metal",[2,8,13,1],"solid"),
(25,"Mn","Manganese","54.938","transition_metal",[2,8,13,2],"solid"),(26,"Fe","Iron","55.845","transition_metal",[2,8,14,2],"solid"),
(27,"Co","Cobalt","58.933","transition_metal",[2,8,15,2],"solid"),(28,"Ni","Nickel","58.693","transition_metal",[2,8,16,2],"solid"),
(29,"Cu","Copper","63.546","transition_metal",[2,8,18,1],"solid"),(30,"Zn","Zinc","65.38","transition_metal",[2,8,18,2],"solid"),
(31,"Ga","Gallium","69.723","post_transition",[2,8,18,3],"solid"),(32,"Ge","Germanium","72.630","metalloid",[2,8,18,4],"solid"),
(33,"As","Arsenic","74.922","metalloid",[2,8,18,5],"solid"),(34,"Se","Selenium","78.971","nonmetal",[2,8,18,6],"solid"),
(35,"Br","Bromine","79.904","halogen",[2,8,18,7],"liquid"),(36,"Kr","Krypton","83.798","noble_gas",[2,8,18,8],"gas"),
(37,"Rb","Rubidium","85.468","alkali_metal",[2,8,18,8,1],"solid"),(38,"Sr","Strontium","87.62","alkaline_earth",[2,8,18,8,2],"solid"),
(39,"Y","Yttrium","88.906","transition_metal",[2,8,18,9,2],"solid"),(40,"Zr","Zirconium","91.224","transition_metal",[2,8,18,10,2],"solid"),
(41,"Nb","Niobium","92.906","transition_metal",[2,8,18,12,1],"solid"),(42,"Mo","Molybdenum","95.95","transition_metal",[2,8,18,13,1],"solid"),
(43,"Tc","Technetium","98","transition_metal",[2,8,18,13,2],"solid"),(44,"Ru","Ruthenium","101.07","transition_metal",[2,8,18,15,1],"solid"),
(45,"Rh","Rhodium","102.91","transition_metal",[2,8,18,16,1],"solid"),(46,"Pd","Palladium","106.42","transition_metal",[2,8,18,18],"solid"),
(47,"Ag","Silver","107.87","transition_metal",[2,8,18,18,1],"solid"),(48,"Cd","Cadmium","112.41","transition_metal",[2,8,18,18,2],"solid"),
(49,"In","Indium","114.82","post_transition",[2,8,18,18,3],"solid"),(50,"Sn","Tin","118.71","post_transition",[2,8,18,18,4],"solid"),
(51,"Sb","Antimony","121.76","metalloid",[2,8,18,18,5],"solid"),(52,"Te","Tellurium","127.60","metalloid",[2,8,18,18,6],"solid"),
(53,"I","Iodine","126.90","halogen",[2,8,18,18,7],"solid"),(54,"Xe","Xenon","131.29","noble_gas",[2,8,18,18,8],"gas"),
(55,"Cs","Caesium","132.91","alkali_metal",[2,8,18,18,8,1],"solid"),(56,"Ba","Barium","137.33","alkaline_earth",[2,8,18,18,8,2],"solid"),
(57,"La","Lanthanum","138.91","lanthanide",[2,8,18,18,9,2],"solid"),(58,"Ce","Cerium","140.12","lanthanide",[2,8,18,19,9,2],"solid"),
(59,"Pr","Praseodymium","140.91","lanthanide",[2,8,18,21,8,2],"solid"),(60,"Nd","Neodymium","144.24","lanthanide",[2,8,18,22,8,2],"solid"),
(61,"Pm","Promethium","145","lanthanide",[2,8,18,23,8,2],"solid"),(62,"Sm","Samarium","150.36","lanthanide",[2,8,18,24,8,2],"solid"),
(63,"Eu","Europium","151.96","lanthanide",[2,8,18,25,8,2],"solid"),(64,"Gd","Gadolinium","157.25","lanthanide",[2,8,18,25,9,2],"solid"),
(65,"Tb","Terbium","158.93","lanthanide",[2,8,18,27,8,2],"solid"),(66,"Dy","Dysprosium","162.50","lanthanide",[2,8,18,28,8,2],"solid"),
(67,"Ho","Holmium","164.93","lanthanide",[2,8,18,29,8,2],"solid"),(68,"Er","Erbium","167.26","lanthanide",[2,8,18,30,8,2],"solid"),
(69,"Tm","Thulium","168.93","lanthanide",[2,8,18,31,8,2],"solid"),(70,"Yb","Ytterbium","173.05","lanthanide",[2,8,18,32,8,2],"solid"),
(71,"Lu","Lutetium","174.97","lanthanide",[2,8,18,32,9,2],"solid"),(72,"Hf","Hafnium","178.49","transition_metal",[2,8,18,32,10,2],"solid"),
(73,"Ta","Tantalum","180.95","transition_metal",[2,8,18,32,11,2],"solid"),(74,"W","Tungsten","183.84","transition_metal",[2,8,18,32,12,2],"solid"),
(75,"Re","Rhenium","186.21","transition_metal",[2,8,18,32,13,2],"solid"),(76,"Os","Osmium","190.23","transition_metal",[2,8,18,32,14,2],"solid"),
(77,"Ir","Iridium","192.22","transition_metal",[2,8,18,32,15,2],"solid"),(78,"Pt","Platinum","195.08","transition_metal",[2,8,18,32,17,1],"solid"),
(79,"Au","Gold","196.97","transition_metal",[2,8,18,32,18,1],"solid"),(80,"Hg","Mercury","200.59","transition_metal",[2,8,18,32,18,2],"liquid"),
(81,"Tl","Thallium","204.38","post_transition",[2,8,18,32,18,3],"solid"),(82,"Pb","Lead","207.2","post_transition",[2,8,18,32,18,4],"solid"),
(83,"Bi","Bismuth","208.98","post_transition",[2,8,18,32,18,5],"solid"),(84,"Po","Polonium","209","post_transition",[2,8,18,32,18,6],"solid"),
(85,"At","Astatine","210","halogen",[2,8,18,32,18,7],"solid"),(86,"Rn","Radon","222","noble_gas",[2,8,18,32,18,8],"gas"),
(87,"Fr","Francium","223","alkali_metal",[2,8,18,32,18,8,1],"solid"),(88,"Ra","Radium","226","alkaline_earth",[2,8,18,32,18,8,2],"solid"),
(89,"Ac","Actinium","227","actinide",[2,8,18,32,18,9,2],"solid"),(90,"Th","Thorium","232.04","actinide",[2,8,18,32,18,10,2],"solid"),
(91,"Pa","Protactinium","231.04","actinide",[2,8,18,32,20,9,2],"solid"),(92,"U","Uranium","238.03","actinide",[2,8,18,32,21,9,2],"solid"),
(93,"Np","Neptunium","237","actinide",[2,8,18,32,22,9,2],"solid"),(94,"Pu","Plutonium","244","actinide",[2,8,18,32,24,8,2],"solid"),
(95,"Am","Americium","243","actinide",[2,8,18,32,25,8,2],"solid"),(96,"Cm","Curium","247","actinide",[2,8,18,32,25,9,2],"solid"),
(97,"Bk","Berkelium","247","actinide",[2,8,18,32,27,8,2],"solid"),(98,"Cf","Californium","251","actinide",[2,8,18,32,28,8,2],"solid"),
(99,"Es","Einsteinium","252","actinide",[2,8,18,32,29,8,2],"solid"),(100,"Fm","Fermium","257","actinide",[2,8,18,32,30,8,2],"solid"),
(101,"Md","Mendelevium","258","actinide",[2,8,18,32,31,8,2],"solid"),(102,"No","Nobelium","259","actinide",[2,8,18,32,32,8,2],"solid"),
(103,"Lr","Lawrencium","266","actinide",[2,8,18,32,32,8,3],"solid"),(104,"Rf","Rutherfordium","267","transition_metal",[2,8,18,32,32,10,2],"solid"),
(105,"Db","Dubnium","268","transition_metal",[2,8,18,32,32,11,2],"solid"),(106,"Sg","Seaborgium","269","transition_metal",[2,8,18,32,32,12,2],"solid"),
(107,"Bh","Bohrium","270","transition_metal",[2,8,18,32,32,13,2],"solid"),(108,"Hs","Hassium","269","transition_metal",[2,8,18,32,32,14,2],"solid"),
(109,"Mt","Meitnerium","278","transition_metal",[2,8,18,32,32,15,2],"solid"),(110,"Ds","Darmstadtium","281","transition_metal",[2,8,18,32,32,16,2],"solid"),
(111,"Rg","Roentgenium","282","transition_metal",[2,8,18,32,32,17,2],"solid"),(112,"Cn","Copernicium","285","transition_metal",[2,8,18,32,32,18,2],"solid"),
(113,"Nh","Nihonium","286","post_transition",[2,8,18,32,32,18,3],"solid"),(114,"Fl","Flerovium","289","post_transition",[2,8,18,32,32,18,4],"solid"),
(115,"Mc","Moscovium","290","post_transition",[2,8,18,32,32,18,5],"solid"),(116,"Lv","Livermorium","293","post_transition",[2,8,18,32,32,18,6],"solid"),
(117,"Ts","Tennessine","294","halogen",[2,8,18,32,32,18,7],"solid"),(118,"Og","Oganesson","294","noble_gas",[2,8,18,32,32,18,8],"solid")
]

TEMPLATE = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>L.E.U. — {symbol} ({name})</title>
<style>
body{{margin:0;overflow:hidden;background:#0a0a0a;font-family:'Courier New',monospace}}
#matrix-bg{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0}}
#c{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1}}
#hud{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:2;pointer-events:none}}
.p{{position:absolute;background:rgba(26,26,26,0.88);border:1px solid {color};border-radius:8px;padding:12px 16px;color:{color};font-size:12px;line-height:1.6;backdrop-filter:blur(4px)}}
.t{{color:#c0c0c0;font-weight:bold;letter-spacing:2px;margin-bottom:6px;font-size:11px}}
#tl{{top:20px;left:20px}} #tr{{top:20px;right:20px;text-align:right}}
#tc{{top:20px;left:50%;transform:translateX(-50%);text-align:center;padding:10px 30px}}
#tc .n{{font-size:28px;color:{color};letter-spacing:4px;font-weight:bold}}
#bl{{bottom:20px;left:20px;pointer-events:auto}} #br{{bottom:20px;right:20px;text-align:right}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head>
<body>
<canvas id="matrix-bg"></canvas><div id="c"></div>
<div id="hud">
<div class="p" id="tc"><div class="n">{symbol} — {name}</div><div style="font-size:11px;color:#c0c0c0">Z={z} · {category_upper} · {state_upper}</div></div>
<div class="p" id="tl"><div class="t">Atomic Data (DNA)</div>
<div>Z: {z} | Mass: {mass} u</div>
<div>Shells: {shells_str}</div>
<div>Electrons: {electrons}</div>
<div>SHA-256: {sha}</div></div>
<div class="p" id="tr"><div class="t">Scientific Measurements</div>
<div>PROTONS: {z}</div>
<div>NEUTRONS: {neutrons}</div>
<div>ELECTRONS: {electrons}</div>
<div>MASS: {mass_kg} kg</div>
<div>TIME: <span id="clock">--:--</span></div></div>
<div class="p" id="bl"><button onclick="playSound({freq})" style="background:{color};color:#000;border:none;padding:8px 16px;border-radius:4px;cursor:pointer;font-weight:bold">▶ PLAY ({freq} Hz)</button></div>
<div class="p" id="br"><div class="t">Cryptographic Proof</div>
<div>GPG: 4ED4A15B...ADD1AEE</div>
<div>DOI: 10.5281/zenodo.23476518</div>
<div>STATE: SEALED</div></div>
</div>
<script>
// MATRIX BACKGROUND
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
const camera=new THREE.PerspectiveCamera(60,innerWidth/innerHeight,0.1,1000);camera.position.z=18;
const renderer=new THREE.WebGLRenderer({{antialias:true,alpha:true}});renderer.setSize(innerWidth,innerHeight);
document.getElementById('c').appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0xffffff,0.5));
const pl=new THREE.PointLight({color_hex},2,60);pl.position.set(8,8,8);scene.add(pl);
const C={color_hex};

// NUCLEUS (protons + neutrons cluster)
const nucleusGroup=new THREE.Group();scene.add(nucleusGroup);
const protonGeo=new THREE.SphereGeometry(0.35,16,16);
const protonMat=new THREE.MeshStandardMaterial({{color:0xff3333,emissive:0xff3333,emissiveIntensity:0.5}});
const neutronMat=new THREE.MeshStandardMaterial({{color:0x3333ff,emissive:0x3333ff,emissiveIntensity:0.5}});
const totalNucleons=Math.min({z}+{neutrons},30); // Limit for performance
const protonsToShow=Math.round({z}/({z}+{neutrons})*totalNucleons);
for(let i=0;i<totalNucleons;i++){{
    const isProton=i<protonsToShow;
    const sphere=new THREE.Mesh(protonGeo,isProton?protonMat:neutronMat);
    const phi=Math.acos(1-2*(i+0.5)/totalNucleons);
    const theta=Math.PI*(1+Math.sqrt(5))*i;
    const r=0.8*Math.cbrt(totalNucleons)*0.4;
    sphere.position.set(r*Math.sin(phi)*Math.cos(theta),r*Math.sin(phi)*Math.sin(theta),r*Math.cos(phi));
    nucleusGroup.add(sphere);
}}

// ELECTRON SHELLS
const shellArrays={shells_js};
const shellGroup=new THREE.Group();scene.add(shellGroup);
const electronGeo=new THREE.SphereGeometry(0.15,8,8);
const electronMat=new THREE.MeshStandardMaterial({{color:0xffff00,emissive:0xffff00,emissiveIntensity:0.8}});
shellArrays.forEach((count,shellIdx)=>{{
    const radius=2.5+shellIdx*1.2;
    const ringGeo=new THREE.TorusGeometry(radius,0.02,8,100);
    const ring=new THREE.Mesh(ringGeo,new THREE.MeshBasicMaterial({{color:C,transparent:true,opacity:0.3}}));
    ring.rotation.x=Math.PI/2+shellIdx*0.2;
    shellGroup.add(ring);
    for(let e=0;e<Math.min(count,8);e++){{
        const electron=new THREE.Mesh(electronGeo,electronMat);
        const angle=(e/Math.min(count,8))*Math.PI*2;
        electron.position.set(radius*Math.cos(angle),radius*Math.sin(angle)*0.3,radius*Math.sin(angle));
        electron.userData={{shell:shellIdx,angle:angle,radius:radius}};
        shellGroup.add(electron);
    }}
}});

function animate(){{
    requestAnimationFrame(animate);
    nucleusGroup.rotation.y+=0.005;
    shellGroup.children.forEach(child=>{{
        if(child.userData&&child.userData.radius){{
            child.userData.angle+=0.01*(child.userData.shell+1);
            const r=child.userData.radius;
            child.position.set(r*Math.cos(child.userData.angle),r*Math.sin(child.userData.angle)*0.3,r*Math.sin(child.userData.angle));
        }}
    }});
    renderer.render(scene,camera);
}}
animate();

function updateClock(){{document.getElementById('clock').textContent=new Date().toISOString().split('T')[1].split('.')[0];}}
setInterval(updateClock,1000);updateClock();
function playSound(freq){{var ctx=new(window.AudioContext||window.webkitAudioContext)();if(ctx.state==='suspended')ctx.resume();
var o=ctx.createOscillator(),g=ctx.createGain();o.type="sine";o.frequency.setValueAtTime(freq,ctx.currentTime);
g.gain.setValueAtTime(0.2,ctx.currentTime);o.connect(g);g.connect(document.body.appendChild(document.createElement('audio'))||ctx.destination);
o.start();o.stop(ctx.currentTime+0.6);}}
</script></body></html>'''

def generate():
    root = Path.home() / "ALPHA_ARCHIVE_000_2026-10-17_UNIVERSAL_EXECUTABLE_LANGUAGE"
    out = root / "04_ARTIFACTS" / "elements"
    out.mkdir(parents=True, exist_ok=True)
    
    for z, symbol, name, mass, category, shells, state in ELEMENTS:
        color = CAT_COLORS.get(category, "#ffffff")
        electrons = sum(shells)
        neutrons = round(float(mass)) - z
        if neutrons < 0: neutrons = 0
        mass_kg = f"{float(mass) * 1.66054e-27:.4e}"
        freq = 100 + z * 10
        sha = hashlib.sha256(f"{symbol}:{name}:{z}".encode()).hexdigest()[:32]
        color_hex = color.replace("#", "0x")
        shells_str = str(shells)
        shells_js = "[" + ",".join(str(s) for s in shells) + "]"
        
        html = TEMPLATE.format(
            symbol=symbol, name=name, z=z, mass=mass, category_upper=category.upper(),
            state_upper=state.upper(), shells_str=shells_str, electrons=electrons,
            sha=sha, neutrons=neutrons, mass_kg=mass_kg, freq=freq, color=color,
            color_hex=color_hex, shells_js=shells_js
        )
        (out / f"{z:03d}_{symbol}.html").write_text(html)
        print(f"✓ {z:3d} {symbol:3s} {name}")
    
    print(f"\n✅ {len(ELEMENTS)} elements generated in {out}")

if __name__ == "__main__":
    generate()
