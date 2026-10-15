import sys
import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# ==============================================================================
# 1. PAGE SETUP (Must run first before anything else)
# ==============================================================================
st.set_page_config(
    page_title="Soil Physics & Geotechnical Virtual Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Anchor BASE_DIR safely to the folder containing app.py
BASE_DIR = Path(__file__).resolve().parent

st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .lab-banner {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        padding: 1.25rem 1.75rem;
        border-radius: 0.75rem;
        color: #ffffff;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .lab-pill {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

MODULES = {
    "porosity": {
        "title": "Soil Porosity (n) & Void Ratio (e) Laboratory",
        "file": "Soil_Porosity_VoidRatio_Lab.html",
        "standard": "IS 2720 (Part 3)",
        "icon": "🧽",
        "height": 1100,
        "summary": "2 mm sieved soil saturation method with volumetric phase breakdown (Solids, Water, Air voids)."
    },
    "sieve_shaker": {
        "title": "Mechanical Sieve Shaker & Grain Size Distribution",
        "file": "Comprehensive_Sieve_Shaker_Lab_Rays.html",
        "standard": "IS 2720 (Part 4) • ASTM D6913",
        "icon": "⚖️",
        "height": 1150,
        "summary": "Vibrating mechanical sieve shaker with D10/D30/D60 ray tracing and Hazen permeability."
    },
    "geosieve_pro": {
        "title": "GeoSieve Pro: Interactive Particle Curve Studio",
        "file": "GeoSieve_Pro_Studio.html",
        "standard": "IS 1498 • ASTM D2487",
        "icon": "📊",
        "height": 1150,
        "summary": "Geotechnical sieve analysis studio with mass loss audit and automated USCS soil classification."
    },
     "atterberg": {
        "title": "Atterberg Limits & Soil Plasticity Studio",
        "file": "Atterberg_Limits_Studio_MultiTrial.html",
        "standard": "IS 2720 (Part 5 & 6) • ASTM D4318",
        "icon": "🥣",
        "height": 1200,
        "summary": "Casagrande liquid limit, 3mm thread plastic limit, shrinkage limit, and Casagrande A-line chart."
    },
    "darcy": {
        "title": "Darcy's Law Permeameter & Hydraulic Conductivity",
        "file": "darcy_permeameter_lab.html",
        "standard": "ASTM D2434 • ASTM D5084",
        "icon": "💧",
        "height": 1150,
        "summary": "Constant and falling head permeameter simulation with live flow vectors and temperature correction."
    },
    "hydrometer": {
        "title": "Soil Hydrometer Sedimentation Analysis (< 75 µm)",
        "file": "Soil_Hydrometer_Analysis_Lab.html",
        "standard": "IS 2720 (Part 4) • ASTM D7928",
        "icon": "🧪",
        "height": 1200,
        "summary": "Stokes' law sedimentation simulation for silt and clay fractions using a 152H hydrometer."
    },
    "proctor": {
        "title": "Standard & Modified Proctor Compaction Test",
        "file": "proctor_compaction_lab.html",
        "standard": "ASTM D698 • D1557 • IS 2720",
        "icon": "🚜",
        "height": 1100,
        "summary": "Determine Maximum Dry Density (MDD), Optimum Moisture Content (OMC), and Zero Air Voids (ZAV) curves."
    }
    
}

with st.sidebar:
    st.title("🧪 Virtual Soil Lab")
    
    module_keys = list(MODULES.keys())
    module_labels = [f"{MODULES[k]['icon']} {MODULES[k]['title']}" for k in module_keys]
    
    selected_idx = st.radio(
        "Select Experiment:",
        range(len(module_keys)),
        format_func=lambda i: module_labels[i]
    )
    
    active_key = module_keys[selected_idx]
    active_module = MODULES[active_key]
    
    st.divider()
    
    target_file = BASE_DIR / active_module["file"]
    
    if target_file.is_file():
        try:
            with open(target_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            st.download_button(
                label=f"💾 Download {active_module['file']}",
                data=content,
                file_name=active_module["file"],
                mime="text/html",
                use_container_width=True
            )
        except Exception as e:
            st.caption(f"Download unavailable: {e}")
    else:
        st.warning(f"File missing from folder: `{active_module['file']}`")

    st.markdown("---")
    st.caption("Educational Laboratory Suite • Soil & Water Conservation Engineering")

st.markdown(f"""
<div class="lab-banner">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;">
        <div>
            <h2 style="margin:0; font-size:1.35rem; font-weight:700;">
                {active_module['icon']} {active_module['title']}
            </h2>
            <p style="margin:0.25rem 0 0 0; font-size:0.85rem; opacity:0.95;">
                {active_module['summary']}
            </p>
        </div>
        <div>
            <span class="lab-pill">{active_module['standard']}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

target_file = BASE_DIR / active_module["file"]

if not target_file.exists():
    st.error(f"""
    ### ❌ File Not Found
    Could not find `{active_module['file']}` in the app directory:
    `{BASE_DIR}`
    
    **How to fix:**
    Make sure your HTML file is placed in the exact same directory as `app.py`, with exact spelling and casing.
    """)
else:
    try:
        with open(target_file, "r", encoding="utf-8", errors="replace") as f:
            html_content = f.read().strip()
            
        if len(html_content) < 50 or "<!-- Paste your" in html_content:
            st.warning(f"""
            ### ⚠️ File is Empty or Unfilled: `{active_module['file']}`
            The file exists on disk, but only contains placeholder comments. 
            Open `{active_module['file']}` in your editor, paste your HTML lab code inside, and save.
            """)
        else:
            # Action controls bar directly above the workspace
            col_a, col_b = st.columns([1, 4])
            with col_a:
                # Render direct button to open the HTML in a new tab if browser blocks iframe
                b64_html = base64.b64encode(html_content.encode("utf-8")).decode("utf-8")
                href = f'data:text/html;base64,{b64_html}'
                st.markdown(
                    f'<a href="{href}" target="_blank" style="display:inline-block; padding:0.4rem 0.8rem; background:#0284c7; color:white; border-radius:0.5rem; text-decoration:none; font-size:0.82rem; font-weight:600;">↗ Open in Full Tab</a>',
                    unsafe_allow_html=True
                )
            with col_b:
                st.caption(f"Rendering: `{active_module['file']}` ({len(html_content):,} bytes loaded)")

            # Render interactive component
            components.html(
                html_content,
                height=active_module.get("height", 1150),
                scrolling=True
            )
            
    except Exception as err:
        st.error(f"Error reading `{active_module['file']}`: {err}")

with st.expander("🛠️ Debug & Directory Status (Click to inspect if anything is missing)", expanded=False):
    st.write(f"**Python executable:** `{sys.executable}`")
    st.write(f"**Application folder:** `{BASE_DIR}`")
    files_on_disk = sorted([p.name for p in BASE_DIR.glob("*") if p.is_file()])
    st.write(f"**Files detected in folder ({len(files_on_disk)} total):**")
    st.code("\n".join(files_on_disk) if files_on_disk else "No files found in folder!")
