"""
Central repository for tooltip/popover content across the dashboard.
Organized by section with title, content (HTML), action_items, and examples.
"""

TOOLTIPS = {
    # ── Metrics Section ──
    "metrics": {
        "yoy_change": {
            "title": "Year-over-Year Change",
            "content": """
                <p><strong>YoY Change</strong> compares the current value to 12 months ago.</p>
                <p><strong>Example:</strong> If Jan 2024 = 100 and Jan 2025 = 105, YoY = +5%</p>
                <p><strong>Why it matters:</strong> Shows annualized growth, removing seasonal variations.</p>
            """,
            "action_items": "Compare sectors: positive YoY = expansion, negative = contraction.",
        },
        "percentile": {
            "title": "Percentile Score",
            "content": """
                <p><strong>Percentile</strong> shows position in the 3-year historical range.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong>0-20%ile:</strong> Historically low (concerning)</li>
                    <li><strong>40-60%ile:</strong> Average (normal)</li>
                    <li><strong>80-100%ile:</strong> Historically high (note inflation risk)</li>
                </ul>
                <p><strong>Example:</strong> 85%ile unemployment = rarely-high unemployment rate.</p>
            """,
            "action_items": "Watch extreme readings (0-5% or 95-100%): may signal turning points.",
        },
        "sparkline": {
            "title": "12-Month Trend",
            "content": """
                <p><strong>Sparkline</strong> is a compact chart of the last 12 months of data.</p>
                <p><strong>What to look for:</strong></p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li>Upward slope = acceleration</li>
                    <li>Downward slope = deceleration</li>
                    <li>Flat = stability or consolidation</li>
                </ul>
            """,
            "action_items": "Sparklines confirm YoY direction: match color (green=positive, red=negative).",
        },
    },
    # ── Business Cycle Section ──
    "business_cycle": {
        "phase": {
            "title": "Economic Phase",
            "content": """
                <p><strong>Current Phase:</strong> The sector's position in the economic cycle.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong style="color: #00c896;">🟢 Expansion:</strong> Growth accelerating</li>
                    <li><strong style="color: #ffb347;">🟡 Peak:</strong> Growth slowing, cycle turning</li>
                    <li><strong style="color: #ff5757;">🔴 Contraction:</strong> Shrinking</li>
                    <li><strong style="color: #6c8cff;">🔵 Trough:</strong> Bottom; recovery beginning</li>
                </ul>
            """,
            "action_items": "Phases rotate roughly every 3-5 years. Track duration for cycle maturity.",
        },
        "x_position": {
            "title": "Trend Position (X-Axis)",
            "content": """
                <p><strong>X-Position:</strong> Distance from the 12-month moving average (trend).</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong>Left (0):</strong> Below trend — defensive posture</li>
                    <li><strong>Center (0.5):</strong> At trend — neutral</li>
                    <li><strong>Right (1.0):</strong> Above trend — extended from mean</li>
                </ul>
                <p><strong>Implication:</strong> Values far from trend may revert (mean reversion).</p>
            """,
            "action_items": "Extremes (far left/right) suggest reversal risk; center = stable.",
        },
        "y_position": {
            "title": "Momentum Direction (Y-Axis)",
            "content": """
                <p><strong>Y-Position:</strong> Is growth accelerating or decelerating?</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong>Bottom (0):</strong> Decelerating (rate of change weakening)</li>
                    <li><strong>Center (0.5):</strong> Steady momentum</li>
                    <li><strong>Top (1.0):</strong> Accelerating (pace increasing)</li>
                </ul>
                <p><strong>Signal:</strong> Acceleration = bullish; deceleration = caution.</p>
            """,
            "action_items": "Watch deceleration near peaks: often precedes recessions.",
        },
        "sector_recommendations": {
            "title": "Favored Sectors",
            "content": """
                <p><strong>Based on phase:</strong> Sectors historically strong during this cycle stage.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong style="color: #00c896;">Expansion:</strong> Growth, Tech, Discretionary</li>
                    <li><strong style="color: #ffb347;">Peak:</strong> Financials, Staples, Defensive</li>
                    <li><strong style="color: #ff5757;">Contraction:</strong> Utilities, Healthcare, Staples</li>
                    <li><strong style="color: #6c8cff;">Trough:</strong> Cyclicals, Tech, Growth</li>
                </ul>
                <p><strong>Caveat:</strong> Recommendations are historical patterns, not guarantees.</p>
            """,
            "action_items": "Use sector recommendations to guide capital allocation within the economy.",
        },
    },
    # ── Causal Factors Section ──
    "causal_factors": {
        "correlation": {
            "title": "Correlation Strength",
            "content": """
                <p><strong>Correlation (r):</strong> Strength of relationship between proxy and sector.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong>r = 1.0:</strong> Perfect positive — move together exactly</li>
                    <li><strong>r = 0.5–0.9:</strong> Strong — reliable leading indicator</li>
                    <li><strong>r = 0.3–0.5:</strong> Moderate — useful but with noise</li>
                    <li><strong>r < 0.3:</strong> Weak — unreliable for prediction</li>
                    <li><strong>r < 0:</strong> Inverse — opposites (e.g., oil ↑ = airline margins ↓)</li>
                </ul>
            """,
            "action_items": "Focus on factors with r > 0.5 for reliable forecasting.",
        },
        "proxy_status": {
            "title": "Proxy Status",
            "content": """
                <p><strong>Proxy Status:</strong> Current trend of the external factor.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong style="color: #00c896;">📈 Rising:</strong> Factor strengthening</li>
                    <li><strong style="color: #ff5757;">📉 Falling:</strong> Factor weakening</li>
                    <li><strong>➡️ Stable:</strong> No change detected</li>
                </ul>
                <p><strong>Interpretation:</strong> If proxy rising + strong correlation = sector tailwind.</p>
            """,
            "action_items": "Combine with correlation: rising factor + strong r = bullish signal.",
        },
        "confidence": {
            "title": "Confidence Level",
            "content": """
                <p><strong>Confidence:</strong> Reliability of this factor based on recent correlation.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong style="color: #00c896;">🟢 High (70%+):</strong> Recently reliable</li>
                    <li><strong style="color: #ffb347;">🟡 Medium (50-70%):</strong> Use with caution</li>
                    <li><strong style="color: #ff5757;">🔴 Low (&lt;50%):</strong> Unreliable; ignore</li>
                </ul>
                <p><strong>Why it changes:</strong> Relationship strength varies over time; recalibrate quarterly.</p>
            """,
            "action_items": "Prioritize high-confidence factors; low-confidence factors are noise.",
        },
    },
    # ── Momentum Section ──
    "momentum": {
        "momentum_scale": {
            "title": "Momentum Scale (0–100)",
            "content": """
                <p><strong>Momentum Score:</strong> Rate of change ranking (0 = weakest, 100 = strongest).</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong>0–20:</strong> Decelerating (weakening)</li>
                    <li><strong>40–60:</strong> Steady (neutral)</li>
                    <li><strong>80–100:</strong> Accelerating (strengthening)</li>
                </ul>
                <p><strong>Positive/Negative:</strong> Sign indicates direction (+ = growing, − = shrinking).</p>
            """,
            "action_items": "High momentum + positive direction = strong growth; monitor for deceleration peaks.",
        },
        "rate_of_change": {
            "title": "Rate of Change (1M, 3M, 6M)",
            "content": """
                <p><strong>Rate of Change (RoC):</strong> Percentage change over the period.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong>1M RoC:</strong> Immediate, volatile momentum</li>
                    <li><strong>3M RoC:</strong> Near-term trend (more reliable)</li>
                    <li><strong>6M RoC:</strong> Medium-term momentum (trend confirmation)</li>
                </ul>
                <p><strong>Divergence check:</strong> If 1M diverges from 6M, trend may be reversing.</p>
            """,
            "action_items": "Use 3M/6M for signals; 1M for confirmation. Falling RoC = caution.",
        },
        "acceleration": {
            "title": "Acceleration Direction",
            "content": """
                <p><strong>Acceleration:</strong> Is the rate of change itself accelerating or decelerating?</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong style="color: #00c896;">▲ Accelerating:</strong> Rate of growth increasing (bullish)</li>
                    <li><strong style="color: #ff5757;">▼ Decelerating:</strong> Rate of growth decreasing (caution)</li>
                    <li><strong>= Stable:</strong> Consistent rate (neutral)</li>
                </ul>
                <p><strong>Key insight:</strong> Deceleration often precedes reversals; watch it closely.</p>
            """,
            "action_items": "Deceleration + extended valuation = exit signal. Acceleration = add positions.",
        },
    },
    # ── Anomalies Section ──
    "anomalies": {
        "z_score": {
            "title": "Z-Score (Statistical Deviation)",
            "content": """
                <p><strong>Z-Score:</strong> Standard deviations from the 3-year rolling mean.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong>|Z| < 1.0:</strong> Normal range (expected variation)</li>
                    <li><strong>1.0 < |Z| < 1.5:</strong> Unusual (monitor)</li>
                    <li><strong>1.5 < |Z| < 2.5:</strong> Warning (likely inflection)</li>
                    <li><strong>|Z| > 2.5:</strong> Critical (urgent; investigate cause)</li>
                </ul>
                <p><strong>Positive/Negative:</strong> Sign indicates above/below mean.</p>
            """,
            "action_items": "Research cause: Is it cycle change, policy, or external shock?",
        },
        "severity": {
            "title": "Severity Level",
            "content": """
                <p><strong>Severity:</strong> Urgency classification based on Z-score magnitude.</p>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    <li><strong style="color: #ffb347;">⚠️ Warning:</strong> |Z| 1.5–2.5 (monitor trend)</li>
                    <li><strong style="color: #ff5757;">🚨 Critical:</strong> |Z| > 2.5 (act immediately)</li>
                </ul>
                <p><strong>Action:</strong> Critical = likely inflection point; investigate underlying drivers.</p>
            """,
            "action_items": "Critical alerts demand investigation: cycle turn, policy change, or structural shift?",
        },
    },
}


def get_tooltip(section, key):
    """
    Retrieve tooltip content by section and key.

    Args:
        section (str): Top-level section (e.g., 'metrics', 'business_cycle')
        key (str): Specific tooltip key (e.g., 'yoy_change')

    Returns:
        dict: Tooltip data with 'title', 'content', 'action_items' keys.
              Returns empty dict if not found.
    """
    return TOOLTIPS.get(section, {}).get(key, {})


def tooltip_exists(section, key):
    """Check if a tooltip exists."""
    return bool(get_tooltip(section, key))
