"""
Sunburst Chart Component for Hierarchical Sector/Sub-industry Visualization

Replaces the single-level treemap with a hierarchical sunburst chart showing:
- Inner ring: Sectors (with YoY color coding)
- Outer ring: Sub-industries within each sector (with their own YoY color coding)
- Click behavior: Sectors expand to show sub-industries, sub-industries navigate to indicators
"""

import plotly.graph_objects as go
from styles import COLORS, trend_arrow


def build_sector_sunburst(sectors_with_subitems, country_name):
    """
    Build a hierarchical sunburst chart for sector and sub-industry visualization.

    Args:
        sectors_with_subitems: List of sector dicts with structure:
            {
                "id": int,
                "name": str,
                "yoy_change_pct": float,
                "indicator_count": int,
                "sub_industries": [
                    {
                        "id": int,
                        "name": str,
                        "yoy_change_pct": float,
                        "indicator_count": int
                    },
                    ...
                ]
            }
        country_name: str, the country name for the chart title

    Returns:
        plotly.graph_objects.Figure: Sunburst chart
    """
    if not sectors_with_subitems:
        return go.Figure()

    # Transform hierarchical data into Plotly sunburst structure
    labels = [""]  # Root label (invisible)
    parents = [""]  # Root parent
    values = [0]  # Root value (will be computed from children)
    colors = [0]  # Root color
    customdata = [""]  # Root customdata
    hover_texts = [""]  # Root hover text

    all_yoy_values = []  # Collect all YoY values for color scaling

    # First pass: collect all YoY values for proper color scaling
    for sector in sectors_with_subitems:
        all_yoy_values.append(sector["yoy_change_pct"])
        if "sub_industries" in sector:
            for sub in sector["sub_industries"]:
                all_yoy_values.append(sub.get("yoy_change_pct", 0))

    min_yoy = min(all_yoy_values) if all_yoy_values else -5
    max_yoy = max(all_yoy_values) if all_yoy_values else 5
    yoy_range = max_yoy - min_yoy if max_yoy != min_yoy else 1

    # Build sector and sub-industry hierarchy
    sector_values = []  # Track sector values for root computation
    for sector in sectors_with_subitems:
        sector_id = sector["id"]
        sector_name = sector["name"]
        sector_yoy = sector["yoy_change_pct"]
        sub_count = len(sector.get("sub_industries", []))

        all_yoy_values.append(sector_yoy)

        # Add sector to hierarchy (inner ring)
        labels.append(sector_name)
        parents.append("")  # Parent is root
        values.append(sub_count if sub_count > 0 else 1)  # Use sub-industry count as value
        colors.append(sector_yoy)
        customdata.append(str(sector_id))

        # Build hover text for sector
        arrow = trend_arrow(sector_yoy)
        sector_hover = (
            f"<b>{sector_name}</b><br>"
            f"YoY: {arrow} {sector_yoy:+.1f}%<br>"
            f"<span style='font-size:11px; color:{COLORS['text_muted']}'>"
            f"Sub-industries: {sub_count}<br>Click to expand</span>"
        )
        hover_texts.append(sector_hover)

        # Add sub-industries to hierarchy (outer ring)
        sub_industries = sector.get("sub_industries", [])
        for sub in sub_industries:
            sub_id = sub["id"]
            sub_name = sub["name"]
            sub_yoy = sub.get("yoy_change_pct", 0)
            # Get indicator count from indicators array or use provided field
            indicator_count = sub.get("indicator_count", len(sub.get("indicators", [])))

            labels.append(sub_name)
            parents.append(sector_name)
            values.append(1)
            colors.append(sub_yoy)
            customdata.append(str(sub_id))

            # Build hover text for sub-industry
            arrow = trend_arrow(sub_yoy)
            sub_hover = (
                f"<b>{sub_name}</b><br>"
                f"YoY: {arrow} {sub_yoy:+.1f}%<br>"
                f"<span style='font-size:11px; color:{COLORS['text_muted']}'>"
                f"Indicators: {indicator_count}<br>Click to view</span>"
            )
            hover_texts.append(sub_hover)

        sector_values.append(sub_count if sub_count > 0 else 1)

    # Update root value to be sum of sector values
    values[0] = sum(sector_values) if sector_values else 1

    # Create sunburst figure
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colors=colors,
            colorscale=[
                [0, "#c0392b"],      # Deep red for -5%
                [0.3, "#e74c3c"],    # Light red for -2%
                [0.45, "#7f8c8d"],   # Gray for -0.5%
                [0.55, "#7f8c8d"],   # Gray for +0.5%
                [0.7, "#27ae60"],    # Green for +2%
                [1, "#00c896"],      # Bright green for +5%
            ],
            cmid=0,
            cmin=min_yoy,
            cmax=max_yoy,
            line=dict(width=2, color=COLORS["bg"]),
            showscale=False,  # Don't show colorbar for cleaner UI
        ),
        customdata=customdata,
        text=labels,  # Show labels inside the sectors
        hovertext=hover_texts,
        hovertemplate="%{hovertext}<extra></extra>",
        textfont=dict(size=13, color=COLORS["text"]),
        maxdepth=2,  # Allow 2 levels: sector + sub-industry
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>{country_name} - Sector Performance</b><br>"
                 f"<span style='font-size:12px; color:{COLORS['text_muted']}'>"
                 f"Inner ring: Sectors | Outer ring: Sub-industries | "
                 f"Color: YoY Change</span>",
            x=0.5,
            xanchor="center",
            font=dict(size=16, color=COLORS["text"]),
        ),
        margin=dict(t=120, l=0, r=0, b=0),
        height=500,
        paper_bgcolor=COLORS["surface"],
        font=dict(family="Arial, sans-serif", color=COLORS["text"]),
        clickmode="event+select",
    )

    return fig
