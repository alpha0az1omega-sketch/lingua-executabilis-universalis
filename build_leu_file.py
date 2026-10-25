import zipfile
from pathlib import Path

def build_leu_file():
    root = Path.cwd()
    leu_file = root / "04_ARTIFACTS" / "lingua_universalis.leu"
    leu_file.parent.mkdir(exist_ok=True, parents=True)
    
    with zipfile.ZipFile(leu_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 1. L'Agentic Glyph (le cœur)
        zf.write(root / "04_ARTIFACTS" / "svg" / "glyph_agentic_v2.svg", "agent.svg")
        
        # 2. Le Lexique (les 20 primitives)
        zf.write(root / "01_SPECIFICATION" / "primitive_lexicon.json", "lexicon.json")
        
        # 3. Un petit fichier readme interne
        readme = "LINGUA EXECUTABILIS UNIVERSALIS (L.E.U.)\nThis is an intelligent archive. \nOpen 'agent.svg' in a web browser to interact with the Agentic Glyph."
        zf.writestr("README.txt", readme)
        
    print(f"Fichier intelligent généré : {leu_file}")
    print("Vous pouvez l'envoyer par mail, le partager, ou l'archiver.")

if __name__ == "__main__":
    build_leu_file()
