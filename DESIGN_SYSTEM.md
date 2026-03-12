# Design System — Econ Dashboard

**Version:** 1.0
**Date:** 2026-03-12
**Status:** Foundation Complete (Phase 1)

---

## Overview

The Econ Dashboard uses a modern, dark-themed design system optimized for economic data visualization. This document defines colors, typography, spacing, components, and responsive patterns.

---

## Color Palette

### Semantic Colors

| Name | Hex | Usage | Context |
|------|-----|-------|---------|
| **Positive** | `#00c896` | Growth, gains, up trends | Green for economic expansion |
| **Negative** | `#ff5757` | Decline, losses, down trends | Red for contractions |
| **Warning** | `#ffb347` | Alerts, caution, watch items | Orange for monitoring |
| **Neutral** | `#8b8fa3` | Neutral states, secondary info | Gray for non-urgent data |

### Backgrounds & Surfaces

| Name | Hex | Usage |
|------|-----|-------|
| **Background** | `#0f1117` | Main page background |
| **Surface** | `#1a1d29` | Cards, panels, modals |
| **Surface Hover** | `#222636` | Interactive surface on hover |
| **Border** | `#2a2d3a` | Dividers, panel edges, grid lines |

### Text

| Name | Hex | Usage |
|------|-----|-------|
| **Primary Text** | `#e8eaed` | Body text, headings |
| **Secondary Text** | `#8b8fa3` | Labels, secondary info |
| **Muted Text** | `#5a5e72` | Disabled, hints, tertiary info |

### Accent & Interactive

| Name | Hex | Usage |
|------|-----|-------|
| **Primary** | `#6c8cff` | Links, active states, primary buttons |
| **Primary Hover** | `#8da6ff` | Hover state for primary elements |

### Chart Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Chart Line** | `#6c8cff` | Time-series lines |
| **Chart Area** | `rgba(108, 140, 255, 0.1)` | Area fill under lines |
| **Chart Grid** | `#1e2130` | Grid lines |
| **Recession** | `rgba(255, 255, 255, 0.04)` | Recession/event overlays |

---

## Typography

### Font Family

**Primary Font:** `Inter`
- Sans-serif, modern, highly legible
- Used for all UI text and labels
- Fallback: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto`

### Scale

| Role | Size | Weight | Line-Height | Usage |
|------|------|--------|-------------|-------|
| **H1** | 1.5rem (24px) | 600 | 1.3 | Page title, main heading |
| **H2** | 1.25rem (20px) | 600 | 1.3 | Section heading |
| **H3** | 1.1rem (17px) | 600 | 1.3 | Subsection |
| **H4** | 1rem (16px) | 600 | 1.3 | Panel title |
| **H5** | 0.9rem (14px) | 600 | 1.3 | Card title |
| **Body** | 0.95rem (15px) | 400 | 1.5 | Standard text |
| **Body Small** | 0.85rem (13px) | 400 | 1.4 | Secondary text |
| **Label** | 0.8rem (12px) | 500 | 1.4 | Form labels, captions |
| **Small** | 0.75rem (11px) | 500 | 1.3 | Badges, footnotes |
| **Monospace** | 0.85rem (13px) | 400 | 1.4 | Data values, code |

### Font Weight

- **300**: Light (rarely used)
- **400**: Regular (body text)
- **500**: Medium (labels, secondary headings)
- **600**: Semibold (headings, emphasis)
- **700**: Bold (rare, emphasis only)

---

## Spacing & Layout

### Base Unit

**1 unit = 4px**

### Spacing Scale

| Name | Value | Usage |
|------|-------|-------|
| **xs** | 4px | Internal card spacing, tight layouts |
| **sm** | 8px | Small gaps, button padding |
| **md** | 12px | Standard internal padding |
| **base** | 16px | Default spacing, card padding, grid gaps |
| **lg** | 24px | Section spacing, panel margins |
| **xl** | 32px | Large section breaks |
| **2xl** | 40px | Very large breaks |

### Common Spacings

```python
# CSS Variables (in style.css)
--spacing-xs: 4px
--spacing-sm: 8px
--spacing-md: 12px
--spacing-base: 16px
--spacing-lg: 24px
--spacing-xl: 32px
--spacing-2xl: 40px

# Grid Gap
--grid-gap: 16px
```

### Responsive Spacing

- **Desktop (1440px+):** Full spacing (`24px` gaps)
- **Tablet (768-1024px):** Reduced spacing (`16px` gaps)
- **Mobile (<768px):** Minimal spacing (`12px` gaps)

---

## Responsive Breakpoints

### Breakpoint Definitions

| Screen | Size | Grid Cols | Usage |
|--------|------|-----------|-------|
| **4K** | 3840px+ | 3 columns | Ultra-wide displays |
| **2K** | 2560px+ | 2-3 columns | High-res monitors |
| **1920p** | 1920-2559px | 2 columns | Full HD + |
| **1440p** | 1440-1919px | 2 columns | Common laptop |
| **1080p** | 1025-1439px | 1-2 columns | Laptop, compact |
| **Tablet** | 768-1024px | 1 column | iPad, tablets |
| **Mobile** | <768px | 1 column | Phones |

### CSS Media Queries

```css
/* 4K */
@media (min-width: 2560px) { }

/* 1920p */
@media (min-width: 1920px) and (max-width: 2559px) { }

/* 1440p */
@media (min-width: 1440px) and (max-width: 1919px) { }

/* 1080p */
@media (min-width: 1025px) and (max-width: 1439px) { }

/* Tablet */
@media (min-width: 768px) and (max-width: 1024px) { }

/* Mobile */
@media (max-width: 767px) { }
```

---

## Components

### Cards

**Purpose:** Container for content with visual separation

**Properties:**
- Background: `var(--surface)`
- Border: `1px solid var(--border)`
- Border Radius: `12px`
- Padding: `16px`
- Transition: `all 0.2s`

**Hover State:**
- Border Color: `var(--text-muted)`

**Variants:**
- **Metric Card:** Shows single KPI with value, trend, alert
- **Panel Card:** Large container for related content
- **Collapsible Card:** Card with expand/collapse toggle

### Buttons

**Primary Button**
- Background: `var(--primary)`
- Color: `white`
- Padding: `8px 16px`
- Border Radius: `6px`
- Font Size: `0.9rem`
- Font Weight: `500`

**Hover:**
- Background: `var(--primary-hover)`

**Secondary Button (Outline)**
- Background: `transparent`
- Color: `var(--text-secondary)`
- Border: `1px solid var(--border)`
- Padding: `8px 16px`
- Border Radius: `6px`

**Hover:**
- Color: `var(--primary)`
- Border Color: `var(--primary)`
- Background: `rgba(108, 140, 255, 0.08)`

**Touch-Friendly (Mobile):**
- Minimum size: `44px × 44px`
- Padding: `12px 16px`

### Badges & Pills

**Default Badge**
- Background: `rgba(108, 140, 255, 0.15)`
- Color: `var(--primary)`
- Padding: `4px 8px`
- Border Radius: `4px`
- Font Size: `0.75rem`

**Semantic Badges:**
- **Positive:** Green background with `#00c896`
- **Negative:** Red background with `#ff5757`
- **Warning:** Orange background with `#ffb347`

### Inputs

**Text Input / Select**
- Background: `var(--surface)`
- Border: `1px solid var(--border)`
- Color: `var(--text)`
- Padding: `8px 12px`
- Border Radius: `6px`
- Font Size: `0.9rem`

**Focus State:**
- Border Color: `var(--primary)`
- Box Shadow: `0 0 0 3px rgba(108, 140, 255, 0.1)`

**Mobile:** Minimum height `44px`

### Dropdowns

**Select Control**
- Background: `var(--surface)`
- Border: `1px solid var(--border)`
- Border Radius: `8px`
- Minimum Width: `180px`

**Menu**
- Background: `var(--surface)`
- Border: `1px solid var(--border)`
- Border Radius: `8px`

**Option Hover:**
- Background: `var(--surface-hover)`

### Switches & Checkboxes

**Unchecked:**
- Background: `var(--border)`
- Border Color: `var(--text-muted)`

**Checked:**
- Background: `var(--primary)`
- Border Color: `var(--primary)`

---

## Patterns

### Dashboard Grid Layouts

#### 3-Column Layout (4K)
```
┌─────────────────────┬─────────────────────┬─────────────────────┐
│   Intelligence      │   Sentiment         │   Structural        │
├─────────────────────┼─────────────────────┼─────────────────────┤
│   Policy Timeline   │   Trade Flows       │   Causal Factors    │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

#### 2-Column Layout (1440p-1920p)
```
┌──────────────────────────┬──────────────────────────┐
│   Intelligence           │   Sentiment + Structural │
├──────────────────────────┼──────────────────────────┤
│   Policy Timeline        │   Trade Flows            │
└──────────────────────────┴──────────────────────────┘
```

#### 1-Column Layout (Tablet/Mobile)
```
┌──────────────────────────────────┐
│   Intelligence                   │
├──────────────────────────────────┤
│   Sentiment                      │
├──────────────────────────────────┤
│   Structural Health              │
├──────────────────────────────────┤
│   Trade Flows                    │
└──────────────────────────────────┘
```

### Sidebar + Main Content

```
┌────────────┬─────────────────────────┐
│            │                         │
│  Sidebar   │  Main Content           │
│  (25%)     │  (75%)                  │
│            │                         │
│  sticky    │  scrollable             │
│            │                         │
└────────────┴─────────────────────────┘
```

**Responsive:**
- Desktop (1025px+): Side-by-side
- Tablet/Mobile: Stacked vertically

### Collapsible Cards

**Closed State:**
```
┌─ Title ─────────────────────────────┐
│                            ▼ expand │
└─────────────────────────────────────┘
```

**Open State:**
```
┌─ Title ─────────────────────────────┐
│                            ▲ collapse│
├─────────────────────────────────────┤
│                                     │
│   Content displayed here            │
│                                     │
└─────────────────────────────────────┘
```

### Progressive Disclosure

**Level 1 (Homepage):**
- Metric value + trend arrow

**Level 2 (Sector Detail):**
- Chart + YoY% + Trend

**Level 3 (Sub-Industry):**
- Detailed chart + Causal factors + Anomalies

**Level 4 (Indicator):**
- Full analysis + Decomposition + Peer comparison

---

## Animation & Transitions

### Timing

- **Fast:** `0.15s` — Hover effects, icon changes
- **Normal:** `0.2s` — Card transitions, state changes
- **Slow:** `0.3s` — Expand/collapse, major layout shifts

### Easing

- **Default:** `ease`
- **In/Out:** `ease-in-out`
- **Spring:** `cubic-bezier(0.68, -0.55, 0.265, 1.55)`

### Common Transitions

```css
/* Hover effects */
transition: all 0.15s;

/* Expand/collapse */
transition: max-height 0.3s ease, opacity 0.3s ease;

/* Layout changes */
transition: all 0.2s;

/* Border changes */
transition: border-color 0.15s, box-shadow 0.15s;
```

---

## Accessibility

### Color Contrast

- **WCAG AA:** All text has 4.5:1 contrast ratio
- **WCAG AAA:** Headers have 7:1 contrast ratio
- **Avoid relying on color alone** for meaning (use icons/text too)

### Touch Targets

- **Minimum size:** 44px × 44px
- **Minimum spacing:** 8px between targets
- Mobile buttons should be easy to tap

### Keyboard Navigation

- **Tab:** Move focus through interactive elements
- **Shift+Tab:** Move focus backwards
- **Enter:** Activate buttons, submit forms
- **Space:** Toggle checkboxes, radio buttons
- **Arrow keys:** Navigate within lists, select options

### Screen Readers

- Use semantic HTML (`<button>`, `<a>`, `<label>`)
- Add `aria-label` to icon-only buttons
- Use `aria-expanded` for collapsible items
- Use `role` attributes for custom components

### Focus Indicators

- Always visible, typically blue outline
- 2px border or box-shadow
- Minimum 2px contrast ratio with background

---

## Implementation Files

### CSS Files
- `frontend/assets/style.css` — Base styles, colors, components
- `frontend/assets/responsive.css` — Responsive grid system, breakpoints

### Python Components
- `frontend/components/grid_layout.py` — Grid system (responsive-grid, dashboard-grid, sidebar-layout)
- `frontend/components/collapsible_card.py` — Collapsible/expandable cards
- `frontend/components/sidebar_layout.py` — Sidebar + context patterns

### Configuration
- `frontend/styles.py` — Python color constants, chart templates
- `frontend/config.py` — Layout configuration

---

## Usage Examples

### Building Responsive Layouts

```python
from components.grid_layout import dashboard_grid, responsive_grid, sidebar_layout
from components.collapsible_card import build_collapsible_card

# 3-column grid (adapts by screen size)
dashboard_grid([
    card1,
    card2,
    card3,
    card4,
], layout="adaptive")

# Sidebar + main content
sidebar_layout(
    sidebar_content=context_panel,
    main_content=main_panel,
    sidebar_width="25%"
)

# Collapsible card
build_collapsible_card(
    title="Policy Timeline",
    children=policy_content,
    card_id="policy-card",
    default_open=False,
    icon="📅"
)
```

### Using Color Semantics

```python
from styles import COLORS, trend_arrow, trend_color

# Show growth
html.Span(
    "↑ +2.3%",
    style={"color": COLORS["positive"]}
)

# Show decline
html.Span(
    "↓ -1.5%",
    style={"color": COLORS["negative"]}
)

# Show warning
html.Div(
    "Supply disruption risk",
    style={"backgroundColor": COLORS["warning"]}
)
```

### Responsive Typography

```css
/* Scales based on screen size */
h1 {
    font-size: 1.5rem;
}

@media (max-width: 768px) {
    h1 {
        font-size: 1.25rem;
    }
}
```

---

## Dark Mode Implementation

The dashboard is dark-themed by default. Colors are CSS variables and can be overridden for light mode if needed.

**CSS Variables (in `:root`):**
```css
:root {
    --bg: #0f1117;
    --surface: #1a1d29;
    --border: #2a2d3a;
    --text: #e8eaed;
    --text-secondary: #8b8fa3;
    --primary: #6c8cff;
    --positive: #00c896;
    --negative: #ff5757;
    --warning: #ffb347;
}
```

---

## Performance Considerations

### CSS Optimization

- Use CSS variables for theme colors (single source of truth)
- Minimize color transformations (avoid `rgba()` filters when possible)
- Group related selectors
- Use `will-change` sparingly for animated elements

### Grid System

- Prefer CSS Grid over flexbox for complex layouts
- Use `repeat()` function for cleaner templates
- Set `minWidth: 0` on grid items to prevent overflow

### Animation Performance

- Animate `transform` and `opacity` (GPU-accelerated)
- Avoid animating `width`, `height`, `top`, `left` when possible
- Use `reduce-motion` media query for accessibility

```css
@media (prefers-reduced-motion: reduce) {
    * {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

---

## Future Enhancements

- [ ] Light mode support with CSS variable overrides
- [ ] Custom theme builder for users
- [ ] Typography size adjustments (large text mode)
- [ ] Additional chart color schemes
- [ ] Component animation library
- [ ] Design tokens export (Figma → code)

---

## References

- **Colors Chosen For:**
  - Accessible contrast ratios (WCAG AA+)
  - Professional financial dashboard appearance
  - Semantic meaning (green=positive, red=negative)
  - Reduced eye strain (dark background)

- **Spacing Based On:**
  - 4px base unit (widely used in modern design systems)
  - 8px multiples (powers of 2 for clean math)
  - Common patterns (16px standard, 24px section breaks)

- **Breakpoints Based On:**
  - Common device screen sizes
  - Practical dashboard usage scenarios
  - Content readability at different sizes

---

*This design system evolves as the dashboard grows. Updates documented in CHANGELOG.md.*
