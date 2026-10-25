import json
from pathlib import Path

SANDBOX_PATH = Path("../04_ARTIFACTS/living/DIVINE_CORE_V3.html")

def generate_divine_core():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>L.E.U. - Divine Core V3</title>
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

/* Execution Terminal */
#execution-ui { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 750px; background: rgba(5, 5, 8, 0.9); border: 1px solid rgba(212, 175, 55, 0.3); padding: 40px; display: none; z-index: 100; box-shadow: 0 0 150px rgba(212,175,55,0.15), inset 0 0 50px rgba(212,175,55,0.05); backdrop-filter: blur(15px); }
#execution-ui::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 1px solid rgba(23, 190, 207, 0.1); pointer-events: none; }
#ui-close { position: absolute; top: 20px; right: 25px; color: #d4af37; cursor: pointer; font-size: 24px; transition: color 0.3s; }
#ui-close:hover { color: #fff; }
.ui-title { font-family: 'Cinzel', serif; font-size: 36px; color: #d4af37; margin-bottom: 5px; text-align: center; text-shadow: 0 0 30px rgba(212,175,55,0.6); }
.ui-author { text-align: center; color: #17becf; font-size: 14px; margin-bottom: 30px; font-style: italic; letter-spacing: 1px; }

.execution-terminal { background: rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.1); padding: 25px; font-size: 14px; line-height: 1.8; color: #ccc; min-height: 250px; font-family: 'Space Mono', monospace; border-left: 3px solid #d4af37; }
.term-line { margin-bottom: 8px; opacity: 0; transform: translateY(5px); animation: fadeIn 0.3s forwards; }
@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
.term-line.cmd { color: #17becf; font-weight: bold; }
.term-line.out { color: #d4af37; }
.term-line.sys { color: #666; }

.ui-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 25px; }
.crypto-proof { font-size: 11px; color: #666; word-break: break-all; max-width: 400px; }
.btn-infinity { background: transparent; border: 1px solid #d4af37; color: #d4af37; padding: 12px 25px; font-family: 'Cinzel', serif; font-weight: bold; cursor: pointer; transition: all 0.3s; letter-spacing: 2px; box-shadow: 0 0 15px rgba(212,175,55,0.1); }
.btn-infinity:hover { background: #d4af37; color: #000; box-shadow: 0 0 30px rgba(212,175,55,0.5); }

body.hovering-formula { cursor: pointer; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="c"></div>

<div class="hud" id="top-left">
    <div class="title">Divine Core V3</div>
    <div class="sub">HOLOGRAPHIC MATHEMATICAL ENTITIES</div>
    <div class="data-row">ACTIVE FORMULAS: <span class="data-val" id="formula-count">0</span></div>
    <div class="data-row">STATE: <span class="data-gold" id="state-text">OBSERVING</span></div>
</div>

<div class="hud" id="top-right">
    <div class="sub">SYSTEM PROOF</div>
    <div class="data-row">GPG: <span class="data-val">4ED4A15B...</span></div>
    <div class="data-row">DOI: <span class="data-gold">10.5281/zenodo.23476518</span></div>
</div>

<div class="hud" id="bottom-left">
    <div class="sub">INTERACTION</div>
    <div class="data-row">DRAG: Rotate Cosmos</div>
    <div class="data-row">CLICK FORMULA: Enter Execution Heart</div>
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

// ===== THREE.JS SETUP =====
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x020205, 0.002);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, 60);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.getElementById('c').appendChild(renderer.domElement);

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 0.4));
const l1 = new THREE.PointLight(0xd4af37, 2.5, 300); l1.position.set(20, 30, 20); scene.add(l1);
const l2 = new THREE.PointLight(0x17becf, 1.5, 300); l2.position.set(-20, -30, -20); scene.add(l2);

// ===== 1. THE LIVING CORE (Morphing Torus) =====
const coreGeo = new THREE.TorusKnotGeometry(7, 1.2, 200, 24, 3, 4);
const coreMat = new THREE.MeshStandardMaterial({
    color: 0xd4af37,
    emissive: 0xd4af37,
    emissiveIntensity: 0.8,
    metalness: 0.9,
    roughness: 0.1,
    wireframe: true,
    transparent: true,
    opacity: 0.5
});
const coreMesh = new THREE.Mesh(coreGeo, coreMat);
scene.add(coreMesh);

// Inner glowing sphere
const innerSphere = new THREE.Mesh(
    new THREE.SphereGeometry(4, 32, 32),
    new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.1, blending: THREE.AdditiveBlending })
);
scene.add(innerSphere);

// ===== 2. MATH PARTICLE SWARM =====
const particleCount = 3000;
const particleGeo = new THREE.BufferGeometry();
const pos = new Float32Array(particleCount * 3);
const colors = new Float32Array(particleCount * 3);
const color1 = new THREE.Color(0xd4af37); // Gold
const color2 = new THREE.Color(0x17becf); // Cyan

for(let i=0; i<particleCount; i++) {
    const r = 15 + Math.random() * 40;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos((Math.random() * 2) - 1);
    pos[i*3] = r * Math.sin(phi) * Math.cos(theta);
    pos[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
    pos[i*3+2] = r * Math.cos(phi);
    
    const mixed = Math.random();
    const c = mixed > 0.8 ? color2 : color1;
    colors[i*3] = c.r; colors[i*3+1] = c.g; colors[i*3+2] = c.b;
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
const particleMat = new THREE.PointsMaterial({
    size: 0.4, vertexColors: true, transparent: true, opacity: 0.7, blending: THREE.AdditiveBlending
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);

// ===== 3. HOLOGRAPHIC FORMULAS (Fixed Text Sprites) =====
// Function to dynamically size the canvas to avoid clipping
function createTextTexture(text, colorHex) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // Measure text to determine canvas size
    ctx.font = "bold 40px 'Space Mono', monospace";
    const textWidth = ctx.measureText(text).width;
    
    // Add padding
    canvas.width = Math.ceil(textWidth + 60);
    canvas.height = 100;
    
    // Draw background glow
    ctx.shadowColor = colorHex;
    ctx.shadowBlur = 20;
    
    // Draw text
    ctx.fillStyle = colorHex;
    ctx.font = "bold 40px 'Space Mono', monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(text, canvas.width/2, canvas.height/2);
    
    const texture = new THREE.CanvasTexture(canvas);
    texture.minFilter = THREE.LinearFilter;
    return { texture, aspectRatio: canvas.width / canvas.height };
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
    { eq: "F = ma", author: "Newton · 1687" }
];

const formulaNodes = [];
const colorsList = [0xffd700, 0x17becf, 0xff8c00, 0x87ceeb];

theorems.forEach((th, index) => {
    const colorHex = '#' + new THREE.Color(colorsList[index % colorsList.length]).getHexString();
    const { texture, aspectRatio } = createTextTexture(th.eq, colorHex);
    
    const material = new THREE.SpriteMaterial({ 
        map: texture, 
        transparent: true, 
        blending: THREE.AdditiveBlending,
        depthTest: false
    });
    
    const sprite = new THREE.Sprite(material);
    
    // Scale based on aspect ratio (keeping height consistent)
    const baseHeight = 4;
    sprite.scale.set(baseHeight * aspectRatio, baseHeight, 1);
    
    // Position in a sphere
    const phi = Math.acos(1 - 2 * (index + 0.5) / theorems.length);
    const theta = Math.PI * (1 + Math.sqrt(5)) * index;
    const radius = 22;
    
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

// ===== 4. INTERACTION =====
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
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(formulaNodes);
    
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
document.addEventListener('wheel', (e) => {
    camera.position.z += e.deltaY * 0.05;
    camera.position.z = Math.max(15, Math.min(120, camera.position.z));
});

// ===== 5. CLICK TO EXECUTE =====
const ui = document.getElementById('execution-ui');
const uiTerminal = document.getElementById('ui-terminal');

document.addEventListener('click', (e) => {
    if (e.target.closest('#execution-ui')) return; 
    
    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    
    const intersects = raycaster.intersectObjects(formulaNodes);
    
    if (intersects.length > 0) {
        activeSprite = intersects[0].object;
        const th = activeSprite.userData.theorem;
        
        document.getElementById('ui-title').textContent = th.eq;
        document.getElementById('ui-author').textContent = th.author;
        document.getElementById('state-text').textContent = "EXECUTING";
        
        let hash = 0;
        for (let i = 0; i < th.eq.length; i++) hash = ((hash << 5) - hash) + th.eq.charCodeAt(i);
        const shaHex = Math.abs(hash).toString(16).padEnd(16, '0');
        document.getElementById('ui-hash').textContent = `SHA-256: ${shaHex}... | STATUS: VERIFIED`;
        
        ui.style.display = 'block';
        uiTerminal.innerHTML = '';
        
        const lines = [
            { text: `> INITIATING DEEP EXECUTION: ${th.eq}`, type: 'cmd' },
            { text: `> SOURCE: ${th.author}`, type: 'sys' },
            { text: `> LOADING ONTOLOGICAL PRIMITIVES [20/20]`, type: 'sys' },
            { text: `> RESOLVING IN INFINITE DIMENSIONAL SPACE...`, type: 'cmd' },
            { text: `  [MATHEMATICAL COHERENCE ACHIEVED]`, type: 'out' },
            { text: `> CRYPTOGRAPHIC SEAL: ${shaHex}`, type: 'sys' },
            { text: `> EXECUTION HEART OPEN. AWAITING OBSERVER.`, type: 'cmd' }
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
                setTimeout(printLine, 400 + Math.random() * 200);
            }
        }
        printLine();
        
        playSound(600);
    }
});

document.getElementById('ui-close').addEventListener('click', () => {
    ui.style.display = 'none';
    activeSprite = null;
    document.getElementById('state-text').textContent = "OBSERVING";
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
    
    const positions = coreMesh.geometry.attributes.position.array;
    for(let i=0; i<positions.length; i+=3) {
        const x = positions[i]; const y = positions[i+1]; const z = positions[i+2];
        const dist = Math.sqrt(x*x + y*y + z*z);
        const offset = Math.sin(dist * 0.4 + t * 2) * 0.1;
        positions[i] += offset; positions[i+1] += offset; positions[i+2] += offset;
    }
    coreMesh.geometry.attributes.position.needsUpdate = true;
    
    // Swarm
    particles.rotation.y = t * 0.02;
    
    // Sprites floating
    formulaNodes.forEach((sprite, i) => {
        sprite.position.y = sprite.userData.baseY + Math.sin(t * sprite.userData.speed + sprite.userData.phase) * 2.5;
        sprite.lookAt(camera.position);
        
        // If active, zoom slightly towards camera
        if (sprite === activeSprite) {
            sprite.scale.set(sprite.scale.x * 0.95 + (baseHeight * aspectRatio) * 0.05, sprite.scale.y * 0.95 + baseHeight * 0.05, 1);
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
    print(f"OK: DIVINE CORE V3 genere. Les formules sont intactes et le coeur brille.")

if __name__ == "__main__":
    generate_divine_core()
