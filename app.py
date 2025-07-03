import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Tetris Game", layout="wide")

# Custom CSS for outstanding UI
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<style>
body {
    background: linear-gradient(135deg, #1e3a8a, #7c3aed);
}
.stApp {
    background: transparent;
}
.game-container {
    animation: fadeIn 1s ease-in-out;
}
@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

st.title("🎮 Tetris Game")
st.markdown("A modern take on the classic Tetris game with a vibrant UI!")

# Embed PyGame with Pyodide
html("""
<script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>
<script>
async function main() {
    let pyodide = await loadPyodide();
    await pyodide.loadPackage("pygame");
    await pyodide.runPythonAsync(`
        import js
        from pyodide.http import pyfetch
        response = await pyfetch("tetris.py")
        code = await response.string()
        exec(code)
    `);
}
main();
</script>
<canvas id="pygame" width="300" height="600"></canvas>
""", height=600)

# Sidebar with controls and score
with st.sidebar:
    st.header("Controls")
    st.markdown("""
    - **Left Arrow**: Move left
    - **Right Arrow**: Move right
    - **Down Arrow**: Move down
    - **Up Arrow**: Rotate
    """)
    st.header("Score")
    st.markdown("**Score**: 0 (Updated dynamically in production)")
    if st.button("Start/Pause"):
        st.write("Game started!")  # Placeholder for game control
