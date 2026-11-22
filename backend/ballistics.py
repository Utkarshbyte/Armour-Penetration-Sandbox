import math
from dataclasses import dataclass

@dataclass
class Shell:
    id: str
    name: str
    shell_type: str       # "APCBC", "APFSDS", "HEAT"
    caliber_mm: float
    velocity_ms: float
    base_pen_mm: float    # Penetration at 0m, 0°
    ricochet_deg: float   # Guaranteed ricochet angle
    drag_factor: float    # Velocity/pen drop-off per 1000m (0 for HEAT)
    spall_multiplier: float

SHELLS = {
    "apcbc_88": Shell("apcbc_88", "88mm PzGr 39 (APCBC)", "APCBC", 88, 1000, 237, 71.0, 0.16, 1.2),
    "apfsds_120": Shell("apfsds_120", "120mm DM53 (APFSDS)", "APFSDS", 120, 1750, 652, 81.0, 0.05, 1.0),
    "heat_105": Shell("heat_105", "105mm M456 (HEAT-FS)", "HEAT", 105, 1173, 400, 78.0, 0.0, 0.65),
}

MATERIAL_MODIFIERS = {
    "RHA": 1.0,        # Rolled Homogeneous Armor
    "CAST": 0.94,      # Cast Homogeneous Armor
    "COMPOSITE": 1.35, # Simplified composite multiplier
}

def calculate_impact(
    shell_id: str,
    thickness_mm: float,
    impact_angle_deg: float,
    distance_m: float,
    material: str = "RHA",
) -> dict:
    shell = SHELLS[shell_id]
    mat_mod = MATERIAL_MODIFIERS.get(material, 1.0)

    # Clamp angle to avoid division by zero at 90°
    angle_clamped = min(max(impact_angle_deg, 0.0), 89.5)
    cos_theta = math.cos(math.radians(angle_clamped))

    # Effective line-of-sight thickness
    effective_thickness = (thickness_mm / cos_theta) * mat_mod

    # Distance penetration drop-off (chemical HEAT rounds don't lose pen over distance)
    drop_multiplier = max(0.3, 1.0 - (distance_m / 1000.0) * shell.drag_factor)
    pen_at_distance = shell.base_pen_mm * drop_multiplier

    # Determine outcome
    if angle_clamped >= shell.ricochet_deg:
        verdict = "RICOCHET"
        residual_pen = 0.0
        spall_count = 0
        spall_cone_deg = 0.0
    elif pen_at_distance >= effective_thickness:
        verdict = "PENETRATION"
        residual_pen = pen_at_distance - effective_thickness
        # More overmatch/residual pen = denser spall cone
        spall_count = int(min(55, max(18, (25 + residual_pen * 0.08) * shell.spall_multiplier)))
        spall_cone_deg = 16.0 if shell.shell_type == "HEAT" else 28.0
    else:
        verdict = "NON_PENETRATION"
        residual_pen = 0.0
        spall_count = 0
        spall_cone_deg = 0.0

    return {
        "shell_name": shell.name,
        "shell_type": shell.shell_type,
        "verdict": verdict,
        "impact_angle_deg": round(angle_clamped, 1),
        "effective_thickness_mm": round(effective_thickness, 1),
        "penetration_mm": round(pen_at_distance, 1),
        "residual_pen_mm": round(residual_pen, 1),
        "spall_count": spall_count,
        "spall_cone_deg": spall_cone_deg,
    }
