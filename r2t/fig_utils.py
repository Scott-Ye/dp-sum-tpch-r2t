import matplotlib.pyplot as plt
from pathlib import Path

def set_style():
    try:
        plt.style.use("seaborn-v0_8")
    except Exception:
        pass

def save_fig(out_path_png: str):
    Path(out_path_png).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path_png, dpi=220)
    if out_path_png.endswith(".png"):
        plt.savefig(out_path_png.replace(".png", ".svg"))

