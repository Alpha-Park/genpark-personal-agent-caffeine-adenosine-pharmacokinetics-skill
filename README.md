# Personal Agent Caffeine Adenosine Pharmacokinetics Skill

[![OpenClaw Ecosystem](https://img.shields.io/badge/OpenClaw-Ecosystem-blue.svg)](https://github.com/Alpha-Park)
[![Dual-Org Sync](https://img.shields.io/badge/GitHub-Dual--Org_Mirrored-success.svg)](https://github.com/alphaparkinc)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Standard_Library_Only-brightgreen.svg)](https://www.python.org/)
[![Model Context Protocol](https://img.shields.io/badge/Protocol-MCP_Native-orange.svg)](https://modelcontextprotocol.io/)
[![Production Grade](https://img.shields.io/badge/Status-100%25_Grade_A_Verified-success.svg)](https://github.com/Alpha-Park)

Zero-dependency two-compartment caffeine elimination pharmacokinetic modeler, adenosine A1/A2A receptor occupancy calculator, and sleep-architecture-safe intake scheduler.

## Architecture

```mermaid
flowchart TD
    Doses[Dose Amount, Hour, CYP1A2 Phenotype] --> ClearanceModel[Two-Compartment Pharmacokinetic Engine]
    ClearanceModel --> BedtimeResidual[Circulating Bedtime Residual mg]
    BedtimeResidual --> AdenosineModel[Adenosine A1/A2A Receptor Occupancy]
    AdenosineModel --> SleepPenalty[Slow-Wave Deep Sleep Suppression %]
    SleepSchedule[Wake Time & Bedtime] --> CutoffScheduler[Optimal Intake Window & Cutoff Scheduler]
```

## Quickstart

```python
from client import PersonalAgentCaffeineAdenosinePharmacokinetics

agent = PersonalAgentCaffeineAdenosinePharmacokinetics()
res = agent.simulate_caffeine_clearance([{"hour": 8.0, "mg": 150.0}, {"hour": 14.0, "mg": 100.0}])
print(f"Bedtime Residual: {res['bedtime_circulating_residual_mg']} mg | SWS Penalty: {res['slow_wave_sleep_suppression_pct']}")
```
