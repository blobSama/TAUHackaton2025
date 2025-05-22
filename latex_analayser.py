import re
from pylatexenc.latex2text import LatexNodes2Text

# --- Prompt user for LaTeX proof input ---
def get_proof_input():
    print("Paste your LaTeX proof below. Enter '$0' on a new line to finish:")
    proof = ''
    while True:
        line = input()
        if line.strip() == '$0':
            break
        proof += line + '\n'
    if not proof.strip():
        print("No input detected. Using default example.")
        proof = r"""
        \begin{proof}
        Let $x$ be a real number. Assume $x > 0$. Then $x^2 > 0$. \\ Therefore, the square of any positive real number is positive.
        \end{proof}
        """
    return proof

# --- Keywords for simple classification ---
KEYWORDS = {
    'assumption': [r'let ', r'lets', r'assume', r'asume' ,r'suppose', r'supose', r'given', r'for all', r'for any'],
    'inference': [r'then', r'it follows', r'hence', r'so', r'thus', r'implies'],
    'conclusion': [r'therefore', r'we conclude', r'we have shown', r'proved', r'hence proved'],
    'induction': [r'by induction', r'inductive', r'base case', r'inductive step'],
    'contradiction': [r'contradiction', r'assume the contrary', r'suppose not', r'leads to a contradiction'],
    'case': [r'case ', r'cases:', r'consider the case', r'if ', r'otherwise'],
    'claim': [r'claim', r'true', r'false', r'True', r'False']
}

# --- Improved LaTeX cleaning ---
def clean_latex(text):
    # Convert LaTeX to plain text using pylatexenc
    plain = LatexNodes2Text().latex_to_text(text)
    # Remove extra spaces and newlines
    plain = re.sub(r'\s+', ' ', plain)
    return plain.strip()

# --- Improved step splitting ---
def split_proof(proof_text):
    # Split on LaTeX sectioning (e.g., \textbf{...}), double newlines, or LaTeX line breaks (\\)
    # Keep math expressions as part of the step
    # First, split on \textbf{...} and keep the marker
    parts = re.split(r'(\\textbf\{[^}]+\})', proof_text)
    steps = []
    buffer = ''
    for part in parts:
        if re.match(r'\\textbf\{[^}]+\}', part):
            if buffer.strip():
                steps.extend(re.split(r'\n\s*\n|\\\\', buffer))
                buffer = ''
            steps.append(part)
        else:
            buffer += part
    if buffer.strip():
        steps.extend(re.split(r'\n\s*\n|\\\\', buffer))
    # Flatten and clean
    cleaned_steps = []
    for step in steps:
        cleaned = clean_latex(step)
        if cleaned:
            cleaned_steps.extend([s.strip() for s in re.split(r'[.;]\s*', cleaned) if s.strip()])
    return cleaned_steps

# --- Classify each step ---
def classify_step(step):
    step_lower = step.lower()
    for label, patterns in KEYWORDS.items():
        for pat in patterns:
            if re.search(pat, step_lower):
                return label
    return 'other'

# --- Main analysis ---
def main():
    proof = get_proof_input()
    steps = split_proof(proof)
    print("\nProof analysis:\n")
    for idx, step in enumerate(steps, 1):
        label = classify_step(step)
        print(f"Step {idx}: {step} [{label}]")

if __name__ == "__main__":
    main() 