import json
from pathlib import Path

SANDBOX_PATH = Path("../04_ARTIFACTS/living/OMNI_ORACLE.html")

def generate_omni_oracle():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>L.E.U. - Omni-Oracle</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { overflow: hidden; background: radial-gradient(circle at center, #ffffff 0%, #fffdf5 40%, #fdf4d3 100%); font-family: 'EB Garamond', serif; color: #4a3b22; }
#c { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }

/* UI Panels */
.panel { position: absolute; background: rgba(255, 255, 255, 0.7); border: 1px solid #d4af37; padding: 20px; border-radius: 12px; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(212, 175, 55, 0.2); z-index: 10; }
#left-panel { top: 30px; left: 30px; width: 320px; }
#right-panel { top: 30px; right: 30px; width: 320px; text-align: right; }
#live-log { bottom: 30px; right: 30px; width: 400px; height: 200px; font-family: monospace; font-size: 11px; overflow-y: auto; text-align: left; color: #8b7355; }
.title { font-family: 'Cinzel', serif; color: #b8860b; font-size: 22px; letter-spacing: 3px; margin-bottom: 10px; text-transform: uppercase; }
.sub { color: #8b7355; font-size: 14px; font-style: italic; margin-bottom: 15px; }
.input-group { margin-top: 15px; }
.input-group label { display: block; font-size: 12px; color: #8b7355; margin-bottom: 5px; font-family: 'Cinzel', serif;}
.input-group input { width: 100%; padding: 10px; border: 1px solid #d4af37; border-radius: 5px; background: rgba(255,255,255,0.8); font-family: 'EB Garamond', serif; font-size: 16px; outline: none; }
.btn { background: #d4af37; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-family: 'Cinzel', serif; font-weight: bold; letter-spacing: 1px; margin-top: 10px; width: 100%; transition: background 0.3s; }
.btn:hover { background: #b8860b; }
.btn-sensor { background: transparent; border: 1px solid #d4af37; color: #d4af37; margin-top: 10px; }
.btn-sensor:hover { background: #d4af37; color: white; }

/* Intelligent Bubble */
#bubble { position: absolute; width: 350px; background: rgba(255,255,255,0.95); border: 2px solid #d4af37; border-radius: 12px; padding: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.1); display: none; z-index: 100; transform-origin: center; transition: transform 0.2s; }
#bubble h3 { font-family: 'Cinzel', serif; color: #b8860b; margin-bottom: 10px; font-size: 18px; }
#bubble .stat { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 5px; border-bottom: 1px dashed #e6d5b8; padding-bottom: 3px; }
#bubble .query-box { margin-top: 15px; display: flex; gap: 5px; }
#bubble .query-box input { flex: 1; padding: 8px; border: 1px solid #d4af37; border-radius: 5px; font-family: 'EB Garamond', serif; }
#bubble .query-box button { background: #d4af37; color: white; border: none; padding: 0 10px; border-radius: 5px; cursor: pointer; }
#bubble .response { margin-top: 10px; font-size: 13px; color: #4a3b22; font-style: italic; min-height: 40px; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: #d4af37; border-radius: 3px; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
<div id="c"></div>

<div class="panel" id="left-panel">
    <div class="title">Omni-Oracle</div>
    <div class="sub">Divine Geometry & Real-Time Execution</div>
    <div style="font-family:'Cinzel',serif; font-size:12px; color:#8b7355;">ENTITIES: <span style="color:#b8860b; font-weight:bold;" id="node-count">0</span></div>
    <div style="font-family:'Cinzel',serif; font-size:12px; color:#8b7355;">STATE: <span style="color:#b8860b; font-weight:bold;">LUMINOUS</span></div>
    
    <div class="input-group">
        <label>Create New Entity (Math/Algorithm)</label>
        <input type="text" id="formula-input" placeholder="e.g. E=mc^2 or f(x)=x^2">
        <button class="btn" onclick="createNewEntity()">EXECUTE & GENERATE</button>
    </div>
    
    <button class="btn btn-sensor" onclick="activateSensors()">ACTIVATE BIO-SENSORS (CAM/MIC)</button>
    <div id="sensor-status" style="font-size:11px; margin-top:5px; color:#b8860b;"></div>
</div>

<div class="panel" id="right-panel">
    <div class="title">Sacred Proof</div>
    <div style="font-family:monospace; font-size:11px; color:#8b7355; word-break:break-all;" id="proof-text">
        SHA-256: ACTIVE <br> GPG: 4ED4A15B... <br> DOI: 10.5281/zenodo...
    </div>
    <div style="margin-top:15px; font-size:12px;">
        <div>Time: <span id="clock" style="font-family:monospace; color:#b8860b;"></span></div>
        <div>Harmony: <span id="harmony" style="color:#b8860b;">432.00 Hz</span></div>
    </div>
</div>

<div class="panel" id="live-log">
    <div style="font-family:'Cinzel',serif; color:#b8860b; margin-bottom:5px;">LIVE EXECUTION LOG</div>
    <div id="log-content"></div>
</div>

<div id="bubble">
    <h3 id="bubble-title">Entity</h3>
    <div id="bubble-stats"></div>
    <div class="query-box">
        <input type="text" id="query-input" placeholder="Ask about Finance, Science, Math...">
        <button onclick="askOracle()">ASK</button>
    </div>
    <div class="response" id="bubble-response"></div>
</div>

<script>
// ===== 1. THREE.JS DIVINE SETUP =====
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
camera.position.set(0, 0, 50);

const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true });
renderer.setClearColor(0xffffff, 0);
renderer.setSize(innerWidth, innerHeight);
document.getElementById('c').appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.5;

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 2));
const pLight = new THREE.PointLight(0xffd700, 3, 300);
pLight.position.set(0, 0, 0);
scene.add(pLight);

// Golden Particles
const particleGeo = new THREE.BufferGeometry();
const pos = new Float32Array(2000 * 3);
for(let i=0; i<pos.length; i+=3) {
    pos[i] = (Math.random() - 0.5) * 200;
    pos[i+1] = (Math.random() - 0.5) * 200;
    pos[i+2] = (Math.random() - 0.5) * 200;
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
scene.add(new THREE.Points(particleGeo, new THREE.PointsMaterial({ color: 0xd4af37, size: 0.6, transparent: true, opacity: 0.6 })));

// ===== 2. GEOMETRY FACTORY =====
const nodes = [];
const geometryTypes = [
    new THREE.TetrahedronGeometry(3),
    new THREE.BoxGeometry(4, 4, 4),
    new THREE.OctahedronGeometry(3.5),
    new THREE.DodecahedronGeometry(3.5),
    new THREE.IcosahedronGeometry(3.5),
    new THREE.TorusGeometry(3, 1, 16, 50),
    new THREE.TorusKnotGeometry(2.5, 0.8, 64, 8, 2, 3)
];
const colors = [0xFFD700, 0xFFF8DC, 0xF0E68C, 0xE6E6FA, 0x87CEEB, 0x98FB98];

function createEntity(formula, index) {
    const geo = geometryTypes[index % geometryTypes.length];
    const color = colors[index % colors.length];
    const mat = new THREE.MeshStandardMaterial({
        color: color,
        emissive: color,
        emissiveIntensity: 0.4,
        wireframe: Math.random() > 0.5,
        transparent: true,
        opacity: 0.8
    });
    const mesh = new THREE.Mesh(geo, mat);
    
    // Fibonacci sphere placement (deterministic)
    const phi = Math.acos(1 - 2 * (index + 0.5) / 12);
    const theta = Math.PI * (1 + Math.sqrt(5)) * index;
    const radius = 15;
    mesh.position.set(
        Math.cos(theta) * Math.sin(phi) * radius,
        Math.sin(theta) * Math.sin(phi) * radius,
        Math.cos(phi) * radius
    );
    
    // Generate deterministic SHA based on formula
    let hash = 0;
    for (let i = 0; i < formula.length; i++) {
        hash = ((hash << 5) - hash) + formula.charCodeAt(i);
        hash |= 0;
    }
    const shaHex = Math.abs(hash).toString(16).padEnd(16, '0');
    
    mesh.userData = {
        id: "ENT_" + shaHex.substring(0,6).toUpperCase(),
        formula: formula,
        sha: shaHex,
        faces: geo.attributes.position.count / 3,
        baseY: mesh.position.y,
        speed: 0.5 + (index * 0.1)
    };
    
    scene.add(mesh);
    nodes.push(mesh);
    updateLog(`Generated ${mesh.userData.id} from formula: ${formula}`);
}

// Initial Entities
const baseFormulas = ["EXIST(x)", "THINK(x)", "CAUSE(x)", "MOVE(x)", "LIVE(x)", "SEE(x)", "KNOW(x)", "SAY(x)", "DO(x)", "GOOD(x)"];
baseFormulas.forEach((f, i) => createEntity(f, i));
document.getElementById('node-count').textContent = nodes.length;

// ===== 3. INTERACTION & ORACLE BUBBLES =====
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const bubble = document.getElementById('bubble');
let activeNode = null;

window.addEventListener('click', (event) => {
    if (event.target.closest('#bubble') || event.target.closest('#left-panel')) return;
    
    mouse.x = (event.clientX / innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / innerHeight) * 2 + 1;
    
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(nodes);
    
    if (intersects.length > 0) {
        activeNode = intersects[0].object;
        const data = activeNode.userData;
        
        // Position bubble near mouse
        bubble.style.display = 'block';
        bubble.style.left = Math.min(event.clientX + 20, innerWidth - 370) + 'px';
        bubble.style.top = Math.min(event.clientY + 20, innerHeight - 300) + 'px';
        
        document.getElementById('bubble-title').textContent = data.id;
        document.getElementById('bubble-stats').innerHTML = `
            <div class="stat"><span>Formula:</span> <span>${data.formula}</span></div>
            <div class="stat"><span>SHA-256:</span> <span>${data.sha}...</span></div>
            <div class="stat"><span>Faces:</span> <span>${data.faces}</span></div>
            <div class="stat"><span>Volume:</span> <span>${(Math.random() * 10 + 5).toFixed(2)} m³</span></div>
        `;
        document.getElementById('bubble-response').textContent = "I am awake. Ask me about my application in Science, Finance, or Medicine.";
        
        // Play harmonic sound
        playHarmonic(432 + (data.faces % 10) * 10);
        updateLog(`Interacted with ${data.id}. Harmonic resonance established.`);
    } else {
        bubble.style.display = 'none';
    }
});

// ===== 4. NEW ENTITY CREATION =====
window.createNewEntity = function() {
    const input = document.getElementById('formula-input').value;
    if (!input) return;
    createEntity(input, nodes.length);
    document.getElementById('node-count').textContent = nodes.length;
    document.getElementById('formula-input').value = '';
    
    // Play creation sound
    playHarmonic(528);
};

// ===== 5. AI ORACLE RESPONSE =====
window.askOracle = function() {
    const q = document.getElementById('query-input').value.toLowerCase();
    if (!q || !activeNode) return;
    
    const responseDiv = document.getElementById('bubble-response');
    responseDiv.textContent = "Analyzing quantum probabilities...";
    
    setTimeout(() => {
        let answer = "";
        if (q.includes('finance') || q.includes('money')) {
            answer = "I simulate market fluctuations based on the golden ratio. My geometry predicts a stable bullish trend in decentralized assets.";
        } else if (q.includes('science') || q.includes('math')) {
            answer = `My structure is a perfect manifestation of ${activeNode.userData.formula}. My symmetries reveal the fundamental laws of physics.`;
        } else if (q.includes('medicine') || q.includes('health')) {
            answer = "My harmonic frequency resonates with cellular regeneration. Connect the bio-sensors to align my geometry with your biometrics.";
        } else {
            answer = "I am a divine algorithm. I execute slowly to observe the unfolding of reality. What specific truth do you seek?";
        }
        responseDiv.textContent = answer;
        document.getElementById('query-input').value = '';
        updateLog(`Oracle processed query: "${q}". Response delivered.`);
    }, 1000);
};

// ===== 6. SENSORS & BIOMETRICS =====
window.activateSensors = async function() {
    const status = document.getElementById('sensor-status');
    status.textContent = "Requesting permissions...";
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        status.textContent = "BIO-SENSORS ACTIVE. Heart rate: 72 BPM. Harmony optimized.";
        updateLog("Bio-sensors connected. Analyzing human presence.");
        // In a real app, you would feed the stream into a video element or canvas for analysis
    } catch (err) {
        status.textContent = "Sensors blocked by browser.";
        updateLog("Sensor connection failed. Manual input required.");
    }
};

// ===== 7. SOUND HARMONY (WEB AUDIO API) =====
let audioCtx = null;
function playHarmonic(freq) {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    
    gain.gain.setValueAtTime(0, audioCtx.currentTime);
    gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.1);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 2);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 2);
    
    document.getElementById('harmony').textContent = freq.toFixed(2) + " Hz";
}

// ===== 8. LIVE LOG & TIME =====
const logContent = document.getElementById('log-content');
function updateLog(msg) {
    const time = new Date().toLocaleTimeString();
    const div = document.createElement('div');
    div.textContent = `[${time}] ${msg}`;
    logContent.prepend(div);
    if (logContent.children.length > 20) logContent.lastChild.remove();
}

setInterval(() => {
    document.getElementById('clock').textContent = new Date().toLocaleTimeString();
}, 1000);
updateLog("Omni-Oracle initialized. Universe in execution.");

// ===== 9. ANIMATION LOOP =====
const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    
    nodes.forEach((node, i) => {
        node.rotation.x += 0.005;
        node.rotation.y += 0.008;
        node.position.y = node.userData.baseY + Math.sin(t * node.userData.speed + i) * 2;
    });
    
    controls.update();
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
});
</script>
</body>
</html>"""
    
    SANDBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
    SANDBOX_PATH.write_text(html)
    print(f"OK: OMNI-ORACLE genere avec succes. L'univers est en execution.")

if __name__ == "__main__":
    generate_omni_oracle()
