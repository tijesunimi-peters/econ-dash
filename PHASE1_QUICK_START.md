# Phase 1 Foundation — Quick Start Guide

**For:** Frontend developers implementing layout changes
**Status:** Phase 1 deliverables ready to use
**Time to Read:** 5 minutes

---

## What You Have

### New Components (Use These!)

#### 1. Responsive Grid System
```python
from components.grid_layout import dashboard_grid, sidebar_layout, responsive_grid

# 2-column grid (adapts: 4K→3col, 1440p→2col, mobile→1col)
dashboard_grid([
    policy_panel,
    sentiment_panel,
    structural_panel,
    trade_panel,
])

# Or explicit 2-column
dashboard_grid([card1, card2], layout="2-col")

# Sidebar + main (25% left, 75% right)
sidebar_layout(
    sidebar_content=context_panel,
    main_content=main_content,
    sidebar_width="25%"
)

# Card grid (auto-fill: shows as many cards as fit)
card_grid([card1, card2, card3, card4, ...])
```

#### 2. Collapsible Cards
```python
from components.collapsible_card import build_collapsible_card, build_collapsible_panel

# Single card
build_collapsible_card(
    title="Policy Timeline",
    children=policy_content,
    card_id="policy-card",  # IMPORTANT: unique ID
    default_open=False,      # starts closed
    icon="📅",
    subtitle="Recent policy decisions"
)

# Or full-width panel
build_collapsible_panel(
    title="Market Sentiment",
    children=sentiment_content,
    panel_id="sentiment-panel",
    default_open=True,
    icon="📊"
)
```

#### 3. Sidebar Layouts
```python
from components.sidebar_layout import (
    build_sidebar_layout,
    build_sidebar_context_card,
    build_sticky_header
)

# Context card for sidebar
context = build_sidebar_context_card(
    title="Manufacturing",
    metrics={
        "Latest": "$245B",
        "YoY Change": "+3.2%",
        "Trend": "↑"
    },
    related_items=["Semiconductors", "Auto Parts"],
    actions=[dbc.Button("Save View", size="sm")]
)

# Full sidebar + main layout
sidebar_layout(
    sidebar_content=context,
    main_content=main_detail_area,
)

# Sticky header (stays visible while scrolling)
build_sticky_header(
    breadcrumb=html.Div("Home > US > Manufacturing"),
    controls=dbc.Row([...])
)
```

---

## Responsive Breakpoints (Automatic!)

You don't need to do anything special. The CSS handles everything:

```
Screen Size       Grid Layout    Example Device
────────────────────────────────────────────────
3840px+ (4K)      3 columns      Ultra-wide monitor
2560px (2K)       2-3 columns    High-res monitor
1920p             2 columns      Full HD + monitor
1440p             2 columns      MacBook Pro, desktop
1080p             1-2 columns    Laptop
768-1024px        1 column       iPad, tablet
<768px            1 column       Phone
```

**No media query code needed** — CSS variables and grid templates handle it.

---

## Integration Checklist

### Step 1: Add Callback Registration (app.py)
```python
from components.collapsible_card import register_collapsible_callbacks

app = dash.Dash(__name__, external_stylesheets=[...])

# Register collapsible card callbacks
register_collapsible_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
```

### Step 2: Use in Layouts
```python
from components.grid_layout import dashboard_grid
from components.collapsible_card import build_collapsible_card

def build_layout():
    return html.Div([
        html.H1("Economic Dashboard"),

        # Responsive grid of collapsible panels
        dashboard_grid([
            build_collapsible_card(
                title="Policy Timeline",
                card_id="policy",
                children=policy_content,
                default_open=False,
                icon="📅"
            ),
            build_collapsible_card(
                title="Market Sentiment",
                card_id="sentiment",
                children=sentiment_content,
                default_open=True,
                icon="📊"
            ),
            # ... more panels
        ])
    ])
```

### Step 3: Test at Different Sizes
- Open dashboard at 3840px (4K) — should show 3 columns
- Open at 1440px — should show 2 columns
- Open at mobile (375px) — should show 1 column stacked
- Collapse/expand cards — state should persist on refresh

---

## Common Patterns

### Pattern 1: Homepage with Collapsible Panels
```python
dashboard_grid([
    build_collapsible_card("Intelligence", intelligence_content, "intel", True, "🧠"),
    build_collapsible_card("Sentiment", sentiment_content, "sentiment", True, "📊"),
    build_collapsible_card("Policy", policy_content, "policy", False, "📅"),
    build_collapsible_card("Structural", structural_content, "structural", True, "🏗️"),
    build_collapsible_card("Trade", trade_content, "trade", True, "🚢"),
])
```

### Pattern 2: Detail View with Sidebar
```python
sidebar_layout(
    sidebar_content=html.Div([
        build_sticky_header(
            breadcrumb=html.Div("US > Manufacturing"),
            controls=dbc.Row([...])
        ),
        build_sidebar_context_card(
            title="Semiconductors",
            metrics={"Value": "$45B", "Trend": "↑"},
            related_items=["Electronics", "Tech"]
        ),
    ]),
    main_content=html.Div([
        dcc.Graph(id="main-chart"),
        html.Div(id="detail-table"),
    ])
)
```

### Pattern 3: Metric Cards Grid
```python
from components.grid_layout import card_grid

card_grid([
    build_metric_card("GDP Growth", "2.4%", "↑", "positive"),
    build_metric_card("Unemployment", "4.2%", "↓", "positive"),
    build_metric_card("Inflation", "3.1%", "↑", "warning"),
    # ... more cards
])
```

---

## Styling & Colors

Use CSS variables (already defined):

```python
# In your Dash component
html.Div(
    "Your content",
    style={
        "backgroundColor": "var(--surface)",
        "borderColor": "var(--border)",
        "color": "var(--text)",
        "padding": "var(--spacing-base)",
    }
)
```

**Available CSS Variables:**
- Colors: `--bg`, `--surface`, `--surface-hover`, `--border`, `--text`, `--text-secondary`, `--primary`, `--positive`, `--negative`, `--warning`
- Spacing: `--spacing-xs` (4px) to `--spacing-2xl` (40px)
- Grid: `--grid-gap`, `--max-content-width`, `--sidebar-width`

---

## FAQs

**Q: Do I need to add media queries for responsive layouts?**
A: No! CSS media queries are in `responsive.css`. Just use `dashboard_grid()` or `responsive_grid()`.

**Q: How do I customize column count?**
A: Pass `layout` parameter: `layout="2-col"`, `"3-col"`, `"1-col"`, or `"adaptive"`.

**Q: How do collapsible card states persist?**
A: Browser localStorage. Automatically saved/restored. Works across page refreshes.

**Q: Can I use old components with new ones?**
A: Yes! Fully backwards compatible. Mix and match freely.

**Q: What if I need a different sidebar width?**
A: Use `sidebar_width="30%"` or any percentage/pixel value.

**Q: Do I need to handle mobile separately?**
A: No! Components auto-adapt. Sidebar becomes stacked on mobile automatically.

**Q: Can I animate the layout changes?**
A: Yes! CSS transitions are configured (0.3s for expand/collapse, 0.2s for other changes).

---

## Debugging Tips

### Grid Not Responding to Screen Size?
- Check browser console for CSS errors
- Verify `responsive.css` is loaded (`<link href="responsive.css">`)
- Inspect element → check `display: grid` is applied

### Collapsible Cards Not Toggling?
- Check browser console for JavaScript errors
- Verify `register_collapsible_callbacks()` is called in `app.py`
- Check `card_id` values are unique (no duplicates)

### Colors Look Wrong?
- Check CSS variables are using `var(--color-name)` syntax
- Verify `style.css` defines `:root` variables
- Check browser DevTools → Computed styles

### Layout Breaks on Mobile?
- Use browser mobile emulator (Ctrl+Shift+M)
- Check sidebar becomes stacked (no side-by-side)
- Verify buttons are 44px+ (tap-friendly)

---

## What's Next?

After Phase 1 foundation works:

1. **Phase 5 (Week 2):** Animations, performance, mobile polish
2. **Phase 3 (Week 3):** Sidebar pattern for drill-down detail views
3. **Phase 2 (Week 4):** Homepage redesign with collapsible panels
4. **Phase 4 (Week 5):** Comparison mode enhancements

Each phase builds on Phase 1 foundation.

---

## Resources

- **DESIGN_SYSTEM.md** — Complete design reference (colors, typography, spacing)
- **PHASE1_FOUNDATION_SUMMARY.md** — Detailed technical overview
- **PHASE_IMPLEMENTATION_ROADMAP.md** — Full phase breakdown and timeline

---

## Questions?

Check documentation:
- Component usage → See files in `frontend/components/`
- Design patterns → DESIGN_SYSTEM.md
- Implementation details → PHASE1_FOUNDATION_SUMMARY.md
- Next phase → PHASE_IMPLEMENTATION_ROADMAP.md

---

*Phase 1 Foundation ready for use. Build with confidence! 🚀*
