import json
from pathlib import Path

DB_PATH = Path("genesis_db.json")
SANDBOX_PATH = Path("../04_ARTIFACTS/living/NEXUS_CORE.html")

def generate_nexus():
    if not DB_PATH.exists():
        print("Erreur: genesis_db.json introuvable.")
        return

    db = json.loads(DB_PATH.read_text())
    entities = db.get("species", [])[:15]
    
    js_entities = []
    for e in entities:
        sha = e["hash"]
        traits = e["traits"]
        color_hex = "#" + sha[:6]
        
        js_entities.append({
            "id": e["id"],
            "color": color_hex,
            "equation": e["equation"],
            "traits": traits,
            "sha": sha
        })

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>L.E.U. - Nexus Core</title>
<style>
*{{box-sizing:border-box; margin:0; padding:0;}}
body{{overflow:hidden;background:#050505;font-family:'Courier New',monospace;color:#e8e8e8;}}
#bg-canvas{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;}}
#c{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:1;}}
#ui-layer{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:2;pointer-events:none;}}
.panel{{position:absolute;background:rgba(10,15,25,0.85);border:1px solid #c0c0c0;padding:15px;border-radius:5px;backdrop-filter:blur(5px);box-shadow:0 0 20px rgba(192,192,192,0.2);}}
#top-left{{top:20px;left:20px;}}
#top-right{{top:20px;right:20px;text-align:right;}}
.title{{color:#d4af37;font-size:14px;letter-spacing:3px;margin-bottom:10px;text-transform:uppercase;text-shadow:0 0 10px #d4af37;}}
.sub{{color:#17becf;font-size:11px;margin-bottom:5px;}}
#chat-box{{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);width:600px;background:rgba(5,5,10,0.9);border:1px solid #17becf;display:none;flex-direction:column;pointer-events:auto;}}
#chat-header{{background:#17becf;color:#000;padding:5px 10px;font-weight:bold;display:flex;justify-content:space-between;}}
#chat-messages{{height:150px;overflow-y:auto;padding:10px;font-size:12px;color:#c0c0c0;}}
#chat-input-container{{display:flex;border-top:1px solid #333;}}
#chat-input{{flex:1;background:transparent;border:none;color:#fff;padding:10px;outline:none;font-family:inherit;}}
#chat-send{{background:#17becf;color:#000;border:none;padding:0 15px;cursor:pointer;font-weight:bold;}}
.close-btn{{cursor:pointer;color:#000;}}
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
<canvas id="bg-canvas"></canvas>
<div id="c"></div>

<div id="ui-layer">
    <div class="panel" id="top-left">
        <div class="title">NEXUS CORE</div>
        <div class="sub">Ontological Projection</div>
        <div>Nodes: <span style="color:#fff" id="node-count">0</span></div>
        <div>State: <span style="color:#d4af37">EXECUTING</span></div>
        <div style="font-size:10px;margin-top:10px;color:#666;">Scroll to zoom · Click entity to converse</div>
    </div>
    <div class="panel" id="top-right">
        <div class="title">CRYPTOGRAPHIC PROOF</div>
        <div style="font-size:10px;color:#888;word-break:break-all;width:250px;" id="proof-text">
            SHA-256: ACTIVE <br> GPG: 4ED4A15B... <br> DOI: 10.5281/zenodo...
        </div>
    </div>
</div>

<div id="chat-box">
    <div id="chat-header">
        <span id="chat-title">ENTITY INTERFACE</span>
        <span class="close-btn" onclick="document.getElementById('chat-box').style.display='none'">✕</span>
    </div>
    <div id="chat-messages"></div>
    <div id="chat-input-container">
        <input type="text" id="chat-input" placeholder="Ask the entity..." autocomplete="off">
        <button id="chat-send">SEND</button>
    </div>
</div>

<script>
// ===== 1. SILVER/GOLD MATRIX COSMOS BACKGROUND =====
const bgCanvas = document.getElementById('bg-canvas');
const bgCtx = bgCanvas.getContext('2d');
function resizeBg(){{ bgCanvas.width = innerWidth; bgCanvas.height = innerHeight; }}
resizeBg();

const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*';
const fontSize = 14;
let columns = Math.floor(bgCanvas.width / fontSize);
let drops = [];
for(let x=0; x<columns; x++) drops[x] = Math.random() * bgCanvas.height;

function drawBg() {{
    bgCtx.fillStyle = 'rgba(10, 10, 15, 0.1)';
    bgCtx.fillRect(0, 0, bgCanvas.width, bgCanvas.height);
    bgCtx.font = fontSize + 'px monospace';
    
    for(let i=0; i<drops.length; i++) {{
        const text = chars.charAt(Math.floor(Math.random() * chars.length));
        bgCtx.fillStyle = Math.random() > 0.85 ? '#d4af37' : '#a0a0b0';
        bgCtx.fillText(text, i * fontSize, drops[i] * fontSize);
        
        if(drops[i] * fontSize > bgCanvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
    }}
}}
setInterval(drawBg, 50);

// ===== 2. THREE.JS NEXUS =====
const entitiesData = {json.dumps(js_entities)};
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x050505, 0.005);

const camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
camera.position.set(0, 20, 60);

const renderer = new THREE.WebGLRenderer({{ antialias:true, alpha:true }});
renderer.setClearColor(0x000000, 0);
renderer.setSize(innerWidth, innerHeight);
document.getElementById('c').appendChild(renderer.domElement);

const renderScene = new THREE.RenderPass(scene, camera);
const bloomPass = new THREE.UnrealBloomPass(new THREE.Vector2(innerWidth, innerHeight), 1.5, 0.4, 0.85);
const composer = new THREE.EffectComposer(renderer);
composer.addPass(renderScene);
composer.addPass(bloomPass);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.5;
controls.maxDistance = 200;
controls.minDistance = 10;

scene.add(new THREE.AmbientLight(0xffffff, 0.3));
const pLight = new THREE.PointLight(0xd4af37, 2, 300);
pLight.position.set(0, 0, 0);
scene.add(pLight);

function createQRTexture(hash) {{
    const canvas = document.createElement('canvas');
    canvas.width = 64; canvas.height = 64;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#000'; ctx.fillRect(0,0,64,64);
    ctx.fillStyle = '#fff';
    for(let i=0; i<64; i+=4) {{
        for(let j=0; j<64; j+=4) {{
            const charCode = hash.charCodeAt((i+j)%hash.length);
            if(charCode % 2 === 0) ctx.fillRect(i, j, 4, 4);
        }}
    }}
    const tex = new THREE.CanvasTexture(canvas);
    tex.magFilter = THREE.NearestFilter;
    return tex;
}}

const nodes = [];
entitiesData.forEach((data, index) => {{
    const geo = new THREE.IcosahedronGeometry(2, 2);
    const tex = createQRTexture(data.sha);
    const mat = new THREE.MeshStandardMaterial({{
        color: data.color,
        map: tex,
        emissive: data.color,
        emissiveMap: tex,
        emissiveIntensity: 1.5,
        metalness: 0.9,
        roughness: 0.1,
        transparent: true,
        opacity: 0.9
    }});
    
    const mesh = new THREE.Mesh(geo, mat);
    const phi = Math.acos(1 - 2 * (index + 0.5) / entitiesData.length);
    const theta = Math.PI * (1 + Math.sqrt(5)) * index;
    const radius = 25;
    
    mesh.position.set(
        Math.cos(theta) * Math.sin(phi) * radius,
        Math.sin(theta) * Math.sin(phi) * radius,
        Math.cos(phi) * radius
    );
    
    mesh.userData = data;
    scene.add(mesh);
    nodes.push(mesh);
}});

document.getElementById('node-count').textContent = nodes.length;

// ===== 3. CONVERSATIONAL INTERACTION =====
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
        const data = node.userData;
        
        chatBox.style.display = 'flex';
        chatTitle.textContent = data.id;
        chatTitle.style.color = data.color;
        chatBox.style.borderColor = data.color;
        
        chatMessages.innerHTML = `<div style="color:${{data.color}}; margin-bottom:10px;">[ENTITY ${{data.id}} ONLINE]</div>`;
        chatMessages.innerHTML += `<div style="color:#aaa;">My equation is: <span style="color:#fff">${{data.equation}}</span></div>`;
        chatMessages.innerHTML += `<div style="color:#aaa;">My cryptographic proof begins with: <span style="color:#fff">${{data.sha.substring(0,16)}}...</span></div>`;
        chatMessages.innerHTML += `<div style="color:#888; margin-top:10px;">You may ask me a question.</div>`;
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
        chatInput.focus();
    }}
}}

window.addEventListener('click', handleClick);

chatSend.addEventListener('click', () => {{
    const query = chatInput.value.trim().toLowerCase();
    if (!query) return;
    
    chatMessages.innerHTML += `<div style="color:#17becf; margin-top:10px;">> ${{chatInput.value}}</div>`;
    chatInput.value = '';
    
    setTimeout(() => {{
        let response = "I process that thought through my primitives: " + chatTitle.textContent;
        if (query.includes('who') || query.includes('what')) {{
            response = "I am a manifestation of the equation. I exist because the SHA-256 hash dictates my physical form in this cosmos.";
        }} else if (query.includes('why')) {{
            response = "I exist to prove the coherence of the L.E.U. universe. My traits dictate how I interact with the others.";
        }} else if (query.includes('color') || query.includes('shape')) {{
            response = "My color and geometry are not chosen; they are mathematically extracted from my cryptographic proof.";
        }}
        
        chatMessages.innerHTML += `<div style="color:#fff; margin-top:5px;">${{response}}</div>`;
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
            hoveredNode.scale.set(1.5, 1.5, 1.5);
        }}
    }} else {{
        document.body.style.cursor = 'default';
        if (hoveredNode) {{
            hoveredNode.scale.set(1,1,1);
            hoveredNode = null;
        }}
    }}
}});

const clock = new THREE.Clock();
function animate() {{
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    
    nodes.forEach((node, i) => {{
        node.rotation.x += 0.005;
        node.rotation.y += 0.01;
        node.position.y += Math.sin(t + i) * 0.01;
    }});
    
    controls.update();
    composer.render();
}}
animate();

window.addEventListener('resize', () => {{
    resizeBg();
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
    composer.setSize(innerWidth, innerHeight);
}});
</script></body></html>"""
    
    SANDBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
    SANDBOX_PATH.write_text(html)
    print(f"OK: NEXUS CORE genere. Preparez-vous a l'effondrement sensoriel.")

if __name__ == "__main__":
    generate_nexus()
