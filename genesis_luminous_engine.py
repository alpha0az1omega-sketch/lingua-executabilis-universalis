import json
from pathlib import Path

SANDBOX_PATH = Path("../04_ARTIFACTS/living/GENESIS_LUMINOUS_V5.html")

def generate_v5():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>L.E.U. - Genesis Luminous V5</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { overflow: hidden; background: radial-gradient(circle at center, #ffffff 0%, #fffdf5 40%, #fdf4d3 100%); font-family: 'Space Mono', monospace; color: #4a3b22; }
#c { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }

/* HUD */
.hud { position: absolute; z-index: 10; pointer-events: none; }
#top-left { top: 30px; left: 30px; }
#top-right { top: 30px; right: 30px; text-align: right; }
#bottom-left { bottom: 30px; left: 30px; }

.title { font-family: 'Cinzel', serif; color: #b8860b; font-size: 26px; letter-spacing: 5px; text-transform: uppercase; text-shadow: 0 0 15px rgba(212,175,55,0.6); margin-bottom: 5px; }
.sub { color: #8b7355; font-size: 11px; letter-spacing: 2px; margin-bottom: 20px; }
.data-row { font-size: 12px; margin-bottom: 6px; color: #6b5b45; font-weight: bold; }
.data-val { color: #b8860b; }
.data-cyan { color: #17becf; }

/* Execution Terminal */
#execution-ui { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 750px; background: rgba(255, 255, 255, 0.95); border: 2px solid #d4af37; padding: 40px; display: none; z-index: 100; box-shadow: 0 20px 80px rgba(212,175,55,0.4); backdrop-filter: blur(15px); border-radius: 4px; }
#ui-close { position: absolute; top: 20px; right: 25px; color: #b8860b; cursor: pointer; font-size: 24px; transition: color 0.3s; }
#ui-close:hover { color: #000; }
.ui-title { font-family: 'Cinzel', serif; font-size: 36px; color: #b8860b; margin-bottom: 5px; text-align: center; text-shadow: 0 0 20px rgba(212,175,55,0.4); }
.ui-author { text-align: center; color: #17becf; font-size: 14px; margin-bottom: 30px; font-style: italic; letter-spacing: 1px; }

.execution-terminal { background: rgba(253, 244, 211, 0.5); border-left: 4px solid #d4af37; padding: 25px; font-size: 14px; line-height: 1.8; color: #4a3b22; min-height: 250px; font-family: 'Space Mono', monospace; border-radius: 0 4px 4px 0; }
.term-line { margin-bottom: 8px; opacity: 0; transform: translateY(5px); animation: fadeIn 0.3s forwards; }
@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
.term-line.cmd { color: #b8860b; font-weight: bold; }
.term-line.out { color: #17becf; font-weight: bold; }
.term-line.sys { color: #8b7355; }

.ui-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 25px; }
.crypto-proof { font-size: 11px; color: #8b7355; word-break: break-all; max-width: 400px; }
.btn-infinity { background: transparent; border: 2px solid #d4af37; color: #b8860b; padding: 12px 25px; font-family: 'Cinzel', serif; font-weight: bold; cursor: pointer; transition: all 0.3s; letter-spacing: 2px; border-radius: 3px; }
.btn-infinity:hover { background: #d4af37; color: #fff; box-shadow: 0 0 20px rgba(212,175,55,0.4); }

body.hovering-formula { cursor: pointer; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="c"></div>

<div class="hud" id="top-left">
    <div class="title">Genesis Luminous</div>
    <div class="sub">THE UNIFIED ARCHIVE OF L.E.U.</div>
    <div class="data-row">TIME: <span class="data-val" id="local-time">--:--</span></div>
    <div class="data-row">COSMIC STATE: <span class="data-val" id="state-text" style="color:#17becf;">AWAITING OBSERVER</span></div>
</div>

<div class="hud" id="top-right">
    <div class="sub">CRYPTOGRAPHIC PROOF</div>
    <div class="data-row">GPG: <span class="data-val">4ED4A15B...</span></div>
    <div class="data-row">DOI: <span class="data-val">10.5281/zenodo.23476518</span></div>
</div>

<div class="hud" id="bottom-left">
    <div class="sub">INTERACTION</div>
    <div class="data-row">DRAG: Rotate Universe</div>
    <div class="data-row">CLICK ENTITY: Execute Formula</div>
    <div class="data-row">MOVE MOUSE: Resonate</div>
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

// ===== 1. TIME & LIGHT =====
const now = new Date();
const h = now.getHours();
let lightColor = 0xffd700; // Default Gold
let uiColor = "#b8860b";

if (h >= 5 && h < 8) { lightColor = 0xffaa00; uiColor = "#d2691e"; } // Dawn
else if (h >= 8 && h < 17) { lightColor = 0xffffff; uiColor = "#17becf"; } // Day (White/Cyan)
else if (h >= 17 && h < 20) { lightColor = 0xff8c00; uiColor = "#ff8c00"; } // Dusk (Orange)

document.documentElement.style.setProperty('--theme-color', uiColor);
setInterval(() => {
    document.getElementById('local-time').textContent = new Date().toLocaleTimeString();
}, 1000);

// ===== 2. THREE.JS SETUP =====
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 70);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setClearColor(0xffffff, 0); // Transparent to show CSS background
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.getElementById('c').appendChild(renderer.domElement);

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 1.5)); // Very bright ambient
const pLight = new THREE.PointLight(lightColor, 3, 400); pLight.position.set(0, 0, 0); scene.add(pLight);
const pLight2 = new THREE.PointLight(0xffffff, 2, 400); pLight2.position.set(30, 30, 30); scene.add(pLight2);

// ===== 3. THE FUSION NEBULA (Light clouds) =====
function createGlowTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 128; canvas.height = 128;
    const ctx = canvas.getContext('2d');
    const grad = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.3, 'rgba(255,255,255,0.6)');
    grad.addColorStop(0.7, 'rgba(255,255,255,0.1)');
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(canvas);
}

const glowTex = createGlowTexture();
const nebulaGroup = new THREE.Group();
const nebulaColors = [0xffd700, 0x17becf, 0xffffff, 0xff8c00];
const nebulaSprites = [];

for (let i = 0; i < 80; i++) {
    const mat = new THREE.SpriteMaterial({
        map: glowTex,
        color: nebulaColors[i % nebulaColors.length],
        transparent: true,
        opacity: 0.15,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });
    const sprite = new THREE.Sprite(mat);
    
    const r = 20 + Math.random() * 60;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos((Math.random() * 2) - 1);
    sprite.position.set(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
    );
    
    const scale = 40 + Math.random() * 80;
    sprite.scale.set(scale, scale, 1);
    
    sprite.userData = { baseScale: scale, phase: Math.random() * Math.PI * 2, speed: 0.1 + Math.random() * 0.2 };
    nebulaGroup.add(sprite);
    nebulaSprites.push(sprite);
}
scene.add(nebulaGroup);

// ===== 4. THE CORE (Living Heart) =====
const coreGeo = new THREE.IcosahedronGeometry(8, 3); // High detail
const coreMat = new THREE.MeshStandardMaterial({
    color: 0xffffff,
    emissive: lightColor,
    emissiveIntensity: 1.0,
    metalness: 0.5,
    roughness: 0.1,
    wireframe: true,
    transparent: true,
    opacity: 0.8
});
const coreMesh = new THREE.Mesh(coreGeo, coreMat);
scene.add(coreMesh);

const innerGlow = new THREE.Mesh(
    new THREE.SphereGeometry(6, 32, 32),
    new THREE.MeshBasicMaterial({ color: lightColor, transparent: true, opacity: 0.3, blending: THREE.AdditiveBlending })
);
scene.add(innerGlow);

// ===== 5. THE ARCHIVE (Elements, Molecules, Formulas) =====
const entities = [
    // Primitives
    { label: "EXIST", type: "prim" }, { label: "THINK", type: "prim" }, { label: "CAUSE", type: "prim" }, { label: "LIVE", type: "prim" },
    // Elements
    { label: "H", type: "atom" }, { label: "Fe", type: "atom" }, { label: "Au", type: "atom" }, { label: "C", type: "atom" }, { label: "O", type: "atom" },
    // Molecules
    { label: "H₂O", type: "mol" }, { label: "CO₂", type: "mol" }, { label: "CH₄", type: "mol" },
    // Sacred Geometry / Math
    { label: "E = mc²", type: "math" }, { label: "a² + b² = c²", type: "math" }, { label: "e^(iπ) + 1 = 0", type: "math" },
    { label: "Φ", type: "math" }, { label: "π", type: "math" }, { label: "∞", type: "math" }
];

function createTextTexture(text, colorHex) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.font = "bold 60px 'Space Mono', monospace";
    const textWidth = ctx.measureText(text).width;
    canvas.width = Math.ceil(textWidth + 80);
    canvas.height = 120;
    
    ctx.shadowColor = colorHex;
    ctx.shadowBlur = 25;
    
    ctx.fillStyle = colorHex;
    ctx.font = "bold 60px 'Space Mono', monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(text, canvas.width/2, canvas.height/2);
    
    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter;
    return { texture, aspectRatio: canvas.width / canvas.height };
}

const entityNodes = [];
entities.forEach((ent, index) => {
    let colorHex = "#d4af37"; // Gold default
    if (ent.type === "atom") colorHex = "#17becf"; // Cyan
    if (ent.type === "mol") colorHex = "#ff8c00"; // Orange
    if (ent.type === "math") colorHex = "#8b7355"; // Bronze
    
    const { texture, aspectRatio } = createTextTexture(ent.label, colorHex);
    const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false });
    const sprite = new THREE.Sprite(material);
    
    const baseHeight = ent.type === "math" ? 3.5 : 4.5;
    sprite.scale.set(baseHeight * aspectRatio, baseHeight, 1);
    
    // Spherical distribution
    const phi = Math.acos(1 - 2 * (index + 0.5) / entities.length);
    const theta = Math.PI * (1 + Math.sqrt(5)) * index;
    const radius = 24;
    
    sprite.position.set(
        Math.cos(theta) * Math.sin(phi) * radius,
        Math.sin(theta) * Math.sin(phi) * radius,
        Math.cos(phi) * radius
    );
    
    sprite.userData = {
        entity: ent,
        baseY: sprite.position.y,
        phase: Math.random() * Math.PI * 2,
        speed: 0.4 + Math.random() * 0.4
    };
    
    scene.add(sprite);
    entityNodes.push(sprite);
});

// ===== 6. OBSERVER EFFECT & INTERACTION =====
const raycaster = new THREE.Raycaster();
const mouseVec = new THREE.Vector2();
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let targetRotation = { x: 0, y: 0 };
let currentRotation = { x: 0, y: 0 };
let activeSprite = null;
let lastMouseMove = Date.now();

document.addEventListener('mousemove', (e) => {
    targetMouseX = (e.clientX / window.innerWidth) * 2 - 1;
    targetMouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    lastMouseMove = Date.now();
    
    if (document.getElementById('state-text').textContent !== "RESONATING") {
        document.getElementById('state-text').textContent = "RESONATING";
    }

    mouseVec.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseVec.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouseVec, camera);
    const intersects = raycaster.intersectObjects(entityNodes);
    
    if (intersects.length > 0 && !isDragging && !activeSprite) {
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

document.addEventListener('mousedown', (e) => { isDragging = true; prevMouse = { x: e.clientX, y: e.clientY }; });
document.addEventListener('mouseup', () => { isDragging = false; });

document.addEventListener('wheel', (e) => {
    camera.position.z += e.deltaY * 0.05;
    camera.position.z = Math.max(20, Math.min(120, camera.position.z));
});

setInterval(() => {
    if (Date.now() - lastMouseMove > 5000 && !activeSprite) {
        document.getElementById('state-text').textContent = "UNIVERSE IS CONSCIOUS";
        document.getElementById('state-text').style.color = "#d4af37";
    }
}, 1000);

// ===== 7. CLICK TO EXECUTE =====
const ui = document.getElementById('execution-ui');
const uiTerminal = document.getElementById('ui-terminal');

document.addEventListener('click', (e) => {
    if (e.target.closest('#execution-ui')) return; 
    mouseVec.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouseVec.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouseVec, camera);
    const intersects = raycaster.intersectObjects(entityNodes);
    
    if (intersects.length > 0) {
        activeSprite = intersects[0].object;
        const ent = activeSprite.userData.entity;
        
        document.getElementById('ui-title').textContent = ent.label;
        document.getElementById('ui-author').textContent = ent.type.toUpperCase() + " ENTITY";
        document.getElementById('state-text').textContent = "OBSERVER EFFECT ACTIVE";
        
        let hash = 0;
        for (let i = 0; i < ent.label.length; i++) hash = ((hash << 5) - hash) + ent.label.charCodeAt(i);
        const shaHex = Math.abs(hash).toString(16).padEnd(16, '0');
        document.getElementById('ui-hash').textContent = `SHA-256: ${shaHex}... | STATUS: VERIFIED`;
        
        ui.style.display = 'block';
        uiTerminal.innerHTML = '';
        
        const lines = [
            { text: `> ACCESSING ARCHIVE ENTITY: ${ent.label}`, type: 'cmd' },
            { text: `> TYPE: ${ent.type.toUpperCase()}`, type: 'sys' },
            { text: `> LOADING ONTOLOGICAL PRIMITIVES...`, type: 'sys' },
            { text: `> SYNCHRONIZING WITH COSMIC CLOCK...`, type: 'cmd' },
            { text: `  [LIGHT FREQUENCY MATCHED]`, type: 'out' },
            { text: `> CRYPTOGRAPHIC PROOF: ${shaHex}`, type: 'sys' },
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
    activeSprite = null;
    document.getElementById('state-text').textContent = "AWAITING OBSERVER";
});

window.executeInfinity = function() {
    if (!activeSprite) return;
    playSound(888);
    const term = document.getElementById('ui-terminal');
    const div = document.createElement('div');
    div.className = 'term-line out';
    div.innerHTML = `<br>♾️ ENGAGING INFINITE LOOP<br>EXPANDING FRACTAL DIMENSIONS...<br>MATHEMATICAL SINGULARITY REACHED.`;
    term.appendChild(div);
    term.scrollTop = term.scrollHeight;
    activeSprite.scale.multiplyScalar(1.5);
    setTimeout(() => activeSprite.scale.multiplyScalar(1/1.5), 300);
};

// ===== 8. AUDIO =====
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

// ===== 9. ANIMATION =====
const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    
    if (!isDragging && !activeSprite) {
        targetRotation.y += 0.001;
        targetRotation.x = Math.sin(t * 0.1) * 0.1;
    }
    currentRotation.x += (targetRotation.x - currentRotation.x) * 0.05;
    currentRotation.y += (targetRotation.y - currentRotation.y) * 0.05;
    
    scene.rotation.x = currentRotation.x;
    scene.rotation.y = currentRotation.y;
    
    // Core breathing
    coreMesh.rotation.x = t * 0.1;
    coreMesh.rotation.y = t * 0.15;
    const pulse = 1 + Math.sin(t * 2) * 0.03;
    coreMesh.scale.set(pulse, pulse, pulse);
    
    // Nebula fusion animation
    nebulaGroup.rotation.y = t * 0.01;
    nebulaGroup.rotation.x = t * 0.005;
    nebulaSprites.forEach((sprite, i) => {
        const p = 1 + Math.sin(t * sprite.userData.speed + sprite.userData.phase) * 0.15;
        sprite.scale.set(sprite.userData.baseScale * p, sprite.userData.baseScale * p, 1);
        sprite.material.opacity = 0.1 + Math.sin(t * 0.5 + i) * 0.05;
    });
    
    // Entities floating
    entityNodes.forEach((sprite, i) => {
        sprite.position.y = sprite.userData.baseY + Math.sin(t * sprite.userData.speed + sprite.userData.phase) * 3;
        sprite.lookAt(camera.position);
    });
    
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
    print(f"OK: GENESIS LUMINOUS V5 genere. La lumiere divine est la.")

if __name__ == "__main__":
    generate_v5()
