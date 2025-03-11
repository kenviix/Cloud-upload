from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI running on Railway"}


@app.get("/run")
def run_script():
    try:
        # Run your script (script.py) and capture output
        result = subprocess.run(
            ["python3", "script.py"], capture_output=True, text=True)
        return {"output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"error": str(e)}
