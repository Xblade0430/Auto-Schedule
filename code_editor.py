import argparse
from ai_engine import AIEngine

class AICodeEditor:
    """AI-powered code editor that applies changes to a file."""
    def __init__(self, engine: AIEngine | None = None):
        self.engine = engine or AIEngine()

    def apply_edit(self, path: str, instruction: str) -> str:
        """Use the AI engine to rewrite a file according to an instruction."""
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
        prompt = (
            "You are a helpful coding assistant. "
            "Edit the following file according to the instruction. "
            "Return ONLY the updated file content.\n" 
            f"Instruction:\n{instruction}\n" 
            "Current file:\n" + original
        )
        updated = self.engine.ask(prompt)
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        return updated

def main():
    parser = argparse.ArgumentParser(description="Edit a code file with AI")
    parser.add_argument("file")
    parser.add_argument("instruction")
    args = parser.parse_args()
    editor = AICodeEditor()
    editor.apply_edit(args.file, args.instruction)
    print(f"Updated {args.file} using AI")

if __name__ == "__main__":
    main()