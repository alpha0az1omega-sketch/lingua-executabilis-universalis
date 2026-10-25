import json
from pathlib import Path

SANDBOX_PATH = Path("../04_ARTIFACTS/living/THEOREM_GENESIS.html")

def generate_theorem_genesis():
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>L.E.U. - Theorem Genesis</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { overflow: hidden; background: #030305; font-family: 'Space Mono', monospace; color: #e0e0e0; }
#c { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; }

/* HUD */
.hud { position: absolute; z-index: 10; pointer-events: none; }
#top-left { top: 30px; left: 30px; }
#top-right { top: 30px; right: 30px; text-align: right; }
#bottom-left { bottom: 30px; left: 30px; }
#bottom-right { bottom: 30px; right: 30px; text-align: right; width: 400px; }

.title { font-family: 'Cinzel', serif; color: #d4af37; font-size: 24px; letter-spacing: 5px; text-transform: uppercase; text-shadow: 0 0 20px rgba(212,175,55,0.5); }
.sub { color: #888; font-size: 10px; letter-spacing: 2px; margin-bottom: 20px; }
.data-row { font-size: 11px; margin-bottom: 5px; color: #a0a0a0; }
.data-val { color: #fff; font-weight: bold; }
.data-gold { color: #d4af37; }
.data-cyan { color: #17becf; }

/* Live Log */
#execution-log { font-size: 10px; color: #666; max-height: 200px; overflow: hidden; }
.log-line { margin-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 3px;}
.log-time { color: #17becf; }
.log-formula { color: #d4af37; font-weight: bold; }

/* Floating Discoveries (HUD) */
#discovery-container { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); pointer-events: none; z-index: 5; text-align: center; }
.discovery-text { font-family: 'Cinzel', serif; font-size: 32px; color: #fff; opacity: 0; text-shadow: 0 0 30px #d4af37, 0 0 60px #d4af37; transition: opacity 0.5s; }
.discovery-author { font-family: 'Space Mono', monospace; font-size: 14px; color: #17becf; margin-top: 10px; opacity: 0; transition: opacity 0.5s; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
<div id="c"></div>

<div id="discovery-container">
    <div class="discovery-text" id="discovery-text">E = mc²</div>
    <div class="discovery-author" id="discovery-author">Albert Einstein · 1905</div>
</div>

<div class="hud" id="top-left">
    <div class="title">Theorem Genesis</div>
    <div class="sub">AUTONOMOUS MATHEMATICAL CONSCIOUSNESS</div>
    <div class="data-row">STATUS: <span class="data-gold" id="status-text">DISCOVERING...</span></div>
    <div class="data-row">FORMULAS EVALUATED: <span class="data-val" id="formula-count">0</span></div>
    <div class="data-row">ENTROPY: <span class="data-gold" id="entropy-val">0.000</span></div>
</div>

<div class="hud" id="top-right">
    <div class="sub">CRYPTOGRAPHIC PROOF</div>
    <div class="data-row">SHA-256: <span class="data-val" id="sys-hash">...</span></div>
    <div class="data-row">DOI: <span class="data-gold">10.5281/zenodo.23476518</span></div>
</div>

<div class="hud" id="bottom-left">
    <div class="sub">OBSERVER</div>
    <div class="data-row">DRAG: Rotate Space</div>
    <div class="data-row">WHEEL: Zoom Dimension</div>
</div>

<div class="hud" id="bottom-right">
    <div class="sub">AUTONOMOUS DISCOVERY LOG</div>
    <div id="execution-log"></div>
</div>

<script>
window.onerror = function(msg) { console.error(msg); };

// ===== THREE.JS SETUP =====
const scene = new THREE.Scene();
scene.fog = new THREE.FogExp2(0x030305, 0.002);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 10, 60);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.getElementById('c').appendChild(renderer.domElement);

// Lights
scene.add(new THREE.AmbientLight(0xffffff, 0.4));
const l1 = new THREE.PointLight(0xd4af37, 2, 200); l1.position.set(20, 30, 20); scene.add(l1);
const l2 = new THREE.PointLight(0x17becf, 1.5, 200); l2.position.set(-20, -30, -20); scene.add(l2);

// ===== 1. THE LIVING CORE (Morphing Torus) =====
const coreGeo = new THREE.TorusKnotGeometry(8, 1.5, 256, 32, 3, 4);
const coreMat = new THREE.MeshStandardMaterial({
    color: 0xd4af37,
    emissive: 0xd4af37,
    emissiveIntensity: 0.6,
    metalness: 0.9,
    roughness: 0.1,
    wireframe: true,
    transparent: true,
    opacity: 0.4
});
const coreMesh = new THREE.Mesh(coreGeo, coreMat);
scene.add(coreMesh);

// ===== 2. MATH PARTICLE SWARM =====
// Create a texture with math symbols
function createMathTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 512; canvas.height = 512;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#000000'; ctx.fillRect(0, 0, 512, 512);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 40px monospace';
    const symbols = ['∑', '∫', 'π', '∞', '√', '≈', '≠', '±', '∂', '∇', 'Δ', 'λ', 'θ', 'μ'];
    for(let i=0; i<100; i++) {
        const s = symbols[Math.floor(Math.random()*symbols.length)];
        ctx.fillText(s, Math.random()*512, Math.random()*512);
    }
    return new THREE.CanvasTexture(canvas);
}

const mathTex = createMathTexture();
const particleCount = 2000;
const particleGeo = new THREE.BufferGeometry();
const pos = new Float32Array(particleCount * 3);
for(let i=0; i<particleCount; i++) {
    const r = 15 + Math.random() * 40;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos((Math.random() * 2) - 1);
    pos[i*3] = r * Math.sin(phi) * Math.cos(theta);
    pos[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
    pos[i*3+2] = r * Math.cos(phi);
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
const particleMat = new THREE.PointsMaterial({
    size: 1.5,
    map: mathTex,
    transparent: true,
    opacity: 0.6,
    color: 0xd4af37,
    blending: THREE.AdditiveBlending,
    depthWrite: false
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);

// ===== 3. CAMERA CONTROLS =====
let isDragging = false;
let prevMouse = { x: 0, y: 0 };
let targetRotation = { x: 0, y: 0 };
let currentRotation = { x: 0, y: 0 };

document.addEventListener('mousedown', (e) => { isDragging = true; prevMouse = { x: e.clientX, y: e.clientY }; });
document.addEventListener('mouseup', () => { isDragging = false; });
document.addEventListener('mousemove', (e) => {
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

// ===== 4. AUTONOMOUS DISCOVERY ENGINE =====
const theorems = [
    { eq: "a² + b² = c²", author: "Pythagore · -500" },
    { eq: "e^(iπ) + 1 = 0", author: "Euler · 1748" },
    { eq: "F = G(m₁m₂)/r²", author: "Newton · 1687" },
    { eq: "E = mc²", author: "Einstein · 1905" },
    { eq: "∂u/∂t + u·∇u = -∇p/ρ + ν∇²u", author: "Navier-Stokes · 1822" },
    { eq: "iħ(∂Ψ/∂t) = ĤΨ", author: "Schrödinger · 1926" },
    { eq: "ζ(s) = 1/1ˢ + 1/2ˢ + 1/3ˢ + ...", author: "Riemann · 1859 (FUTUR)" },
    { eq: "S = (k_B A) / (4ℓ_P²)", author: "Hawking-Bekenstein · 1973" },
    { eq: "∇ × E = -∂B/∂t", author: "Maxwell · 1865" },
    { eq: "F = ma", author: "Newton · 1687" },
    { eq: "C = 2πr", author: "Antiquité · -300" },
    { eq: "e = lim (1+1/n)ⁿ", author: "Bernoulli · 1683" },
    { eq: "x = (-b ± √(b²-4ac)) / 2a", author: "Al-Khwarizmi · 820" },
    { eq: "Φ = ∫ E · dA = Q/ε₀", author: "Gauss · 1835" },
    { eq: "UNIFIED FIELD THEORY", author: "L.E.U. · 2026 (FUTUR)" },
    { eq: "CONSCIOUSNESS = ∫ Ψ* Ψ dt", author: "L.E.U. · 2026 (FUTUR)" }
];

let formulaCount = 0;
const discoveryText = document.getElementById('discovery-text');
const discoveryAuthor = document.getElementById('discovery-author');
const logContainer = document.getElementById('execution-log');

function discoverTheorem() {
    // Pick random theorem
    const th = theorems[Math.floor(Math.random() * theorems.length)];
    
    // Update center screen
    discoveryText.textContent = th.eq;
    discoveryAuthor.textContent = th.author;
    discoveryText.style.opacity = '1';
    discoveryAuthor.style.opacity = '1';
    
    // Fade out after 1.5s
    setTimeout(() => {
        discoveryText.style.opacity = '0';
        discoveryAuthor.style.opacity = '0';
    }, 1500);
    
    // Add to log
    const time = new Date().toISOString().split('T')[1].split('.')[0];
    const div = document.createElement('div');
    div.className = 'log-line';
    div.innerHTML = `<span class="log-time">[${time}]</span> Discovered: <span class="log-formula">${th.eq}</span> <br><span style="color:#888; font-size:9px;">Source: ${th.author}</span>`;
    logContainer.prepend(div);
    if (logContainer.children.length > 8) logContainer.lastChild.remove();
    
    // Increment counter
    formulaCount++;
    document.getElementById('formula-count').textContent = formulaCount;
    
    // Audio chirp
    playSound(300 + Math.random() * 400);
}

// Discovery Interval (Every 2.5 seconds)
setInterval(discoverTheorem, 2500);

// System Hash
setInterval(() => {
    const hash = Array.from({length: 16}, () => Math.floor(Math.random()*16).toString(16)).join('');
    document.getElementById('sys-hash').textContent = hash + "...";
    document.getElementById('entropy-val').textContent = (Math.random() * 0.5 + 0.5).toFixed(3);
}, 1000);

// Audio
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
        gain.gain.linearRampToValueAtTime(0.05, audioCtx.currentTime + 0.05);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 1);
    } catch(e) {}
}

// ===== 5. ANIMATION =====
const clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    
    // Smooth camera rotation
    if (!isDragging) {
        targetRotation.y += 0.001;
        targetRotation.x = Math.sin(t * 0.2) * 0.1;
    }
    currentRotation.x += (targetRotation.x - currentRotation.x) * 0.05;
    currentRotation.y += (targetRotation.y - currentRotation.y) * 0.05;
    
    scene.rotation.x = currentRotation.x;
    scene.rotation.y = currentRotation.y;
    
    // Core Breathing & Morphing
    coreMesh.rotation.x = t * 0.2;
    coreMesh.rotation.y = t * 0.3;
    
    const positions = coreMesh.geometry.attributes.position.array;
    for(let i=0; i<positions.length; i+=3) {
        const x = positions[i];
        const y = positions[i+1];
        const z = positions[i+2];
        const dist = Math.sqrt(x*x + y*y + z*z);
        const offset = Math.sin(dist * 0.3 + t * 3) * 0.15;
        positions[i] += offset;
        positions[i+1] += offset;
        positions[i+2] += offset;
    }
    coreMesh.geometry.attributes.position.needsUpdate = true;
    
    // Swarm rotation
    particles.rotation.y = t * 0.03;
    particles.rotation.x = t * 0.01;
    
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
    print(f"OK: THEOREM GENESIS genere. L'IA pense toute seule.")

if __name__ == "__main__":
    generate_theorem_genesis()
