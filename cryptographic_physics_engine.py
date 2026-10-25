import json
from pathlib import Path

DB_PATH = Path("genesis_db.json")
SANDBOX_PATH = Path("../04_ARTIFACTS/living/UNIFIED_FIELD.html")

def generate_unified_field():
    if not DB_PATH.exists():
        print("Erreur: genesis_db.json introuvable.")
        return

    db = json.loads(DB_PATH.read_text())
    entities = db.get("species", [])[:20] # On prend 20 entités pour le réseau
    
    js_entities = []
    
    for e in entities:
        sha = e["hash"]
        traits = e["traits"]
        
        # Couleur dictée par le SHA
        color_hex = "#" + sha[:6]
        # Masse dictée par le SHA (pour la taille)
        mass_val = (int(sha[6:8], 16) / 255.0) * 2.0 + 1.0
        # Vitesse dictée par l'ontologie
        speed = 0.08 if "MOVE" in traits else 0.02
        
        # Forme dictée par la primitive principale
        primary = traits[0]
        
        js_entities.append({
            "id": e["id"],
            "color": color_hex,
            "mass": mass_val,
            "speed": speed,
            "primary": primary,
            "equation": e["equation"],
            "traits": traits
        })

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>L.E.U. - Unified Semantic Field</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;overflow:hidden;background:#0a0a12;font-family:'Courier New',monospace;color:#e8e8e8}}
#matrix-bg{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;opacity:0.6}}
#c{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1}}
#hud{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:2;pointer-events:none}}
.p{{position:absolute;background:linear-gradient(135deg,rgba(20,20,30,0.9),rgba(5,5,15,0.9));border:1px solid #c0c0c0;border-radius:8px;padding:12px 16px;font-size:11px;line-height:1.7;backdrop-filter:blur(10px);box-shadow:0 0 30px rgba(192,192,192,0.12)}}
.t{{color:#d4af37;font-weight:bold;letter-spacing:2px;margin-bottom:6px;font-size:10px;text-transform:uppercase}}
#tl{{top:20px;left:20px;color:#17becf}}
#tr{{top:20px;right:20px;text-align:right;color:#17becf}}
.v{{color:#fff;font-weight:bold}}
.h{{color:#d4af37}}
.legend-item{{font-size:10px;margin-bottom:3px;opacity:0.8}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head>
<body>
<canvas id="matrix-bg"></canvas>
<div id="c"></div>
<div id="hud">
<div class="p" id="tl"><div class="t">Unified Semantic Field</div>
<div>Network Nodes: <span class="v" id="nodes">0</span></div>
<div>Logical Bonds: <span class="v" id="bonds">0</span></div>
<div>Physics: SHA-256 Driven</div>
<div>Status: <span class="h">STABLE</span></div>
</div>
<div class="p" id="tr"><div class="t">Ontological Map</div><div id="legend"></div></div>
</div>
<script>
// MATRIX BACKGROUND
const mc=document.getElementById('matrix-bg');
const mctx=mc.getContext('2d');
function resizeMatrix(){{mc.width=innerWidth;mc.height=innerHeight;}}
resizeMatrix();
const glyphs='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*EXISTCAUSEPART';
const mfs=14;
let mcols=Math.floor(mc.width/mfs);
let mdrops=[];
for(let i=0;i<mcols;i++)mdrops[i]=Math.random()*mc.height;
function drawMatrix(){{
  mctx.fillStyle='rgba(10,10,18,0.08)';
  mctx.fillRect(0,0,mc.width,mc.height);
  mctx.font=mfs+'px monospace';
  for(let i=0;i<mdrops.length;i++){{
    const txt=glyphs.charAt(Math.floor(Math.random()*glyphs.length));
    mctx.fillStyle=Math.random()>0.8?'#d4af37':'#c0c0c0';
    mctx.fillText(txt,i*mfs,mdrops[i]*mfs);
    if(mdrops[i]*mfs>mc.height&&Math.random()>0.975)mdrops[i]=0;
    mdrops[i]++;
  }}
}}
setInterval(drawMatrix,60);

// THREE.JS SCENE
const entitiesData = {json.dumps(js_entities)};
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
camera.position.set(0, 30, 80);
camera.lookAt(0,0,0);

const renderer = new THREE.WebGLRenderer({{ antialias:true, alpha:true }});
renderer.setClearColor(0x000000, 0);
renderer.setSize(innerWidth, innerHeight);
document.getElementById('c').appendChild(renderer.domElement);

scene.add(new THREE.AmbientLight(0xffffff, 0.4));
const pointLight = new THREE.PointLight(0xd4af37, 2, 200);
pointLight.position.set(20, 40, 20);
scene.add(pointLight);

// CENTRAL CORE (The 20 Primitives)
const coreGeo = new THREE.IcosahedronGeometry(3, 1);
const coreMat = new THREE.MeshStandardMaterial({{ color: 0xd4af37, wireframe: true, emissive: 0xd4af37, emissiveIntensity: 0.5 }});
const core = new THREE.Mesh(coreGeo, coreMat);
scene.add(core);

const nodes = [];
const nodeMeshes = [];
const legend = document.getElementById('legend');

// SHAPE FACTORY (Based on Ontology)
function createShape(primary, color) {{
    const mat = new THREE.MeshStandardMaterial({{ color: color, emissive: color, emissiveIntensity: 0.4, metalness: 0.8, roughness: 0.2 }});
    if (primary === "EXIST") return new THREE.Mesh(new THREE.IcosahedronGeometry(1, 0), mat);
    if (primary === "THINK") return new THREE.Mesh(new THREE.TorusKnotGeometry(0.8, 0.3, 64, 8, 2, 3), mat);
    if (primary === "CAUSE") return new THREE.Mesh(new THREE.ConeGeometry(1, 2, 32), mat);
    if (primary === "SEE") return new THREE.Mesh(new THREE.SphereGeometry(1, 16, 16), mat);
    if (primary === "MOVE") return new THREE.Mesh(new THREE.TetrahedronGeometry(1.2), mat);
    return new THREE.Mesh(new THREE.OctahedronGeometry(1.2), mat);
}}

// BUILD UNIVERSE
entitiesData.forEach((data, index) => {{
    const shape = createShape(data.primary, data.color);
    const angle = (index / entitiesData.length) * Math.PI * 2;
    const radius = 20 + (data.mass * 10);
    
    shape.position.x = Math.cos(angle) * radius;
    shape.position.z = Math.sin(angle) * radius;
    shape.position.y = (Math.random() - 0.5) * 20;
    
    shape.userData = {{
        speed: data.speed,
        angle: angle,
        radius: radius,
        traits: data.traits,
        id: data.id
    }};
    
    scene.add(shape);
    nodes.push(shape);
    
    // HUD Legend
    legend.innerHTML += `<div class="legend-item" style="color:${{data.color}}">${{data.id}} : ${{data.primary}}</div>`;
}});

// BUILD LOGICAL BONDS (Shared traits)
let bondCount = 0;
const bondMaterial = new THREE.LineBasicMaterial({{ color: 0x17becf, transparent: true, opacity: 0.15 }});
for(let i=0; i<nodes.length; i++) {{
    for(let j=i+1; j<nodes.length; j++) {{
        const shared = nodes[i].userData.traits.filter(t => nodes[j].userData.traits.includes(t));
        if(shared.length > 0) {{
            const geo = new THREE.BufferGeometry().setFromPoints([nodes[i].position, nodes[j].position]);
            const line = new THREE.Line(geo, bondMaterial);
            scene.add(line);
            bondCount++;
        }}
    }}
}}

document.getElementById('nodes').textContent = nodes.length;
document.getElementById('bonds').textContent = bondCount;

// ANIMATION
let time = 0;
function animate() {{
    requestAnimationFrame(animate);
    time += 0.01;
    
    core.rotation.x += 0.002;
    core.rotation.y += 0.003;
    
    nodes.forEach(node => {{
        node.userData.angle += node.userData.speed;
        node.position.x = Math.cos(node.userData.angle) * node.userData.radius;
        node.position.z = Math.sin(node.userData.angle) * node.userData.radius;
        node.position.y += Math.sin(time + node.userData.angle) * 0.05;
        node.rotation.y += 0.02;
        node.rotation.x += 0.01;
    }});
    
    // Camera slow orbit
    camera.position.x = Math.sin(time * 0.1) * 80;
    camera.position.z = Math.cos(time * 0.1) * 80;
    camera.lookAt(0,0,0);
    
    renderer.render(scene, camera);
}}
animate();

window.addEventListener('resize', () => {{
    resizeMatrix();
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
}});
</script></body></html>"""
    
    SANDBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
    SANDBOX_PATH.write_text(html)
    print(f"OK: Unified Semantic Field generee avec {len(js_entities)} entites et liaisons logiques.")
    print(f"Fichier: {SANDBOX_PATH}")

if __name__ == "__main__":
    generate_unified_field()
