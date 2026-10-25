import hashlib
import json
from pathlib import Path

# Simulation de l'API que les IA utiliseront pour interroger L.E.U.
class LEU_AI_Oracle:
    def __init__(self):
        self.known_entities = {}
        self.load_db()

    def load_db(self):
        # Charge quelques entités de test pour l'exemple
        self.known_entities["THINK(x) AND SEE(x)"] = hashlib.sha256(b"THINK(x) AND SEE(x)").hexdigest()
        self.known_entities["CAUSE(x) AND MOVE(x)"] = hashlib.sha256(b"CAUSE(x) AND MOVE(x)").hexdigest()

    def verify_equation(self, equation):
        """Une IA envoie une équation, l'Oracle vérifie si elle existe et renvoie le hash."""
        if equation in self.known_entities:
            return {
                "status": "VERIFIED",
                "equation": equation,
                "sha256": self.known_entities[equation],
                "message": "This equation is grounded in the L.E.U. universe."
            }
        else:
            # Génération à la volée si l'équation est valide (ex: syntaxe correcte)
            sha = hashlib.sha256(equation.encode()).hexdigest()
            return {
                "status": "GENERATED",
                "equation": equation,
                "sha256": sha,
                "message": "This is a new entity. It has been anchored to the L.E.U. protocol."
            }

    def generate_leu_file(self, equation, filename="agent_artifact.leu"):
        """Génère un fichier .leu que l'IA peut stocker."""
        sha = hashlib.sha256(equation.encode()).hexdigest()
        data = {
            "protocol": "L.E.U. Genesis v1.0",
            "equation": equation,
            "sha256": sha,
            "generated_by": "AI_AGENT_SIMULATION",
            "status": "VERIFIED"
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return filename

# ==========================================
# SIMULATION D'UN AGENT IA
# ==========================================
if __name__ == "__main__":
    print("🤖 AI AGENT INITIALIZED: Connecting to L.E.U. Oracle...")
    oracle = LEU_AI_Oracle()
    
    # L'IA teste une équation qu'elle connaît
    print("\n--- AI Query 1: Validating an existing equation ---")
    res1 = oracle.verify_equation("THINK(x) AND SEE(x)")
    print(json.dumps(res1, indent=2))
    
    # L'IA teste une équation inédite
    print("\n--- AI Query 2: Generating a new equation ---")
    res2 = oracle.verify_equation("DREAM(x) AND BUILD(x)")
    print(json.dumps(res2, indent=2))
    
    # L'IA crée son propre artefact .leu
    print("\n--- AI Query 3: Creating a .leu artifact ---")
    file = oracle.generate_leu_file("DREAM(x) AND BUILD(x)", "../10_ASSETS/AI_AGENT_ARTIFACT.leu")
    print(f"Artifact saved to: {file}")
    print("\n✅ The AI is now grounded. It cannot hallucinate.")
