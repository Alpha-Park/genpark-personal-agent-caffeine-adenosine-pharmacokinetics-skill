# -*- coding: utf-8 -*-
"""
Personal Agent Caffeine Adenosine Pharmacokinetics Client
Zero-dependency two-compartment caffeine elimination pharmacokinetic modeler,
adenosine A1/A2A receptor occupancy calculator, and sleep-architecture-safe intake scheduler.
"""

import math
from typing import Dict, List, Any, Optional

class PersonalAgentCaffeineAdenosinePharmacokinetics:
    """
    Simulates circulating plasma caffeine concentrations, CYP1A2 metabolic half-life rates,
    adenosine competitive receptor binding, and nocturnal slow-wave sleep (N3) preservation.
    """

    def simulate_caffeine_clearance(
        self,
        caffeine_doses: List[Dict[str, float]],
        metabolism_rate: str = "normal",
        bedtime_hour: float = 23.0
    ) -> Dict[str, Any]:
        """
        Simulates hour-by-hour circulating caffeine clearance from oral ingestion doses:
        Doses format: [{'hour': 8.0, 'mg': 120.0}, {'hour': 13.5, 'mg': 80.0}]
        Metabolism rate half-lives: Fast (3.8h), Normal (5.7h), Slow (8.5h).
        """
        rate_str = str(metabolism_rate).lower()
        if "fast" in rate_str:
            t_half = 3.8
        elif "slow" in rate_str:
            t_half = 8.5
        else:
            t_half = 5.7 # Normal population mean

        ke = math.log(2.0) / t_half
        bed = float(bedtime_hour) % 24.0

        if not caffeine_doses:
            caffeine_doses = [{"hour": 8.0, "mg": 100.0}]

        # Calculate residual caffeine at bedtime
        bedtime_residual_mg = 0.0
        total_ingested_mg = 0.0

        for item in caffeine_doses:
            h = float(item.get("hour", 8.0))
            mg = max(0.0, min(800.0, float(item.get("mg", 100.0))))
            total_ingested_mg += mg

            # Hours between dose and bedtime (accounting for same-day schedule)
            dt = bed - h if bed >= h else (bed + 24.0) - h
            if dt >= 0.5: # 30 min for full gastrointestinal absorption
                residual = mg * math.exp(-ke * dt)
            else:
                residual = mg # immediate or very recent dose
            bedtime_residual_mg += residual

        bedtime_residual_mg = round(bedtime_residual_mg, 1)

        # Adenosine A1 / A2A receptor occupancy percentage
        # Kd binding affinity threshold is approximately ~25 mg circulating equivalent
        kd = 25.0
        receptor_occupancy_pct = round((bedtime_residual_mg / (bedtime_residual_mg + kd)) * 100.0, 1)

        # Slow-wave deep sleep (N3 / delta sleep) suppression penalty
        # Every 10% receptor blockade suppresses stage 3 deep sleep by ~3.5%
        sws_suppression_pct = round(min(40.0, (receptor_occupancy_pct / 10.0) * 3.5), 1)

        if bedtime_residual_mg <= 18.0:
            status = "OPTIMAL SLEEP PRESERVATION (Residual <= 18 mg)"
            guidance = "Negligible adenosine interference. Deep sleep architecture and glymphatic clearance intact."
        elif bedtime_residual_mg <= 40.0:
            status = "MILD DEEP SLEEP FRAGMENTATION (Residual 18 - 40 mg)"
            guidance = "Slight reduction in slow-wave sleep. Consider pulling afternoon cutoff 60 minutes earlier."
        else:
            status = "SEVERE SLOW-WAVE SUPPRESSION (Residual > 40 mg)"
            guidance = "Elevated risk of nocturnal micro-arousals and suppressed growth hormone pulse. Mandate earlier intake cutoff."

        return {
            "total_caffeine_ingested_mg": round(total_ingested_mg, 1),
            "metabolic_half_life_hours": t_half,
            "metabolism_phenotype": "Fast Metabolizer (CYP1A2 *1A)" if t_half < 4.5 else ("Slow Metabolizer (CYP1A2 *1F / Inactive)" if t_half > 7.0 else "Normal Population Mean"),
            "bedtime_circulating_residual_mg": bedtime_residual_mg,
            "adenosine_receptor_occupancy_pct": f"{receptor_occupancy_pct}%",
            "slow_wave_sleep_suppression_pct": f"-{sws_suppression_pct}% deep sleep",
            "sleep_architecture_risk": status,
            "clinical_recommendation": guidance
        }

    def calculate_optimal_ingestion_schedule(
        self,
        target_wake_time: str = "07:00",
        bedtime: str = "23:00",
        total_mg_budget: float = 200.0,
        metabolism_rate: str = "normal"
    ) -> Dict[str, Any]:
        """
        Calculates optimal ingestion delay post-wake (90-120 min) and strict afternoon cutoff
        to guarantee residual caffeine at bedtime remains below 20 mg.
        """
        def parse_h(t_str: str) -> float:
            parts = str(t_str).split(":")
            return float(parts[0]) + (float(parts[1]) / 60.0 if len(parts) > 1 else 0.0)

        def format_h(h_val: float) -> str:
            hh = int(h_val) % 24
            mm = int((h_val - int(h_val)) * 60)
            return f"{hh:02d}:{mm:02d}"

        wake_h = parse_h(target_wake_time)
        bed_h = parse_h(bedtime)
        mg_budget = max(50.0, min(500.0, float(total_mg_budget)))

        rate_str = str(metabolism_rate).lower()
        t_half = 3.8 if "fast" in rate_str else (8.5 if "slow" in rate_str else 5.7)
        ke = math.log(2.0) / t_half

        # Morning delay: 90 to 120 minutes post-wake to allow cortisol awakening response (CAR) to peak
        first_cup_h = (wake_h + 1.5) % 24.0

        # Required clearance duration from last dose to bedtime to reach <= 20 mg
        # Assuming second dose is half the daily budget: 20 = (budget / 2) * exp(-ke * dt)
        dose2_mg = mg_budget * 0.5
        required_clearance_hours = round(math.log(max(1.0, dose2_mg) / 20.0) / ke, 1)

        last_cup_h = (bed_h - required_clearance_hours) % 24.0

        return {
            "wake_time": target_wake_time,
            "bedtime": bedtime,
            "caffeine_budget_mg": mg_budget,
            "cortisol_awakening_delay_minutes": 90,
            "first_intake_window_opens": format_h(first_cup_h),
            "strict_afternoon_cutoff_time": format_h(last_cup_h),
            "required_bedtime_clearance_hours": required_clearance_hours,
            "pharmacokinetic_rationale": f"Delaying first intake 90 min allows endogenous adenosine clearance; shutting off intake at {format_h(last_cup_h)} guarantees <= 20 mg residual at bedtime."
        }
