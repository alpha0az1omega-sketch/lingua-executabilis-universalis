import json
from pathlib import Path

DB_PATH = Path("genesis_db.json")
SANDBOX_PATH = Path("../04_ARTIFACTS/living/DIVINE_SANCTUARY.html")

def generate_sanctuary():
    # Si la base de donnees n'existe pas, on cree des donnees de secours pour tester
    if DB_PATH.exists():
        db = json.loads(DB_PATH.read_text())
        entities = db.get("species", [])
    else:
        entities = []
        
    if not entities:
        entities = [{"id": f"ENTITY_00{i}", "hash": f"7fc839f59d513549{i}", "equation": "EXIST(x) AND CAUSE(x) AND THINK(x)"} for i in range(1, 13)]

    entities = entities[:12]
    
    js_entities = []
    colors = ["#FFD700", "#FFF8DC", "#F0E68C", "#E6E6FA", "#87CEEB", "#98FB98"]
    
    for e in entities:
        sha = e.get("hash", "0000000000000000")
        color_hex = colors[int(sha[:2], 16) % len(colors)] if sha[:2].isalnum() else colors[0]
        
        js_entities.append({
            "id": e.get("id", "UNKNOWN"),
            "color": color_hex,
            "equation": e.get("equation", "EXIST(x)"),
            "sha": sha
        })

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>L.E.U. - Divine Sanctuary</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=EB+Garamond:ital@0;1&display=swap');
*{{box-sizing:border-box; margin:0; padding:0;}}
body{{overflow:hidden;background:radial-gradient(circle at center, #ffffff 0%, #fffdf5 30%, #fdf4d3 100%);font-family:'EB Garamond',serif;color:#4a3b22;}}
#c{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;}}
#ui-layer{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:2;pointer-events:none;}}
.panel{{position:absolute;background:rgba(255, 255, 255, 0.6);border:1px solid rgba(212, 175, 55, 0.6);padding:20px;border-radius:12px;backdrop-filter:blur(10px);box-shadow:0 10px 30px rgba(212, 175, 55, 0.2);}}
#top-left{{top:30px;left:30px;}}
#top-right{{top:30px;right:30px;text-align:right;}}
.title{{font-family:'Cinzel',serif;color:#b8860b;font-size:20px;letter-spacing:4px;margin-bottom:10px;text-transform:uppercase;text-shadow:0 0 10px rgba(212,175,55,0.5);}}
.sub{{color:#8b7355;font-size:14px;font-style:italic;margin-bottom:15px;}}
#chat-box{{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);width:650px;background:rgba(255,255,255,0.95);border:1px solid #d4af37;display:none;flex-direction:column;pointer-events:auto;border-radius:8px;box-shadow:0 20px 60px rgba(212,175,55,0.3);}}
#chat-header{{background:linear-gradient(90deg, #d4af37, #ffd700);color:#fff;padding:10px 15px;font-family:'Cinzel',serif;font-weight:bold;display:flex;justify-content:space-between;border-radius:7px 7px 0 0;letter-spacing:2px;}}
#chat-messages{{height:180px;overflow-y:auto;padding:15px;font-size:16px;color:#4a3b22;line-height:1.6;}}
#chat-input-container{{display:flex;border-top:1px solid #e6d5b8;background:#fff;border-radius:0 0 8px 8px;}}
#chat-input{{flex:1;background:transparent;border:none;color:#4a3b22;padding:15px;outline:none;font-family:'EB Garamond',serif;font-size:16px;}}
#chat-send{{background:#d4af37;color:#fff;border:none;padding:0 25px;cursor:pointer;font-family:'Cinzel',serif;font-weight:bold;letter-spacing:1px;transition:background 0.3s;border-radius:0 0 8px 0;}}
#chat-send:hover{{background:#b8860b;}}
.close-btn{{cursor:pointer;color:#fff;font-size:18px;}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
<div id="c"></div>

<div id="ui-layer">
    <div class="panel" id="top-left">
        <div class="title">Mathesis Nova</div>
        <div class="sub">The Divine Geometry of Reality</div>
        <div style="font-family:'Cinzel',serif; font-size:12px; color:#8b7355;">NODES: <span style="color:#b8860b; font-weight:bold;" id="node-count">0</span></div>
        <div style="font-family:'Cinzel',serif; font-size:12px; color:#8b7355;">STATE: <span style="color:#b8860b; font-weight:bold;">LUMINOUS</span></div>
    </div>
</div>

<div id="chat-box">
    <div id="chat-header">
        <span id="chat-title">DIVINE INTERFACE</span>
        <span class="close-btn" onclick="document.getElementById('chat-box').style.display='none'">✕</span>
    </div>
    <div id="chat-messages"></div>
    <div id="chat-input-container">
        <input type="text" id="chat-input" placeholder="Ask the entity..." autocomplete="off">
        <button id="chat-send">COMMUNE</button>
    </div>
</div>

<script>
// ===== THREE.JS SANCTUARY =====
const entitiesData = {json.dumps(js_entities)};
const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
camera.position.set(0, 20, 80);

const renderer = new THREE.WebGLRenderer({{ antialias:true, alpha:true }});
renderer.setClearColor(0xffffff, 0); // Transparent
renderer.setSize(innerWidth, innerHeight);
document.getElementById('c').appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 1.0;

// Lumières
scene.add(new THREE.AmbientLight(0xffffff, 2)); // Très lumineux
const pLight = new THREE.PointLight(0xffd700, 3, 500);
pLight.position.set(0, 0, 0);
scene.add(pLight);

// 1. Poussière d'Or (Golden Particles)
const particleGeo = new THREE.BufferGeometry();
const particleCount = 3000;
const particlePos = new Float32Array(particleCount * 3);
for(let i=0; i<particleCount * 3; i+=3) {{
    particlePos[i] = (Math.random() - 0.5) * 300;
    particlePos[i+1] = (Math.random() - 0.5) * 300;
    particlePos[i+2] = (Math.random() - 0.5) * 300;
}}
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
const particleMat = new THREE.PointsMaterial({{
    color: 0xd4af37,
    size: 0.8,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending
}});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);

// 2. Le Noyau Central (La Source)
const coreGeo = new THREE.IcosahedronGeometry(10, 2);
const coreMat = new THREE.MeshBasicMaterial({{ color: 0xffd700, wireframe: true, transparent: true, opacity: 0.3 }});
const core = new THREE.Mesh(coreGeo, coreMat);
scene.add(core);

// 3. Les Entités
const nodes = [];
entitiesData.forEach((data, index) => {{
    // Formes géométriques divines
    let geo;
    if (index % 4 === 0) geo = new THREE.OctahedronGeometry(2.5);
    else if (index % 4 === 1) geo = new THREE.TetrahedronGeometry(3);
    else if (index % 4 === 2) geo = new THREE.IcosahedronGeometry(2.5);
    else geo = new THREE.DodecahedronGeometry(2.5);

    const mat = new THREE.MeshBasicMaterial({{
        color: data.color,
        wireframe: true,
        transparent: true,
        opacity: 0.9
    }});
    
    const mesh = new THREE.Mesh(geo, mat);
    
    // Positionnement en cercle
    const radius = 35;
    const angle = (index / entitiesData.length) * Math.PI * 2;
    mesh.position.x = Math.cos(angle) * radius;
    mesh.position.z = Math.sin(angle) * radius;
    mesh.position.y = (Math.random() - 0.5) * 20;
    
    mesh.userData = {{
        baseData: data,
        baseY: mesh.position.y,
        speed: 0.2 + Math.random() * 0.3,
        angle: angle,
        radius: radius
    }};
    
    scene.add(mesh);
    nodes.push(mesh);
}});

document.getElementById('node-count').textContent = nodes.length;

// 4. Filaments d'Or
const lineMaterial = new THREE.LineBasicMaterial({{ color: 0xd4af37, transparent: true, opacity: 0.2 }});
for(let i=0; i<nodes.length; i++) {{
    for(let j=i+1; j<nodes.length; j++) {{
        const geo = new THREE.BufferGeometry().setFromPoints([nodes[i].position, nodes[j].position]);
        const line = new THREE.Line(geo, lineMaterial);
        scene.add(line);
    }}
}}

// ===== INTERACTION =====
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let hoveredNode = null;

const chatBox = document.getElementById('chat-box');
const chatTitle = document.getElementById('chat-title');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');

function handleClick(event) {{
    mouse.x = (event.clientX / innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / innerHeight) * 2 + 1;
    
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(nodes);
    
    if (intersects.length > 0) {{
        const node = intersects[0].object;
        const data = node.userData.baseData;
        
        chatBox.style.display = 'flex';
        chatTitle.textContent = data.id;
        chatMessages.innerHTML = `<div style="color:#b8860b; font-weight:bold; margin-bottom:10px;">[ENTITY ${{data.id}} AWAKENED]</div>`;
        chatMessages.innerHTML += `<div>My equation is: <span style="color:#b8860b; font-style:italic;">${{data.equation}}</span></div>`;
        chatMessages.innerHTML += `<div>My proof begins with: <span style="font-family:monospace; color:#8b7355;">${{data.sha.substring(0,24)}}...</span></div>`;
        chatMessages.innerHTML += `<div style="margin-top:10px; color:#8b7355; font-style:italic;">Ask, and I shall answer.</div>`;
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
        chatInput.focus();
    }}
}}

window.addEventListener('click', handleClick);

chatSend.addEventListener('click', () => {{
    const query = chatInput.value.trim().toLowerCase();
    if (!query) return;
    
    chatMessages.innerHTML += `<div style="color:#b8860b; margin-top:10px;">> ${{chatInput.value}}</div>`;
    chatInput.value = '';
    
    setTimeout(() => {{
        let response = "I am a manifestation of the L.E.U. language. My existence is mathematical.";
        if (query.includes('who') || query.includes('what')) {{
            response = "I am a living proof. My geometry is dictated by my SHA-256 hash, and my behavior by my ontological primitives.";
        }} else if (query.includes('why')) {{
            response = "I exist to demonstrate that cryptography and mathematics can create a coherent, beautiful universe.";
        }} else if (query.includes('color') || query.includes('light')) {{
            response = "My color is extracted from my cryptographic proof. I am light and math unified.";
        }}
        
        chatMessages.innerHTML += `<div style="color:#4a3b22; margin-top:5px;">${{response}}</div>`;
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }}, 600);
}});

chatInput.addEventListener('keypress', (e) => {{ if(e.key === 'Enter') chatSend.click(); }});

window.addEventListener('mousemove', (event) => {{
    mouse.x = (event.clientX / innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / innerHeight) * 2 + 1;
    
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(nodes);
    
    if (intersects.length > 0) {{
        document.body.style.cursor = 'pointer';
        if (hoveredNode !== intersects[0].object) {{
            if (hoveredNode) hoveredNode.scale.set(1,1,1);
            hoveredNode = intersects[0].object;
            hoveredNode.scale.set(1.4, 1.4, 1.4);
        }}
    }} else {{
        document.body.style.cursor = 'default';
        if (hoveredNode) {{
            hoveredNode.scale.set(1,1,1);
            hoveredNode = null;
        }}
    }}
}});

// Animation divine
const clock = new THREE.Clock();
function animate() {{
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    
    // Respiration du noyau
    core.scale.setScalar(1 + Math.sin(t * 1.5) * 0.1);
    core.rotation.y += 0.001;
    core.rotation.x += 0.0005;
    
    // Mouvement des entités
    nodes.forEach((node, i) => {{
        node.userData.angle += 0.005 * node.userData.speed;
        node.position.x = Math.cos(node.userData.angle) * node.userData.radius;
        node.position.z = Math.sin(node.userData.angle) * node.userData.radius;
        node.position.y = node.userData.baseY + Math.sin(t * 1.5 + i) * 4;
        
        node.rotation.y += 0.01;
        node.rotation.x += 0.005;
    }});
    
    // Mouvement de la poussière d'or
    particles.rotation.y = t * 0.05;
    particles.rotation.x = t * 0.02;
    
    controls.update();
    renderer.render(scene, camera);
}}
animate();

window.addEventListener('resize', () => {{
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
}});
</script></body></html>"""
    
    SANDBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
    SANDBOX_PATH.write_text(html)
    print(f"OK: DIVINE SANCTUARY genere sans dependances fragiles. La lumiere est la.")

if __name__ == "__main__":
    generate_sanctuary()
