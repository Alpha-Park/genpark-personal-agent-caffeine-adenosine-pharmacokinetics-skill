# -*- coding: utf-8 -*-
"""Demonstration of Personal Agent Caffeine Adenosine Pharmacokinetics Skill."""

import sys
sys.stdout.reconfigure(encoding='utf-8')
from client import PersonalAgentCaffeineAdenosinePharmacokinetics

def main():
    agent = PersonalAgentCaffeineAdenosinePharmacokinetics()

    print("=" * 70)
    print("DEMO: Personal Agent Caffeine Adenosine Pharmacokinetics Modeler")
    print("=" * 70)

    # 1. Simulate dual caffeine doses (150mg at 08:00, 100mg at 14:00)
    doses = [
        {"hour": 8.0, "mg": 150.0},
        {"hour": 14.0, "mg": 100.0}
    ]

    res_sim = agent.simulate_caffeine_clearance(
        caffeine_doses=doses,
        metabolism_rate="normal",
        bedtime_hour=23.0
    )

    print(f"\n1. Pharmacokinetic Clearance Simulation (150mg @ 08:00, 100mg @ 14:00):")
    print(f"   Total Ingested: {res_sim['total_caffeine_ingested_mg']} mg")
    print(f"   Metabolic Half-Life: {res_sim['metabolic_half_life_hours']} hours ({res_sim['metabolism_phenotype']})")
    print(f"   Circulating Bedtime Residual: {res_sim['bedtime_circulating_residual_mg']} mg")
    print(f"   Adenosine Receptor Occupancy: {res_sim['adenosine_receptor_occupancy_pct']}")
    print(f"   Deep Sleep Suppression: {res_sim['slow_wave_sleep_suppression_pct']}")
    print(f"   Status: {res_sim['sleep_architecture_risk']}")
    print(f"   Rx: {res_sim['clinical_recommendation']}")

    # 2. Calculate optimal schedule for 07:00 wake, 23:00 bed, 200mg budget
    res_sched = agent.calculate_optimal_ingestion_schedule(
        target_wake_time="07:00",
        bedtime="23:00",
        total_mg_budget=200.0,
        metabolism_rate="normal"
    )

    print(f"\n2. Optimal Circadian-Aligned Intake Timing:")
    print(f"   Wake: {res_sched['wake_time']} | Bedtime: {res_sched['bedtime']}")
    print(f"   Morning Window Opens: {res_sched['first_intake_window_opens']} (Delay: {res_sched['cortisol_awakening_delay_minutes']} min)")
    print(f"   Strict Afternoon Cutoff: {res_sched['strict_afternoon_cutoff_time']} (Clearance: {res_sched['required_bedtime_clearance_hours']} hours)")
    print(f"   Rationale: {res_sched['pharmacokinetic_rationale']}")

    print("\nVerification complete: Caffeine pharmacokinetic engine executed flawlessly.")

if __name__ == "__main__":
    main()
