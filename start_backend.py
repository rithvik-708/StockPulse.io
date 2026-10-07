import subprocess
import sys
import os

python_exe = sys.executable

SERVICES = [
    ("STORAGE", [python_exe, "-m", "storage_sink.main"]),
    ("FEATURE", [python_exe, "-m", "feature_engine.main"]),
    ("SIGNAL",  [python_exe, "-m", "signal_engine.main"]),
    ("API",     [python_exe, "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]),
]

def main():
    print("Starting StockPulse.io Backend Services...")
    processes = []
    
    # We run the services with 'services' as the working directory 
    # to maintain compatibility with existing absolute imports.
    services_dir = os.path.join(os.path.dirname(__file__), "services")
    
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        env["NVIDIA_MODEL"] = "z-ai/glm-5.3-flash"
        for name, cmd in SERVICES:
            print(f"Starting {name}...")
            # If using `uv run python start_backend.py`, this inherits the venv automatically
            p = subprocess.Popen(cmd, cwd=services_dir, env=env)
            processes.append(p)
            
        # Wait for processes
        for p in processes:
            p.wait()
            
    except KeyboardInterrupt:
        print("\nShutting down backend services...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()
