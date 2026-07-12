#!/usr/bin/env python3
"""
Tutor de Matematica - IA Local para Concursos Publicos
Setup & Install script — automates everything from Node.js to Ollama to running the server.

Usage:
    python3 setup.py          # full setup + start server
    python3 setup.py --build  # only build frontend
    python3 setup.py --run    # only start server (after build)
    python3 setup.py --cloudflared  # also start cloudflare tunnel

Requirements:
    - Linux (Ubuntu/Debian recommended) or macOS
    - Python 3.8+
    - ~8 GB free RAM (for the AI model)
    - ~15 GB free disk (model + dependencies)
"""

from __future__ import annotations

import argparse
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import time
import urllib.request


# ── constants ────────────────────────────────────────────────────────────────
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
NODE_MIN_MAJOR = 22
OLLAMA_MODEL_SOURCE = "hf.co/unsloth/LFM2.5-8B-A1B-GGUF:UD-Q4_K_M"
OLLAMA_MODEL_NAME = "tutor-matematica"
OLLAMA_NUM_CTX = 131072
SERVER_PORT = 5173

# ── helpers ──────────────────────────────────────────────────────────────────


def run(cmd, *, check=True, shell=False, **kwargs):
    """Run a shell command, print it, and return the result."""
    label = cmd if isinstance(cmd, str) else " ".join(cmd)
    print(f"\n  >> {label}")
    return subprocess.run(cmd, check=check, shell=shell, **kwargs)


def is_tool(name):
    """Return True if `name` is on PATH."""
    return shutil.which(name) is not None


def get_node_major():
    """Return the major version of Node.js, or None."""
    try:
        out = subprocess.run(
            ["node", "--version"], capture_output=True, text=True, check=True
        )
        return int(out.stdout.strip().lstrip("v").split(".")[0])
    except Exception:
        return None


def platform_tag():
    """Return a short OS tag used for download URLs."""
    system = platform.system().lower()
    if system not in ("linux", "darwin"):
        sys.exit(f"Unsupported platform: {system}. Only Linux and macOS are supported.")
    return system


# ── steps ────────────────────────────────────────────────────────────────────


def install_nodejs():
    """Install Node.js >= NODE_MIN_MAJOR if missing or too old."""
    major = get_node_major()
    if major is not None and major >= NODE_MIN_MAJOR:
        print(f"  [OK] Node.js v{major} already installed")
        return

    print(f"  Installing Node.js {NODE_MIN_MAJOR}.x ...")
    tag = platform_tag()

    if tag == "linux":
        run(
            f"curl -fsSL https://deb.nodesource.com/setup_{NODE_MIN_MAJOR}.x | sudo -E bash -",
            shell=True,
            check=True,
        )
        run(["sudo", "apt-get", "install", "-y", "nodejs"])
    else:  # macOS
        if is_tool("brew"):
            run(["brew", "install", "node@22"])
        else:
            sys.exit("Homebrew not found. Install it first: https://brew.sh")

    major = get_node_major()
    if major is None or major < NODE_MIN_MAJOR:
        sys.exit(f"Node.js installation failed. Install Node.js {NODE_MIN_MAJOR}+ manually.")
    print(f"  [OK] Node.js v{major} installed")


def install_npm_deps():
    """Run npm install."""
    print("  Installing npm dependencies ...")
    run(["npm", "install"], cwd=PROJECT_ROOT)
    print("  [OK] Dependencies installed")


def build_frontend():
    """Run vite build."""
    print("  Building frontend (Vite) ...")
    run(["npm", "run", "build"], cwd=PROJECT_ROOT)
    print("  [OK] Frontend built -> dist/")


def install_ollama():
    """Install Ollama if not present."""
    if is_tool("ollama"):
        print("  [OK] Ollama already installed")
        _ensure_ollama_running()
        return

    print("  Installing Ollama ...")
    tag = platform_tag()

    if tag == "linux":
        run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
    else:
        if is_tool("brew"):
            run(["brew", "install", "ollama"])
        else:
            run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)

    print("  [OK] Ollama installed")
    _ensure_ollama_running()


def _ensure_ollama_running():
    """Start Ollama serve in background if not already running."""
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        print("  [OK] Ollama service already running")
        return
    except Exception:
        pass

    print("  Starting Ollama service ...")
    if platform.system() == "Linux":
        try:
            run(["sudo", "systemctl", "start", "ollama"])
            time.sleep(2)
            return
        except Exception:
            pass
        subprocess.Popen(
            ["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    else:
        subprocess.Popen(
            ["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    for _ in range(30):
        try:
            urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)


def pull_model():
    """Pull the base LFM 2.5 model."""
    try:
        out = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        if OLLAMA_MODEL_SOURCE.split(":")[0] in out.stdout:
            print(f"  [OK] Model {OLLAMA_MODEL_SOURCE} already cached")
            return
    except Exception:
        pass

    print(f"  Pulling model {OLLAMA_MODEL_SOURCE} (~5.2 GB, this may take a while) ...")
    run(["ollama", "pull", OLLAMA_MODEL_SOURCE])
    print("  [OK] Model downloaded")


def create_custom_model():
    """Create the tutor-matematica model with extended context."""
    try:
        out = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        if OLLAMA_MODEL_NAME in out.stdout:
            print(f"  [OK] Custom model '{OLLAMA_MODEL_NAME}' already exists")
            return
    except Exception:
        pass

    print(f"  Creating custom model '{OLLAMA_MODEL_NAME}' (num_ctx={OLLAMA_NUM_CTX}) ...")
    modelfile_path = PROJECT_ROOT / "Modelfile"
    if not modelfile_path.exists():
        modelfile_path.write_text(
            f"FROM {OLLAMA_MODEL_SOURCE}\nPARAMETER num_ctx {OLLAMA_NUM_CTX}\n",
            encoding="utf-8",
        )
    run(["ollama", "create", OLLAMA_MODEL_NAME, "-f", str(modelfile_path)])
    print(f"  [OK] Custom model '{OLLAMA_MODEL_NAME}' created")


def ensure_pdf_content():
    """Copy pdf_content.txt to public/ if not already there."""
    public_dir = PROJECT_ROOT / "public"
    public_dir.mkdir(exist_ok=True)
    dest = public_dir / "pdf_content.txt"
    if dest.exists():
        print("  [OK] pdf_content.txt already in public/")
        return
    candidates = [
        PROJECT_ROOT.parent / "guia_formula_combinatoria.txt",
        PROJECT_ROOT.parent / "pdf_content.txt",
    ]
    for src in candidates:
        if src.exists():
            shutil.copy2(src, dest)
            print(f"  [OK] Copied {src.name} -> public/pdf_content.txt")
            return
    dest.write_text(
        "Edital do Concurso Publico — conteudo de matematica.\n"
        "Carregue o PDF do edital para contextualizar o tutor.\n",
        encoding="utf-8",
    )
    print("  [WARN] pdf_content.txt placeholder created — replace with real edital PDF content")


def start_server(port=SERVER_PORT):
    """Start the Express server."""
    print(f"\n  Starting server on http://localhost:{port} ...")
    proc = subprocess.Popen(
        ["node", "server.js"],
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    try:
        urllib.request.urlopen(f"http://localhost:{port}", timeout=5)
        print(f"  [OK] Server running at http://localhost:{port}")
    except Exception:
        print(f"  [WARN] Server may still be starting — check http://localhost:{port}")
    return proc


def start_cloudflared(port=SERVER_PORT):
    """Start cloudflared tunnel if available."""
    if not is_tool("cloudflared"):
        print("  [INFO] cloudflared not installed — skipping tunnel setup")
        return None
    print("  Starting Cloudflare tunnel ...")
    proc = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://localhost:{port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    for _ in range(20):
        line = proc.stdout.readline()
        if line:
            print(f"     {line.rstrip()}")
        if "trycloudflare.com" in line or "try.cloudflare.com" in line:
            break
    return proc


# ── main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Tutor de Matematica — IA Local Setup")
    parser.add_argument("--build", action="store_true", help="Only build the frontend")
    parser.add_argument("--run", action="store_true", help="Only start the server")
    parser.add_argument("--cloudflared", action="store_true", help="Start a Cloudflare tunnel")
    parser.add_argument("--port", type=int, default=SERVER_PORT, help=f"Server port (default: {SERVER_PORT})")
    args = parser.parse_args()

    print("=" * 60)
    print("  Tutor de Matematica — Setup")
    print("  IA Local para Concursos Publicos (LFM 2.5)")
    print("=" * 60)

    if args.run:
        start_server(args.port)
        if args.cloudflared:
            start_cloudflared(args.port)
        print("\n  [OK] Server running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n  Bye!")
        return

    if args.build:
        build_frontend()
        print("\n  [OK] Build complete! Run 'python3 setup.py --run' to start.")
        return

    # Full setup
    print("\n-- Step 1/8 -- Node.js")
    install_nodejs()

    print("\n-- Step 2/8 -- npm dependencies")
    install_npm_deps()

    print("\n-- Step 3/8 -- Build frontend")
    build_frontend()

    print("\n-- Step 4/8 -- Ollama")
    install_ollama()

    print("\n-- Step 5/8 -- Pull LFM 2.5 model")
    pull_model()

    print("\n-- Step 6/8 -- Create custom model")
    create_custom_model()

    print("\n-- Step 7/8 -- Edital context")
    ensure_pdf_content()

    print("\n-- Step 8/8 -- Start server")
    server_proc = start_server(args.port)

    if args.cloudflared:
        cf_proc = start_cloudflared(args.port)

    print("\n" + "=" * 60)
    print(f"  ALL DONE! Open http://localhost:{args.port}")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 60)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Bye!")
        server_proc.terminate()


if __name__ == "__main__":
    main()
