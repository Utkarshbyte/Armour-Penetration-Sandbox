from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from ballistics import SHELLS, calculate_impact

app = FastAPI()
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

class ShotRequest(BaseModel):
    shell_id: str
    thickness_mm: float
    impact_angle_deg: float
    distance_m: float
    material: str = "RHA"

@app.get("/")
def serve_index():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/api/shells")
def get_shells():
    return [
        {"id": s.id, "name": s.name, "type": s.shell_type}
        for s in SHELLS.values()
    ]

@app.post("/api/simulate")
def simulate_shot(req: ShotRequest):
    return calculate_impact(
        shell_id=req.shell_id,
        thickness_mm=req.thickness_mm,
        impact_angle_deg=req.impact_angle_deg,
        distance_m=req.distance_m,
        material=req.material,
    )
