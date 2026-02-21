# Composio Pricing Data Analysis

Analysis code and tools for Composio's pricing tiers and features sourced from [composio.dev/pricing](https://composio.dev/pricing).

## 📊 Google Sheet
The structured pricing data is documented here:
[Composio Pricing Tiers & Features Analysis](https://docs.google.com/spreadsheets/d/1seSMl15D8C3038M4IWjMIX7z4I-sx3aKHbRjPg_plXA/edit)

## 🗂️ Project Structure
```
composio-pricing-analysis/
├── data/
│   └── pricing_data.json       # Raw pricing data as JSON
├── analysis/
│   └── pricing_analysis.py     # Core analysis script
├── notebooks/
│   └── pricing_exploration.ipynb  # Jupyter notebook (optional)
├── requirements.txt
└── README.md
```

## 🚀 Getting Started
```bash
pip install -r requirements.txt
python analysis/pricing_analysis.py
```

## 📋 Pricing Tiers Summary
| Tier              | Price       | Tool Calls/mo | Additional Cost       |
|-------------------|-------------|---------------|-----------------------|
| Totally Free      | $0/mo       | 20,000        | N/A                   |
| Ridiculously Cheap| $29/mo      | 200,000       | $0.299 / 1K calls     |
| Serious Business  | $229/mo     | 2,000,000     | $0.249 / 1K calls     |
| Enterprise        | Custom      | Flexible      | Volume discounts      |

## 🔍 Analysis Goals
- Compare cost-per-call across tiers
- Model break-even points between tiers
- Visualize feature matrix
- Identify optimal tier for given usage levels
