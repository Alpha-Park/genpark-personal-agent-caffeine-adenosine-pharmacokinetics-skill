# -*- coding: utf-8 -*-
"""FastMCP Server for Personal Agent Caffeine Adenosine Pharmacokinetics Skill."""

from mcp.server.fastmcp import FastMCP
from client import PersonalAgentCaffeineAdenosinePharmacokinetics

mcp = FastMCP("PersonalAgentCaffeineAdenosinePharmacokinetics")
client = PersonalAgentCaffeineAdenosinePharmacokinetics()

@mcp.tool()
def simulate_caffeine_clearance(
    caffeine_doses: list[dict],
    metabolism_rate: str = "normal",
    bedtime_hour: float = 23.0
) -> str:
    """Simulates hour-by-hour caffeine clearance, bedtime residual, and deep sleep suppression."""
    import json
    return json.dumps(client.simulate_caffeine_clearance(caffeine_doses, metabolism_rate, bedtime_hour), indent=2)

@mcp.tool()
def calculate_optimal_ingestion_schedule(
    target_wake_time: str = "07:00",
    bedtime: str = "23:00",
    total_mg_budget: float = 200.0,
    metabolism_rate: str = "normal"
) -> str:
    """Calculates optimal morning delay (CAR) and strict afternoon cutoff for sleep preservation."""
    import json
    return json.dumps(client.calculate_optimal_ingestion_schedule(
        target_wake_time, bedtime, total_mg_budget, metabolism_rate
    ), indent=2)

if __name__ == "__main__":
    mcp.run()
