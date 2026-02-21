"""
Composio Pricing Analysis
Source: https://composio.dev/pricing
Google Sheet: https://docs.google.com/spreadsheets/d/1seSMl15D8C3038M4IWjMIX7z4I-sx3aKHbRjPg_plXA/edit
"""

import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "pricing_data.json"


def load_pricing_data():
    with open(DATA_FILE) as f:
        return json.load(f)


def cost_at_usage(tier: dict, tool_calls: int) -> float | str:
    """Calculate total monthly cost for a numeric tier at a given tool call volume."""
    base = tier.get("price_monthly")
    if base is None:
        return "Contact for quote"
    included = tier.get("tool_calls_included", 0)
    extra_rate = tier.get("additional_tool_call_cost_per_1k")
    if extra_rate is None or not isinstance(included, int):
        return base
    overage = max(0, tool_calls - included)
    return base + (overage / 1000) * extra_rate


def find_optimal_tier(data: dict, monthly_tool_calls: int) -> dict:
    """Return the cheapest numeric tier that covers the required tool call volume."""
    results = []
    for tier in data["tiers"]:
        cost = cost_at_usage(tier, monthly_tool_calls)
        if isinstance(cost, (int, float)):
            results.append({"tier": tier["name"], "cost": cost})
    results.sort(key=lambda x: x["cost"])
    return results[0] if results else {"tier": "Enterprise", "cost": "Contact for quote"}


def break_even_analysis(data: dict):
    """Find call volumes where moving to the next tier becomes cheaper."""
    tiers = [t for t in data["tiers"] if isinstance(t.get("price_monthly"), (int, float))]
    print("\n=== Break-Even Analysis ===")
    for i in range(len(tiers) - 1):
        a, b = tiers[i], tiers[i + 1]
        a_rate = a.get("additional_tool_call_cost_per_1k") or 0
        b_base = b["price_monthly"]
        a_base = a["price_monthly"]
        b_rate = b.get("additional_tool_call_cost_per_1k") or 0
        # a_base + (x - a_included) * a_rate/1000 = b_base + (x - b_included) * b_rate/1000
        # Solve for x (calls)
        a_inc = a.get("tool_calls_included", 0)
        b_inc = b.get("tool_calls_included", 0)
        if isinstance(a_inc, int) and isinstance(b_inc, int) and (a_rate - b_rate) != 0:
            x = ((b_base - a_base) - (b_inc * b_rate / 1000) + (a_inc * a_rate / 1000)) / ((a_rate - b_rate) / 1000)
            print(f"  {a['name']} → {b['name']}: break-even at {int(x):,} tool calls/month")
        else:
            print(f"  {a['name']} → {b['name']}: analytical break-even not applicable")


def feature_matrix(data: dict):
    """Print a feature comparison matrix."""
    features = ["support", "custom_tool_builder", "rbac", "audit_logs", "soc2", "vpc_onprem", "log_retention_days"]
    tiers = data["tiers"]
    header = f"{'Feature':<35} " + "  ".join(f"{t['name'][:18]:<18}" for t in tiers)
    print("\n=== Feature Matrix ===")
    print(header)
    print("-" * len(header))
    for feat in features:
        row = f"{feat:<35} " + "  ".join(f"{str(t.get(feat, 'N/A')):<18}" for t in tiers)
        print(row)


def cost_comparison(data: dict, call_volumes: list[int]):
    """Compare costs across tiers at different usage volumes."""
    tiers = [t for t in data["tiers"] if isinstance(t.get("price_monthly"), (int, float))]
    header = f"{'Tool Calls/mo':>15} " + "  ".join(f"{t['name'][:18]:>18}" for t in tiers)
    print("\n=== Cost Comparison by Volume ===")
    print(header)
    print("-" * len(header))
    for vol in call_volumes:
        row = f"{vol:>15,} " + "  ".join(f"${cost_at_usage(t, vol):>16.2f}" for t in tiers)
        print(row)


if __name__ == "__main__":
    data = load_pricing_data()
    print(f"Pricing Source: {data['source']}")
    print(f"Tiers: {[t['name'] for t in data['tiers']]}")

    volumes = [10_000, 50_000, 200_000, 500_000, 1_000_000, 2_000_000, 5_000_000]
    cost_comparison(data, volumes)
    break_even_analysis(data)
    feature_matrix(data)

    print("\n=== Optimal Tier Recommendations ===")
    for vol in volumes:
        rec = find_optimal_tier(data, vol)
        print(f"  {vol:>10,} calls/mo → {rec['tier']} (${rec['cost']:.2f}/mo)")
