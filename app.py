import streamlit as st
import os
import re
import chardet

EXAMPLES_DIR = "nx_examples"  # Folder with your NX example scripts

# Get all example Python files
example_files = [f for f in os.listdir(EXAMPLES_DIR) if f.endswith(".py")]

st.title("🤖 NX CodeBot (Python Generator)")
st.write("Ask me to generate NXOpen Python code! Examples: create block, unite, fillet, extract region, etc.")

example_selected = st.selectbox("Select an operation:", example_files)

st.write("Optional Parameters (if any)")
param_input = st.text_input("Enter parameters separated by comma (e.g., 100,100,50 for block)")

def read_script_auto_encode(path):
    # Read file bytes and detect encoding with chardet
    with open(path, "rb") as f:
        raw_data = f.read()
    detected = chardet.detect(raw_data)
    encoding = detected.get('encoding', 'utf-8') or 'utf-8'
    try:
        return raw_data.decode(encoding)
    except Exception:
        # Fallback to utf-8 ignoring errors if detection fails
        return raw_data.decode("utf-8", errors="ignore")

if st.button("Generate Code"):
    example_path = os.path.join(EXAMPLES_DIR, example_selected)
    try:
        code = read_script_auto_encode(example_path)
        params = [p.strip() for p in param_input.split(",")] if param_input.strip() else []
        matches = re.findall(r"\{param(\d+)\}", code)
        max_param = max([int(m) for m in matches], default=0)
        for i in range(1, max_param + 1):
            param_val = params[i-1] if len(params) >= i else "0"
            code = code.replace(f"{{param{i}}}", param_val)
        st.code(code, language="python")
    except FileNotFoundError:
        st.error(f"❌ File not found: {example_selected}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

st.info(
    "Instructions:\n"
    "1. Select the operation.\n"
    "2. Provide parameters if needed.\n"
    "3. Copy the generated code and run inside NX Journal."
)
