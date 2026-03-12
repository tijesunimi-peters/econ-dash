"""
Grid Layout System for Responsive Dashboard

Provides reusable components for responsive grid layouts that adapt to different
screen sizes (1080p, 1440p, 1920p, 2560p, 4K).

Responsive Breakpoints:
- 4K (3840px+): 3-column layout
- 2K (2560px): 2-3 column layout
- 1440p (1440px): 2-column layout
- 1080p (1025-1440px): 1-2 column layout
- Tablet (768-1024px): 1 column
- Mobile (<768px): 1 column (full-width stacking)
"""

from dash import html
import dash_bootstrap_components as dbc


def responsive_grid(children, columns=None, gap="16px", className=""):
    """
    Create a responsive grid container that adapts column count based on screen size.

    Args:
        children: List of grid items
        columns: Grid template columns (e.g., "1fr 1fr 1fr" for 3 columns)
                If None, uses CSS media queries for automatic responsiveness
        gap: Spacing between grid items (default "16px")
        className: Additional CSS classes

    Returns:
        Div with CSS Grid layout

    Example:
        responsive_grid([card1, card2, card3])
    """

    style = {
        "display": "grid",
        "gap": gap,
        "gridTemplateColumns": columns or "repeat(auto-fit, minmax(400px, 1fr))",
        "width": "100%",
    }

    return html.Div(
        children,
        className=f"responsive-grid {className}",
        style=style,
    )


def dashboard_grid(children, layout="2-col", gap="16px"):
    """
    Create a dashboard-specific grid with predefined layout options.

    Args:
        children: List of items to arrange
        layout: One of:
            - "1-col": Single column (full-width)
            - "2-col": Two equal columns
            - "3-col": Three equal columns
            - "1-2": Left narrow (1/3), right wide (2/3)
            - "2-1": Left wide (2/3), right narrow (1/3)
            - "adaptive": Auto-fit (default, responsive)
        gap: Spacing between items

    Returns:
        Grid container div
    """

    layout_templates = {
        "1-col": "1fr",
        "2-col": "1fr 1fr",
        "3-col": "1fr 1fr 1fr",
        "1-2": "1fr 2fr",
        "2-1": "2fr 1fr",
        "adaptive": "repeat(auto-fit, minmax(400px, 1fr))",
    }

    columns = layout_templates.get(layout, layout_templates["adaptive"])

    return responsive_grid(children, columns=columns, gap=gap, className="dashboard-grid")


def grid_item(child, className=""):
    """
    Wrap a child element to be used as a grid item.

    Args:
        child: The content to wrap
        className: Additional CSS classes

    Returns:
        Styled div suitable for grid placement
    """
    return html.Div(
        child,
        className=f"grid-item {className}",
        style={"minWidth": "0"},  # Prevents overflow of long content
    )


def sidebar_layout(sidebar_content, main_content, sidebar_width="25%", gap="16px"):
    """
    Create a sidebar + main content layout.

    Args:
        sidebar_content: Content for left sidebar (20-25% width)
        main_content: Content for main area (75-80% width)
        sidebar_width: Sidebar width (default "25%")
        gap: Spacing between sidebar and main content

    Returns:
        Two-column layout with sidebar on left

    Example:
        sidebar_layout(
            sidebar_content=html.Div("Context Panel"),
            main_content=html.Div("Main Content"),
            sidebar_width="25%"
        )
    """

    main_width = "75%" if sidebar_width == "25%" else "80%"

    style = {
        "display": "grid",
        "gridTemplateColumns": f"{sidebar_width} {main_width}",
        "gap": gap,
        "width": "100%",
        "alignItems": "start",
    }

    return html.Div(
        [
            html.Div(
                sidebar_content,
                className="sidebar-column",
                style={
                    "position": "sticky",
                    "top": "0",
                    "maxHeight": "calc(100vh - 100px)",
                    "overflowY": "auto",
                },
            ),
            html.Div(main_content, className="main-column"),
        ],
        className="sidebar-layout",
        style=style,
    )


def stacked_grid(children, max_width="1400px", gap="16px"):
    """
    Create a full-width grid that stacks vertically with max-width constraint.

    Args:
        children: List of items to stack
        max_width: Maximum container width
        gap: Vertical spacing between items

    Returns:
        Stacked grid container
    """

    return html.Div(
        children,
        className="stacked-grid",
        style={
            "display": "grid",
            "gridTemplateColumns": "1fr",
            "gap": gap,
            "maxWidth": max_width,
            "margin": "0 auto",
            "width": "100%",
        },
    )


def card_grid(cards, columns=None, gap="16px"):
    """
    Specialized grid for card-based layouts (metric cards, panels, etc.).

    Args:
        cards: List of card components
        columns: Number of columns (auto-fit if None)
        gap: Spacing between cards

    Returns:
        Grid of cards
    """

    if columns is None:
        # Auto-fit cards with minimum 200px width
        grid_columns = "repeat(auto-fill, minmax(200px, 1fr))"
    else:
        grid_columns = f"repeat({columns}, 1fr)"

    return html.Div(
        cards,
        className="card-grid",
        style={
            "display": "grid",
            "gridTemplateColumns": grid_columns,
            "gap": gap,
            "width": "100%",
        },
    )


class ResponsiveContainer:
    """
    Helper class for building responsive layouts with named regions.

    Supports CSS Grid template areas for complex layouts.
    """

    def __init__(self, gap="16px"):
        self.gap = gap
        self.areas = {}
        self.template_columns = None
        self.template_rows = None

    def set_template(self, columns, rows=None):
        """Set grid template columns and rows."""
        self.template_columns = columns
        self.template_rows = rows
        return self

    def add_area(self, name, content):
        """Add a named grid area."""
        self.areas[name] = content
        return self

    def build(self, areas_layout=None):
        """
        Build the responsive container.

        Args:
            areas_layout: Grid template areas string
                e.g., '"header header" "sidebar main"'

        Returns:
            Configured grid div
        """

        children = [
            html.Div(content, style={"gridArea": name})
            for name, content in self.areas.items()
        ]

        style = {
            "display": "grid",
            "gap": self.gap,
            "width": "100%",
        }

        if self.template_columns:
            style["gridTemplateColumns"] = self.template_columns
        if self.template_rows:
            style["gridTemplateRows"] = self.template_rows
        if areas_layout:
            style["gridTemplateAreas"] = areas_layout

        return html.Div(children, className="responsive-container", style=style)
