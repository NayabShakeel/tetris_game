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
.leaderboard-table {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎮 Tetris Game")
st.markdown("A modern take on the classic Tetris game with a vibrant UI!")

# Initialize session state for score and leaderboard
if "score" not in st.session_state:
    st.session_state.score = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

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
        # Mount sound files
        response = await pyfetch("assets/sfx/land.wav")
        with open("assets/sfx/land.wav", "wb") as f:
            f.write(await response.bytes())
        response = await pyfetch("assets/sfx/clear.wav")
        with open("assets/sfx/clear.wav", "wb") as f:
            f.write(await response.bytes())
        response = await pyfetch("assets/sfx/gameover.wav")
        with open("assets/sfx/gameover.wav", "wb") as f:
            f.write(await response.bytes())
        # Run Tetris
        response = await pyfetch("tetris.py")
        code = await response.string()
        exec(code)
    `);
}
main();
</script>
<canvas id="pygame" width="300" height="600"></canvas>
""", height=600)

# Sidebar with controls, score, and leaderboard
with st.sidebar:
    st.header("Controls")
    st.markdown("""
    - **Left Arrow**: Move left
    - **Right Arrow**: Move right
    - **Down Arrow**: Move down
    - **Up Arrow**: Rotate
    """)
    st.header("Score")
    st.markdown(f"**Score**: {st.session_state.score}")
    player_name = st.text_input("Player Name", "Player")
    if st.button("Start/Pause"):
        st.session_state.score = 0  # Reset score on start
        st.write("Game started!")
    if st.button("Submit Score") and st.session_state.score > 0:
        st.session_state.leaderboard.append({"name": player_name, "score": st.session_state.score})
        st.session_state.leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x["score"], reverse=True)[:5]  # Keep top 5
    st.header("Leaderboard")
    if st.session_state.leaderboard:
        st.markdown("<div class='leaderboard-table'>", unsafe_allow_html=True)
        st.table(st.session_state.leaderboard)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.write("No scores yet!")
