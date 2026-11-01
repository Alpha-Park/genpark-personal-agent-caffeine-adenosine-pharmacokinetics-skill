---
name: genpark-personal-agent-caffeine-adenosine-pharmacokinetics-skill
version: "1.0.0"
description: "Zero-dependency two-compartment caffeine elimination pharmacokinetic modeler, adenosine A1/A2A receptor occupancy calculator, and sleep-architecture-safe intake scheduler."
license: MIT
dependencies:
  - python>=3.10
  - mcp>=1.0.0
entrypoint: client.py
---

# Personal Agent Caffeine Adenosine Pharmacokinetics Skill

Designed for **OpenClaw**, **Hermes**, and autonomous personal AI agents to optimize stimulant timing, track individual CYP1A2 metabolic clearance half-lives, evaluate adenosine $A_1 / A_{2A}$ receptor occupancy, and protect restorative slow-wave sleep (N3).

## Agent In-Context Capabilities

- **Two-Compartment Elimination Kinetics**: Accurately simulates circulating plasma caffeine levels based on dose amount, timing, and phenotypic clearance rates (3.8h - 8.5h).
- **Adenosine Receptor Occupancy**: Models competitive binding to predict sleep onset latency and deep sleep architecture suppression.
- **Cortisol Awakening Synchronization**: Automatically schedules a 90-minute morning delay to allow natural adenosine dissipation before caffeine ingestion.

## Tools Summary

1. `simulate_caffeine_clearance`: Evaluates multiple daily doses, computing bedtime residual mg and deep sleep disruption.
2. `calculate_optimal_ingestion_schedule`: Provides personalized morning opening and afternoon cutoff timestamps.
