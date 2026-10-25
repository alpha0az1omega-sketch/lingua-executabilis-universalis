import json
from pathlib import Path

SANDBOX_PATH = Path("../04_ARTIFACTS/living/NEXUS_FORMULAE.html")

def generate_nexus_formulae():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>L.E.U. - Nexus Formulae</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { overflow: hidden; background: #020205; font-family: 'Space Mono', monospace; color: #e0e0e0; }
#c { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }

/* HUD */
.hud { position: absolute; z-index: 10; pointer-events: none; }
#top-left { top: 30px; left: 30px; }
#top-right { top: 30px; right: 30px; text-align: right; }
#bottom-left { bottom: 30px; left: 30px; }

.title { font-family: 'Cinzel', serif; color: #d4af37; font-size: 24px; letter-spacing: 5px; text-transform: uppercase; text-shadow: 0 0 20px rgba(212,175,55,0.5); }
.sub { color: #888; font-size: 10px; letter-spacing: 2px; margin-bottom: 20px; }
.data-row { font-size: 11px; margin-bottom: 5px; color: #a0a0a0; }
.data-val { color: #fff; font-weight: bold; }
.data-gold { color: #d4af37; }
.data-cyan { color: #17becf; }

/* Core Execution Interface */
#execution-ui { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 700px; background: rgba(5, 5, 10, 0.95); border: 1px solid #d4af37; padding: 40px; display: none; z-index: 100; box-shadow: 0 0 100px rgba(212,175,55,0.15); backdrop-filter: blur(20px); }
#execution-ui::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 1px solid rgba(23, 190, 207, 0.3); pointer-events: none; }
#ui-close { position: absolute; top: 20px; right: 25px; color: #d4af37; cursor: pointer; font-size: 24px; }
#ui-close:hover { color: #fff; }
.ui-title { font-family: 'Cinzel', serif; font-size: 32px; color: #d4af37; margin-bottom: 10px; text-align: center; text-shadow: 0 0 20px rgba(212,175,55,0.5); }
.ui-author { text-align: center; color: #17becf; font-size: 14px; margin-bottom: 30px; font-style: italic; }

.execution-terminal { background: rgba(0,0,0,0.6); border: 1px solid #333; padding: 20px; font-size: 13px; line-height: 1.8; color: #ccc; min-height: 200px; font-family: 'Space Mono', monospace; }
.term-line { margin-bottom: 8px; }
.term-line.cmd { color: #17becf; }
.term-line.out { color: #d4af37; }
.term-line.sys { color: #666; }

.ui-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 25px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; }
.crypto-proof { font-size: 10px; color: #666; word-break: break-all; max-width: 400px; }
.btn-infinity { background: transparent; border: 1px solid #d4af37; color: #d4af37; padding: 10px 20px; font-family: 'Cinzel', serif; font-weight: bold; cursor: pointer; transition: all 0.3s; letter-spacing: 2px; }
.btn-infinity:hover { background: #d4af37; color: #000; }

/* Cursor override for hover */
body.hovering-formula { cursor: pointer; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="c"></div>

<div class="hud" id="top-left">
    <div class="title">Nexus Formulae</div>
    <div class="sub">LIVING MATHEMATICAL ENTITIES</div>
    <div class="data-row">ACTIVE FORMULAS: <span class="data-val" id="formula-count">0</span></div>
    <div class="data-row">STATE: <span class="data-gold">EXECUTING</span></div>
</div>

<div class="hud" id="top-right">
    <div class="sub">SYSTEM PROOF</div>
    <div class="data-row">GPG: <span class="data-val">4ED4A15B...</span></div>
    <div class="data-row">DOI: <span class="data-gold">10.5281/zenodo.23476518</span></div>
</div>

<div class="hud" id="bottom-left">
    <div class="sub">INTERACTION</div>
    <div class="data-row">DRAG: Rotate Universe</div>
    <div class="data-row">CLICK FORMULA: Enter Execution Heart</div>
</div>

<div id="execution-ui">
    <div id="ui-close">✕</div>
    <div class="ui-title" id="ui-title">E = mc²</div>
    <div class="ui-author" id="ui-author">Albert Einstein · 1905</div>
    
    <div class="execution-terminal" id="ui-terminal">
        <!-- Terminal lines injected here -->
    </div>

    <div class="ui-footer">
        <div class="crypto-proof" id="ui-hash">SHA-256: calculating...</div>
        <button class="btn-infinity" onclick="executeInfinity()">EXECUTE AT INFINITY</button>
    </div>
</div>

<script>
window.onerror = function(msg) { console.error(msg); };

// ===== THREE.JS SETUP =====
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x020205, 0.003);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 70);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.getElementById('c').appendChild(renderer.domElement);

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 0.5));
const l1 = new THREE.PointLight(0xd4af37, 2, 300); l1.position.set(20, 30, 20); scene.add(l1);
const l2 = new THREE.PointLight(0x17becf, 2, 300); l2.position.set(-20, -30, -20); scene.add(l2);

// ===== 1. THE CORE (The Source of Math) =====
const coreGeo = new THREE.IcosahedronGeometry(6, 2);
const coreMat = new THREE.MeshStandardMaterial({
    color: 0xd4af37,
    emissive: 0xd4af37,
    emissiveIntensity: 0.8,
    wireframe: true,
    transparent: true,
    opacity: 0.3
});
const coreMesh = new THREE.Mesh(coreGeo, coreMat);
scene.add(coreMesh);

// ===== 2. THE FORMULA SWARM (Text Sprites) =====
// Function to generate a text texture for 3D sprites
function createTextTexture(text, colorHex) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 512;
    canvas.height = 128;
    
    // Glow effect
    ctx.shadowColor = colorHex;
    ctx.shadowBlur = 20;
    
    ctx.fillStyle = colorHex;
    ctx.font = "bold 50px 'Space Mono', monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(text, canvas.width/2, canvas.height/2);
    
    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter;
    return texture;
}

const theorems = [
    { eq: "E = mc²", author: "Einstein · 1905" },
    { eq: "a² + b² = c²", author: "Pythagore · -500" },
    { eq: "e^(iπ) + 1 = 0", author: "Euler · 1748" },
    { eq: "F = G(m₁m₂)/r²", author: "Newton · 1687" },
    { eq: "iħ(∂Ψ/∂t) = ĤΨ", author: "Schrödinger · 1926" },
    { eq: "ζ(s) = 1/1ˢ + 1/2ˢ + ...", author: "Riemann · 1859" },
    { eq: "∇ × E = -∂B/∂t", author: "Maxwell · 1865" },
    { eq: "S = k_B ln(W)", author: "Boltzmann · 1877" },
    { eq: "x = (-b ± √(b²-4ac)) / 2a", author: "Al-Khwarizmi · 820" },
    { eq: "F = ma", author: "Newton · 1687" },
    { eq: "UNIFIED FIELD THEORY", author: "L.E.U. · 2026 (FUTUR)" },
    { eq: "CONSCIOUSNESS = ∫ Ψ* Ψ dt", author: "L.E.U. · 2026 (FUTUR)" }
];

const formulaNodes = [];
const colors = [0xffd700, 0x17becf, 0xff8c00, 0x87ceeb];

theorems.forEach((th, index) => {
    const colorHex = '#' + new THREE.Color(colors[index % colors.length]).getHexString();
    const texture = createTextTexture(th.eq, colorHex);
    
    const material = new THREE.SpriteMaterial({ 
        map: texture, 
        transparent: true, 
        blending: THREE.AdditiveBlending,
        depthTest: false // Allows text to glow through things
    });
    
    const sprite = new THREE.Sprite(material);
    
    // Scale based on text length (approximate)
    const scale = 4 + (th.eq.length * 0.5);
    sprite.scale.set(scale, scale/4, 1);
    
    // Spherical positioning (Fibonacci)
    const phi = Math.acos(1 - 2 * (index + 0.5) / theorems.length);
    const theta = Math.PI * (1 + Math.sqrt(5)) * index;
    const radius = 25;
    
    sprite.position.set(
        Math.cos(theta) * Math.sin(phi) * radius,
        Math.sin(theta) * Math.sin(phi) * radius,
        Math.cos(phi) * radius
    );
    
    sprite.userData = {
        theorem: th,
        baseY: sprite.position.y,
        phase: Math.random() * Math.PI * 2,
        speed: 0.5 + Math.random() * 0.5
    };
    
    scene.add(sprite);
    formulaNodes.push(sprite);
});

document.getElementById('formula-count').textContent = formulaNodes.length;

// ===== 3. INTERACTION & CAMERA =====
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let targetRotation = { x: 0, y: 0 };
let currentRotation = { x: 0, y: 0 };
let activeSprite = null;

document.addEventListener('mousedown', (e) => { isDragging = true; prevMouse = { x: e.clientX, y: e.clientY }; });
document.addEventListener('mouseup', () => { isDragging = false; });
document.addEventListener('mousemove', (e) => {
    // Hover effect
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(formulaNodes);
    
    if (intersects.length > 0 && !isDragging) {
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
    camera.position.z = Math.max(20, Math.min(150, camera.position.z));
});

// ===== 4. CLICK TO EXECUTE =====
const ui = document.getElementById('execution-ui');
const uiTerminal = document.getElementById('ui-terminal');

document.addEventListener('click', (e) => {
    if (e.target.closest('#execution-ui')) return; // Ignore clicks inside UI
    
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    
    const intersects = raycaster.intersectObjects(formulaNodes);
    
    if (intersects.length > 0) {
        activeSprite = intersects[0].object;
        const th = activeSprite.userData.theorem;
        
        document.getElementById('ui-title').textContent = th.eq;
        document.getElementById('ui-author').textContent = th.author;
        
        // Generate Hash
        let hash = 0;
        for (let i = 0; i < th.eq.length; i++) hash = ((hash << 5) - hash) + th.eq.charCodeAt(i);
        const shaHex = Math.abs(hash).toString(16).padEnd(16, '0');
        document.getElementById('ui-hash').textContent = `SHA-256: ${shaHex}... | STATUS: VERIFIED`;
        
        // Animate Terminal Execution
        ui.style.display = 'block';
        uiTerminal.innerHTML = '';
        
        const lines = [
            { text: `> INITIATING EXECUTION OF: ${th.eq}`, type: 'cmd' },
            { text: `> SOURCE IDENTIFIED: ${th.author}`, type: 'sys' },
            { text: `> COMPILING ONTOLOGICAL PRIMITIVES...`, type: 'sys' },
            { text: `> EXIST(x) ... OK`, type: 'sys' },
            { text: `> CAUSE(x) ... OK`, type: 'sys' },
            { text: `> RESOLVING EQUATION...`, type: 'cmd' },
            { text: `  Result = COMPUTED_SUCCESS`, type: 'out' },
            { text: `> VERIFYING CRYPTOGRAPHIC PROOF...`, type: 'sys' },
            { text: `  HASH = ${shaHex}`, type: 'out' },
            { text: `> EXECUTION COMPLETE. INFINITE POTENTIAL UNLOCKED.`, type: 'cmd' }
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
});

// Infinity execution visual
window.executeInfinity = function() {
    if (!activeSprite) return;
    const th = activeSprite.userData.theorem;
    playSound(888);
    const term = document.getElementById('ui-terminal');
    const div = document.createElement('div');
    div.className = 'term-line out';
    div.innerHTML = `<br>♾️ ENGAGING INFINITE LOOP FOR: ${th.eq}<br>EXPANDING FRACTAL DIMENSIONS...<br>NO END IN SIGHT.`;
    term.appendChild(div);
    term.scrollTop = term.scrollHeight;
    
    // Visual explosion effect
    activeSprite.scale.multiplyScalar(1.5);
    setTimeout(() => activeSprite.scale.multiplyScalar(1/1.5), 300);
};

// ===== 5. AUDIO =====
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

// ===== 6. ANIMATION LOOP =====
const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    
    // Camera rotation smoothing
    if (!isDragging) {
        targetRotation.y += 0.001;
        targetRotation.x = Math.sin(t * 0.1) * 0.1;
    }
    currentRotation.x += (targetRotation.x - currentRotation.x) * 0.05;
    currentRotation.y += (targetRotation.y - currentRotation.y) * 0.05;
    
    scene.rotation.x = currentRotation.x;
    scene.rotation.y = currentRotation.y;
    
    // Core breathing
    coreMesh.rotation.x = t * 0.1;
    coreMesh.rotation.y = t * 0.2;
    const s = 1 + Math.sin(t * 2) * 0.05;
    coreMesh.scale.set(s, s, s);
    
    // Float sprites (formulas)
    formulaNodes.forEach((sprite, i) => {
        sprite.position.y = sprite.userData.baseY + Math.sin(t * sprite.userData.speed + sprite.userData.phase) * 3;
        
        // Make them face the camera
        sprite.lookAt(camera.position);
        
        // Subtle pulse if not active
        if (sprite !== activeSprite) {
            const pulse = 1 + Math.sin(t * 2 + i) * 0.02;
            sprite.scale.set(sprite.scale.x, sprite.scale.y, 1);
        }
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
    print(f"OK: NEXUS FORMULAE genere. Les formules sont vivantes.")

if __name__ == "__main__":
    generate_nexus_formulae()
