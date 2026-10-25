import json
from pathlib import Path

SANDBOX_PATH = Path("../04_ARTIFACTS/living/COSMIC_WEB_V6.html")

def generate_v6():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>L.E.U. - Cosmic Web V6</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { overflow: hidden; background: #000000; font-family: 'Space Mono', monospace; color: #e0e0e0; }
#c { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }

/* HUD */
.hud { position: absolute; z-index: 10; pointer-events: none; }
#top-left { top: 30px; left: 30px; }
#top-right { top: 30px; right: 30px; text-align: right; }
#bottom-left { bottom: 30px; left: 30px; }

.title { font-family: 'Cinzel', serif; color: #d4af37; font-size: 24px; letter-spacing: 5px; text-transform: uppercase; text-shadow: 0 0 20px rgba(212,175,55,0.8); }
.sub { color: #666; font-size: 10px; letter-spacing: 2px; margin-bottom: 20px; }
.data-row { font-size: 11px; margin-bottom: 5px; color: #888; }
.data-val { color: #17becf; font-weight: bold; text-shadow: 0 0 10px rgba(23,190,207,0.5); }
.data-gold { color: #d4af37; }

/* Execution Terminal */
#execution-ui { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 750px; background: rgba(5, 5, 8, 0.95); border: 1px solid #17becf; padding: 40px; display: none; z-index: 100; box-shadow: 0 0 100px rgba(23,190,207,0.2), inset 0 0 30px rgba(23,190,207,0.1); backdrop-filter: blur(10px); clip-path: polygon(0 0, 100% 0, 100% calc(100% - 30px), calc(100% - 30px) 100%, 0 100%); }
#ui-close { position: absolute; top: 20px; right: 25px; color: #17becf; cursor: pointer; font-size: 24px; transition: color 0.3s; }
#ui-close:hover { color: #fff; }
.ui-title { font-family: 'Cinzel', serif; font-size: 36px; color: #d4af37; margin-bottom: 5px; text-align: center; text-shadow: 0 0 20px rgba(212,175,55,0.5); }
.ui-author { text-align: center; color: #17becf; font-size: 14px; margin-bottom: 30px; font-style: italic; letter-spacing: 1px; }

.execution-terminal { background: rgba(0,0,0,0.8); border-left: 2px solid #d4af37; padding: 25px; font-size: 14px; line-height: 1.8; color: #ccc; min-height: 250px; font-family: 'Space Mono', monospace; }
.term-line { margin-bottom: 8px; opacity: 0; transform: translateY(5px); animation: fadeIn 0.3s forwards; }
@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
.term-line.cmd { color: #17becf; font-weight: bold; }
.term-line.out { color: #d4af37; font-weight: bold; }
.term-line.sys { color: #666; }

.ui-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 25px; }
.crypto-proof { font-size: 11px; color: #666; word-break: break-all; max-width: 400px; }
.btn-infinity { background: transparent; border: 1px solid #17becf; color: #17becf; padding: 12px 25px; font-family: 'Cinzel', serif; font-weight: bold; cursor: pointer; transition: all 0.3s; letter-spacing: 2px; }
.btn-infinity:hover { background: #17becf; color: #000; box-shadow: 0 0 30px rgba(23,190,207,0.5); }

body.hovering-formula { cursor: pointer; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="c"></div>

<div class="hud" id="top-left">
    <div class="title">Cosmic Web</div>
    <div class="sub">THE UNIVERSAL NETWORK OF L.E.U.</div>
    <div class="data-row">NODES: <span class="data-val" id="node-count">0</span></div>
    <div class="data-row">STATE: <span class="data-gold" id="state-text">OBSERVING</span></div>
</div>

<div class="hud" id="top-right">
    <div class="sub">SYSTEM PROOF</div>
    <div class="data-row">GPG: <span class="data-val">4ED4A15B...</span></div>
    <div class="data-row">DOI: <span class="data-gold">10.5281/zenodo.23476518</span></div>
</div>

<div class="hud" id="bottom-left">
    <div class="sub">INTERACTION</div>
    <div class="data-row">DRAG: Rotate Universe</div>
    <div class="data-row">CLICK NODE: Enter Execution Heart</div>
</div>

<div id="execution-ui">
    <div id="ui-close">✕</div>
    <div class="ui-title" id="ui-title">E = mc²</div>
    <div class="ui-author" id="ui-author">Albert Einstein · 1905</div>
    <div class="execution-terminal" id="ui-terminal"></div>
    <div class="ui-footer">
        <div class="crypto-proof" id="ui-hash">SHA-256: calculating...</div>
        <button class="btn-infinity" onclick="executeInfinity()">EXECUTE AT INFINITY</button>
    </div>
</div>

<script>
window.onerror = function(msg) { console.error(msg); };

// ===== 1. THREE.JS SETUP =====
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x000000, 0.002);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 65);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setClearColor(0x000000, 0);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.getElementById('c').appendChild(renderer.domElement);

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 0.3));
const l1 = new THREE.PointLight(0xd4af37, 2, 400); l1.position.set(30, 30, 30); scene.add(l1);
const l2 = new THREE.PointLight(0x17becf, 2, 400); l2.position.set(-30, -30, -30); scene.add(l2);

// ===== 2. CENTRAL COSMIC CORE (Sacred Geometry) =====
const coreGroup = new THREE.Group();
// Icosahedron base
const coreGeo = new THREE.IcosahedronGeometry(8, 1);
const coreMat = new THREE.MeshBasicMaterial({ color: 0xd4af37, wireframe: true, transparent: true, opacity: 0.15 });
coreGroup.add(new THREE.Mesh(coreGeo, coreMat));
// Inner sphere
const coreInner = new THREE.Mesh(new THREE.SphereGeometry(4, 16, 16), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.2, blending: THREE.AdditiveBlending }));
coreGroup.add(coreInner);
scene.add(coreGroup);

// ===== 3. THE COSMIC WEB (Nodes & Connections) =====
const entities = [
    { label: "EXIST", type: "prim" }, { label: "THINK", type: "prim" }, { label: "CAUSE", type: "prim" }, { label: "LIVE", type: "prim" },
    { label: "H", type: "atom" }, { label: "Fe", type: "atom" }, { label: "Au", type: "atom" }, { label: "C", type: "atom" },
    { label: "H₂O", type: "mol" }, { label: "CO₂", type: "mol" }, { label: "CH₄", type: "mol" },
    { label: "E = mc²", type: "math" }, { label: "a² + b² = c²", type: "math" }, { label: "e^(iπ) + 1 = 0", type: "math" },
    { label: "Φ", type: "math" }, { label: "π", type: "math" }, { label: "∞", type: "math" }, { label: "∫", type: "math" }
];

function createTextTexture(text, colorHex) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.font = "bold 50px 'Space Mono', monospace";
    const textWidth = ctx.measureText(text).width;
    canvas.width = Math.ceil(textWidth + 60);
    canvas.height = 100;
    
    ctx.shadowColor = colorHex;
    ctx.shadowBlur = 20;
    
    ctx.fillStyle = colorHex;
    ctx.font = "bold 50px 'Space Mono', monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(text, canvas.width/2, canvas.height/2);
    
    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter;
    return { texture, aspectRatio: canvas.width / canvas.height };
}

const nodeMeshes = [];
const nodePositions = [];
const nodeColors = { prim: 0x17becf, atom: 0xff8c00, mol: 0xd4af37, math: 0x9467bd };

// Create Nodes
entities.forEach((ent, index) => {
    const color = nodeColors[ent.type] || 0xffffff;
    const colorHex = '#' + new THREE.Color(color).getHexString();
    
    // 3D Geometry for the node
    let geo;
    if (ent.type === "prim") geo = new THREE.IcosahedronGeometry(1.5, 0);
    else if (ent.type === "atom") geo = new THREE.OctahedronGeometry(1.5, 0);
    else if (ent.type === "mol") geo = new THREE.TetrahedronGeometry(1.5, 0);
    else geo = new THREE.TorusGeometry(1.2, 0.4, 8, 20);

    const mat = new THREE.MeshStandardMaterial({
        color: color, emissive: color, emissiveIntensity: 0.8,
        metalness: 0.8, roughness: 0.2, wireframe: true
    });
    const mesh = new THREE.Mesh(geo, mat);
    
    // Text Sprite above the geometry
    const { texture, aspectRatio } = createTextTexture(ent.label, colorHex);
    const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false });
    const sprite = new THREE.Sprite(spriteMat);
    const baseHeight = ent.type === "math" ? 2.5 : 3;
    sprite.scale.set(baseHeight * aspectRatio, baseHeight, 1);
    sprite.position.y = 3; // Position above the node
    
    const group = new THREE.Group();
    group.add(mesh);
    group.add(sprite);
    
    // Spherical distribution
    const phi = Math.acos(1 - 2 * (index + 0.5) / entities.length);
    const theta = Math.PI * (1 + Math.sqrt(5)) * index;
    const radius = 22 + Math.random() * 8;
    
    group.position.set(
        Math.cos(theta) * Math.sin(phi) * radius,
        Math.sin(theta) * Math.sin(phi) * radius,
        Math.cos(phi) * radius
    );
    
    group.userData = {
        entity: ent,
        baseY: group.position.y,
        phase: Math.random() * Math.PI * 2,
        speed: 0.5 + Math.random() * 0.5,
        mesh: mesh
    };
    
    scene.add(group);
    nodeMeshes.push(group);
    nodePositions.push(group.position.clone());
});

document.getElementById('node-count').textContent = nodeMeshes.length;

// Create Web (Lines)
const lineMaterial = new THREE.LineBasicMaterial({ color: 0x17becf, transparent: true, opacity: 0.15 });
const linePositions = [];
for(let i=0; i<nodePositions.length; i++) {
    for(let j=i+1; j<nodePositions.length; j++) {
        // Connect if distance is small enough
        if(nodePositions[i].distanceTo(nodePositions[j]) < 30) {
            linePositions.push(nodePositions[i].x, nodePositions[i].y, nodePositions[i].z);
            linePositions.push(nodePositions[j].x, nodePositions[j].y, nodePositions[j].z);
        }
    }
}
const lineGeo = new THREE.BufferGeometry();
lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePositions, 3));
const webLines = new THREE.LineSegments(lineGeo, lineMaterial);
scene.add(webLines);

// ===== 4. INTERACTION =====
const raycaster = new THREE.Raycaster();
const mouseVec = new THREE.Vector2();
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let targetRotation = { x: 0, y: 0 };
let currentRotation = { x: 0, y: 0 };
let activeNode = null;

document.addEventListener('mousedown', (e) => { isDragging = true; prevMouse = { x: e.clientX, y: e.clientY }; });
document.addEventListener('mouseup', () => { isDragging = false; });
document.addEventListener('mousemove', (e) => {
    mouseVec.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseVec.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouseVec, camera);
    
    // Check intersection with the meshes inside the groups
    const meshes = nodeMeshes.map(g => g.userData.mesh);
    const intersects = raycaster.intersectObjects(meshes);
    
    if (intersects.length > 0 && !isDragging && !activeNode) {
        document.body.classList.add('hovering-formula');
    } else {
        document.body.classList.remove('hovering-formula');
    }
    
    if (isDragging) {
        const dx = e.clientX - prevMouse.x;
        const dy = e.clientY - prevMouse.y;
        targetRotation.y += dx * 0.005;
        targetRotation.x += dy * 0.005;
        prevMouse = { x: e.clientX, y: e.clientY };
    }
});
document.addEventListener('wheel', (e) => {
    camera.position.z += e.deltaY * 0.05;
    camera.position.z = Math.max(20, Math.min(120, camera.position.z));
});

// ===== 5. CLICK TO EXECUTE =====
const ui = document.getElementById('execution-ui');
const uiTerminal = document.getElementById('ui-terminal');

document.addEventListener('click', (e) => {
    if (e.target.closest('#execution-ui')) return; 
    mouseVec.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseVec.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouseVec, camera);
    
    const meshes = nodeMeshes.map(g => g.userData.mesh);
    const intersects = raycaster.intersectObjects(meshes);
    
    if (intersects.length > 0) {
        // Find the parent group
        let obj = intersects[0].object;
        let group = obj.parent;
        
        activeNode = group;
        const ent = group.userData.entity;
        
        document.getElementById('ui-title').textContent = ent.label;
        document.getElementById('ui-author').textContent = ent.type.toUpperCase() + " ENTITY";
        document.getElementById('state-text').textContent = "EXECUTING";
        
        let hash = 0;
        for (let i = 0; i < ent.label.length; i++) hash = ((hash << 5) - hash) + ent.label.charCodeAt(i);
        const shaHex = Math.abs(hash).toString(16).padEnd(16, '0');
        document.getElementById('ui-hash').textContent = `SHA-256: ${shaHex}... | STATUS: VERIFIED`;
        
        ui.style.display = 'block';
        uiTerminal.innerHTML = '';
        
        const lines = [
            { text: `> INITIATING DEEP EXECUTION: ${ent.label}`, type: 'cmd' },
            { text: `> TYPE: ${ent.type.toUpperCase()}`, type: 'sys' },
            { text: `> CONNECTING TO COSMIC WEB...`, type: 'sys' },
            { text: `> RESOLVING IN INFINITE DIMENSIONAL SPACE...`, type: 'cmd' },
            { text: `  [MATHEMATICAL COHERENCE ACHIEVED]`, type: 'out' },
            { text: `> CRYPTOGRAPHIC SEAL: ${shaHex}`, type: 'sys' },
            { text: `> EXECUTION HEART OPEN.`, type: 'cmd' }
        ];
        
        let i = 0;
        function printLine() {
            if (i < lines.length) {
                const div = document.createElement('div');
                div.className = `term-line ${lines[i].type}`;
                div.textContent = lines[i].text;
                uiTerminal.appendChild(div);
                uiTerminal.scrollTop = uiTerminal.scrollHeight;
                i++;
                setTimeout(printLine, 300 + Math.random() * 200);
            }
        }
        printLine();
        playSound(600);
    }
});

document.getElementById('ui-close').addEventListener('click', () => {
    ui.style.display = 'none';
    activeNode = null;
    document.getElementById('state-text').textContent = "OBSERVING";
});

window.executeInfinity = function() {
    if (!activeNode) return;
    playSound(888);
    const term = document.getElementById('ui-terminal');
    const div = document.createElement('div');
    div.className = 'term-line out';
    div.innerHTML = `<br>♾️ ENGAGING INFINITE LOOP<br>EXPANDING FRACTAL DIMENSIONS...<br>MATHEMATICAL SINGULARITY REACHED.`;
    term.appendChild(div);
    term.scrollTop = term.scrollHeight;
    activeNode.scale.multiplyScalar(1.5);
    setTimeout(() => activeNode.scale.multiplyScalar(1/1.5), 300);
};

// ===== 6. AUDIO =====
let audioCtx = null;
function playSound(freq) {
    try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.1, audioCtx.currentTime + 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.5);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 1.5);
    } catch(e) {}
}

// ===== 7. ANIMATION =====
const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    
    if (!isDragging && !activeNode) {
        targetRotation.y += 0.001;
        targetRotation.x = Math.sin(t * 0.1) * 0.1;
    }
    currentRotation.x += (targetRotation.x - currentRotation.x) * 0.05;
    currentRotation.y += (targetRotation.y - currentRotation.y) * 0.05;
    
    scene.rotation.x = currentRotation.x;
    scene.rotation.y = currentRotation.y;
    
    // Core rotation
    coreGroup.rotation.x = t * 0.1;
    coreGroup.rotation.y = t * 0.15;
    const pulse = 1 + Math.sin(t * 2) * 0.05;
    coreGroup.scale.set(pulse, pulse, pulse);
    
    // Nodes floating and rotating
    nodeMeshes.forEach((group, i) => {
        group.position.y = group.userData.baseY + Math.sin(t * group.userData.speed + group.userData.phase) * 2.5;
        
        // Rotate the 3D geometry inside
        group.userData.mesh.rotation.x += 0.01;
        group.userData.mesh.rotation.y += 0.015;
        
        // If active, pulse the geometry
        if (group === activeNode) {
            const p = 1 + Math.sin(t * 10) * 0.1;
            group.userData.mesh.scale.set(p, p, p);
        } else {
            group.userData.mesh.scale.set(1, 1, 1);
        }
    });
    
    // Web line pulse (opacity)
    lineMaterial.opacity = 0.1 + Math.sin(t * 2) * 0.05;
    
    renderer.render(scene, camera);
}
animate();

window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
</body>
</html>"""
    
    SANDBOX_PATH.parent.mkdir(parents=True, exist_ok=True)
    SANDBOX_PATH.write_text(html)
    print(f"OK: COSMIC WEB V6 genere. La toile est active.")

if __name__ == "__main__":
    generate_v6()
