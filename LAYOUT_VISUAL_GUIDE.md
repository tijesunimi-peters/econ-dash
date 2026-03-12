# Dashboard Layout Visual Guide

**Quick Reference for Dashboard Redesign Options**

---

## Current Layout (Vertical Panels)

```
┌─────────────────────────────────────────────┐
│  Header: Country Selector & Title           │
├─────────────────────────────────────────────┤
│  [Intelligence Panel - Cycle + Summary]     │  ← Users see this
├─────────────────────────────────────────────┤
│  [Policy Timeline]                          │  ← User must scroll
├─────────────────────────────────────────────┤
│  [Market Sentiment]                         │  ← More scrolling
├─────────────────────────────────────────────┤
│  [Structural Health]                        │  ← Even more
├─────────────────────────────────────────────┤
│  [Trade Flows & Supply Chain]               │  ← Way down
├─────────────────────────────────────────────┤
│  [Anomalies Alert Panel]                    │  ← Deep scroll
├─────────────────────────────────────────────┤
│  [Treemap Visualization]                    │  ← Finally drill entry
├─────────────────────────────────────────────┤
│  [Tabs: Momentum | Compare | Correlations]  │  ← Even deeper
│  [Main Content Area]                        │
│  [Sub-industry table + charts]              │
│                                             │
│  [Bottom of page, lots of scrolling]        │
└─────────────────────────────────────────────┘

Issues:
- Must scroll past 5+ panels to drill down
- Wastes horizontal space (1080p monitor has ~45% unused)
- Sequential layout not optimized for wide screens
- Hard to customize which panels to show
```

---

## Recommended: Adaptive Dashboard Grid

### Version 1A: 2-Column Layout (1080p Standard)

```
┌──────────────────────────┬──────────────────────────┐
│  Header: Country Selector & Controls               │
├──────────────────────────┬──────────────────────────┤
│ Intelligence Panel       │ Market Sentiment Cards   │
│ [Cycle + Summary]        │ [PMI][VIX][CCI][Yield]  │
│ Click to expand          │ [Bond Spread][Inflation]│
├──────────────────────────┼──────────────────────────┤
│ Sector Treemap           │ Structural Health        │
│ [Interactive drill]      │ [Demographics] [Debt]    │
│ Click sector → drill     │ [Productivity]           │
├──────────────────────────┼──────────────────────────┤
│ Policy Timeline          │ Trade Flows              │
│ [Scrollable horizontal]  │ [Exports] [Imports]      │
│                          │ [FDI] [Supply Chain]     │
├──────────────────────────┼──────────────────────────┤
│ Collapsed: Causal        │ Collapsed: Anomalies     │
│ Factors                  │ [Expand to see alerts]   │
│ [Expand for details]     │                          │
└──────────────────────────┴──────────────────────────┘
[View Details →]  [Drill Into Sector →]

Benefits:
✓ More content visible (no scrolling to drill-down)
✓ Uses screen space efficiently
✓ Can collapse less-needed panels
✓ Modern dashboard appearance
```

### Version 1B: 3-Column Layout (2K/4K Displays)

```
┌────────────────────┬────────────────────┬────────────────────┐
│  Header: Country Selector & Controls                        │
├────────────────────┬────────────────────┬────────────────────┤
│ Intelligence Panel │ Market Sentiment   │ Structural Health  │
│ [Cycle + Summary]  │ [Cards grid]       │ [Key metrics]      │
│                    │                    │                    │
├────────────────────┼────────────────────┼────────────────────┤
│ Policy Timeline    │ Treemap            │ Trade Flows        │
│ [Horizontal]       │ [Interactive]      │ [Cards]            │
│                    │                    │                    │
├────────────────────┼────────────────────┼────────────────────┤
│ Causal Factors     │ Anomalies          │ Export Controls    │
│ [Top 3]            │ [Alerts]           │ [Save/Share]       │
│ [Expand]           │ [Expand]           │                    │
└────────────────────┴────────────────────┴────────────────────┘
[View Details →]  [Drill Into Sector →]

Perfect for:
✓ 2560×1440+ monitors (increasingly common)
✓ Trader/analyst workstations
✓ Maximizes visible information
```

---

## Drill-Down: Sidebar + Main Content Split

### Current Drill-Down (Single Column)

```
[Breadcrumb: Home > US > Manufacturing]

┌─────────────────────────────────────┐
│ Sub-Industry Table:                 │
│ Name | Latest | YoY | Trend         │
│ ├─ Semiconductors                   │
│ ├─ Auto Parts                       │
│ └─ Machinery                        │
│                                     │
│ [Chart: Time Series Data]           │
│ [Below chart: More details]         │
│                                     │
│ [Scroll for anomalies, etc]         │
└─────────────────────────────────────┘

Issues:
- Context hard to find (must scroll up)
- Narrow chart area
- Sequential information
```

### Recommended: Sidebar Split

```
[Breadcrumb: Home > US > Manufacturing]
[Controls: Date Range | YoY Toggle | Compare]

┌──────────────────────┬──────────────────────────────────┐
│ CONTEXT SIDEBAR      │ MAIN CONTENT AREA               │
│ (20-25% width)       │ (75-80% width)                  │
├──────────────────────┼──────────────────────────────────┤
│                      │ Sub-Industry Table               │
│ Metrics Summary      │ ┌──────────────────────────────┐ │
│ ┌────────────────┐   │ │ Name|Latest|YoY|Trend|Action│ │
│ │ Latest: $245B  │   │ ├──────────────────────────────┤ │
│ │ ↑ +3.2% YoY    │   │ │ Semiconductors | ... [Drill] │ │
│ │ ↑ Trend: Up    │   │ │ Auto Parts     | ... [Drill] │ │
│ │ ⚠️ Supply Risk  │   │ │ Machinery      | ... [Drill] │ │
│ └────────────────┘   │ └──────────────────────────────┘ │
│                      │                                   │
│ Related Items        │ Time-Series Chart                │
│ [Semiconductors]     │ ┌──────────────────────────────┐ │
│ [Auto]               │ │ [Manufacturing trend over    │ │
│ [Machinery]          │ │  time with recessions]       │ │
│                      │ │                              │ │
│ Causal Factors       │ │ [Interactive hover]          │ │
│ 📈 Oil prices        │ └──────────────────────────────┘ │
│ 📉 Chip shortage     │                                   │
│ ➡️ Export demand     │ Performance Metrics              │
│                      │ ┌────────────────────────────────┐
│ Quick Actions        │ │ [Gauge] [Sparklines] [Trends]  │
│ [Compare] [Share]    │ └────────────────────────────────┘
│ [Save View]          │                                   │
└──────────────────────┴──────────────────────────────────┘

Benefits:
✓ Context always visible (no scroll up needed)
✓ Larger chart area (better visibility)
✓ Modern analytics tool appearance
✓ Easier to drill (see related items in sidebar)
✓ Focused content on right
```

---

## Comparison Mode: Side-by-Side

### Current Tab-Based Comparison

```
[Tabs: Sectors | Momentum | Compare | Correlations]

Click "Compare" tab:
┌─────────────────────────────────────┐
│ Country 1: [US ▼]  vs  Country 2: [CA ▼]
├─────────────────────────────────────┤
│ US Metrics          Canada Metrics   │
│ GDP: 28.5T          GDP: 2.1T        │
│ Growth: 2.4%        Growth: 1.8%     │
│ Unemploy: 4.2%      Unemploy: 5.1%   │
│                                      │
│ [Chart: US] [Chart: Canada]          │
│ [Tables below]                       │
│ [Scroll for more]                    │
└─────────────────────────────────────┘

Issues:
- Must switch tabs to compare (loses sector context)
- Charts not side-by-side (hard to compare visually)
- Single column for comparison isn't great
```

### Recommended: Full-Width Comparison

```
[Comparison Mode] [Country 1: US ↔ Canada] [Swap] [Add 3rd]
[Synchronized Scrolling Enabled ✓]

┌──────────────────────────┬──────────────────────────┐
│ US Intelligence Panel    │ Canada Intelligence Panel│
│ [Cycle + Summary]        │ [Cycle + Summary]        │
├──────────────────────────┼──────────────────────────┤
│ GDP: $28.5T              │ GDP: $2.1T               │
│ Growth: 2.4% ↑ Better    │ Growth: 1.8% ↓ Lower    │
│ Unemploy: 4.2%           │ Unemploy: 5.1%          │
│ Inflation: 3.1%          │ Inflation: 2.8%         │
│ Trade Bal: -$73B         │ Trade Bal: -$50B        │
├──────────────────────────┼──────────────────────────┤
│ US Time Series           │ Canada Time Series       │
│ [Chart scrolls together] │ [Chart scrolls together] │
│                          │                          │
│ Feb 2024: 2.8%           │ Feb 2024: 1.5%           │
│ Mar 2024: 2.5%           │ Mar 2024: 1.8%           │
│ Apr 2024: 2.4%  ←→ Same scroll point → Apr 2024: 1.8% │
│                                                      │
├──────────────────────────┼──────────────────────────┤
│ Divergence: -0.6%        │ (US ahead on growth)    │
│ Recent: Both rising      │ Trend: Similar          │
│ Correlation: 0.87        │ (Strong co-movement)    │
└──────────────────────────┴──────────────────────────┘

Benefits:
✓ Side-by-side visual comparison (much better)
✓ Synchronized scrolling (see same time periods)
✓ Metrics comparison visible
✓ Can see divergence/convergence at a glance
✓ Professional financial dashboard look
```

---

## Card Patterns

### Metric Card (Current)

```
┌────────────────────────┐
│ Unemployment Rate       │
│                        │
│ 4.2%                   │
│ ↑ +0.3% from last month│
│                        │
│ [Sparkline]            │
│ Updated: 3/12/2026     │
└────────────────────────┘

Simple but lacks context
```

### Enhanced Metric Card (Recommended)

```
┌────────────────────────────────────────┐
│ Unemployment Rate  [?]  [Compare]     │
│                                        │
│ 4.2% ↓                                │
│ Current vs. Prior                     │
│                                        │
│ 1M:  -0.1% ↓  (improving)            │
│ YTD: -0.5% ↓                         │
│ 5Y:  +1.2% ↑                         │
│                                        │
│ [Sparkline with forecast dashes]     │
│                                        │
│ Forecast: 4.0% by Q3 2026            │
│ Confidence: High (R²=0.87)           │
│                                        │
│ Updated: 3/12/2026 · FRED            │
│ [Drill] [More Info] [Add to Watch]   │
└────────────────────────────────────────┘

Better:
✓ Immediate trend visibility (color + arrow)
✓ Multiple timeframes (1M, YTD, 5Y)
✓ Forecast shown
✓ Confidence/reliability indicated
✓ Easy action buttons
```

---

## Navigation Patterns

### Breadcrumb Only (Current)

```
[Home > US > Manufacturing > Semiconductors]

Issues:
- Text-only, easy to misread
- No context about current selection
- Must read carefully to know position
```

### Breadcrumb + Context Panel (Recommended)

```
┌──────────────────────────────────────────┐
│ 🏠 Home > US > Manufacturing              │
│                                           │
│ Current Selection: Semiconductors         │
│ 📊 Latest: $127B  ↑ 5.2% YoY             │
│ ⚠️  Alert: Supply chain disruption risk  │
│                                           │
│ Related Items: [Auto] [Machinery]         │
│ [Drill] [Compare] [Save]                 │
└──────────────────────────────────────────┘

Better:
✓ Visual + text (easier to parse)
✓ Current metrics visible immediately
✓ Alerts show without scrolling
✓ Related items for discovery
```

---

## Responsive Breakpoints

### Mobile First Approach

```
Mobile (375px):           Tablet (768px):         Desktop (1920px):
┌──────────┐              ┌────────────┬────────┐  ┌─────┬──────┬─────┐
│ Intelligence
│            │Intelligence │ Sentiment  │  Intel │ Sentiment │ Struct
│ ├ Treemap  │
│ │          │ ├ Treemap   │ Structural│  ├ TM  │ Structural│ Trade
│ │          │ │          │ Trade      │  │     │ Trade     │ Anom
│ ├ Sentiment│
│ │          │ ├ Policy    │ Anomalies  │  ├ Pol │ Policy    │
│ │          │ │          │            │  │     │ Anomalies │
│ ├ Structural
│ │          │ ├ Causal F. │            │  └─────┘          │
│ │          │ │          │            │                    │
│ └─ Policy  │ └────────────┴────────────┘  └──────────────────┘
│
│ [Collapse] [Collapsed sections]
│
└──────────┘

1 column   2 columns      3 columns (optimal for data density)
```

---

## Color + Data Patterns

### Alert Severity Levels

```
🟢 Green (Good/Growing)
├─ Unemployment down
├─ GDP growth up
└─ Trend: positive

🟡 Yellow (Neutral/Stable)
├─ No major change
├─ Within expected range
└─ Trend: stable

🔴 Red (Alert/Risk)
├─ Unemployment spike
├─ Supply chain disruption
└─ Trend: negative, acceleration

⚫ Black (Critical)
├─ Extreme anomaly
├─ Policy decision needed
└─ Trend: severe deterioration
```

### Trend Indicators

```
↑ (Up Arrow)   = Growing, improving, accelerating
↓ (Down Arrow) = Declining, worsening, decelerating
→ (Right Arrow) = Stable, flat, unchanged
? (Uncertain)   = Insufficient data, unclear direction
```

---

## Animation & Interaction Patterns

### Drill-Down Animation

```
1. User clicks "Manufacturing" treemap sector
2. Treemap fades out smoothly (300ms)
3. Sub-industry table fades in (300ms)
4. Chart title animates from treemap to new view
5. Page scrolls to show main content
6. Sidebar appears with context

Result: Natural, guided experience (not jarring)
```

### Hover States

```
Card Hover:
  ┌────────────────────────┐
  │ Metric Name            │ ← Border brightens
  │ 4.2% [More Info] [>]  │ ← Action buttons appear
  │ Context shows          │ ← Background slightly lighter
  └────────────────────────┘

Chart Hover:
  ┌────────────────────────┐
  │ [Time-series chart]    │ ← Crosshair appears
  │ 📍 Feb 2024: 4.2%      │ ← Tooltip shows value
  │                        │
  │ [Preview other metrics]│ ← Compare options appear
  └────────────────────────┘
```

---

## Screen Real Estate Usage

### Current (Vertical Layout)

```
4K Monitor (3840×2160):
┌─────────────────────────────────────────────────────────┐
│ Useful Content (1 column)      │ Wasted Space (45%)    │
│                                │                        │
│ [Full width panel]             │ Empty space            │
│                                │                        │
│ [Another full width panel]     │ Empty space            │
│                                │                        │
│ [Another panel]                │ Empty space            │
└─────────────────────────────────────────────────────────┘
Efficiency: ~55%
```

### Recommended (Multi-Column Grid)

```
4K Monitor (3840×2160):
┌──────────────────┬──────────────────┬──────────────────┐
│ Intelligence     │ Market Sentiment │ Structural       │
│ [Content]        │ [Content]        │ [Content]        │
├──────────────────┼──────────────────┼──────────────────┤
│ Policy Timeline  │ Treemap          │ Trade Flows      │
│ [Content]        │ [Content]        │ [Content]        │
├──────────────────┼──────────────────┼──────────────────┤
│ Causal Factors   │ Anomalies        │ Export Controls  │
│ [Content]        │ [Content]        │ [Content]        │
└──────────────────┴──────────────────┴──────────────────┘
Efficiency: ~95%
```

---

## Summary Decision Tree

```
Choose layout based on your users:

Are they mostly analysts/traders?
├─ YES → Use Sidebar + Main (drill-down optimized)
└─ NO  → Use Dashboard Grid (overview optimized)

Do they use wide screens (2K+)?
├─ YES → Use 3-column grid
└─ NO  → Use 2-column grid

Do they compare countries often?
├─ YES → Implement sync-scroll comparison
└─ NO  → Tab-based comparison OK

Do they need mobile access?
├─ YES → Responsive single-column
└─ NO  → Desktop-only OK

Do they like customization?
├─ YES → Add drag-to-rearrange cards
└─ NO  → Fixed grid OK
```

---

**Next Step:** Create interactive prototype in Figma/Sketch to validate with users
