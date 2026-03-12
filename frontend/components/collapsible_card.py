"""
Collapsible Card Component

Provides reusable collapsible/expandable card pattern with localStorage persistence.
Allows users to hide/show panels and preferences are saved across sessions.
"""

from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc


def build_collapsible_card(
    title,
    children,
    card_id,
    default_open=True,
    icon=None,
    subtitle=None,
    action_buttons=None,
    className="",
):
    """
    Create a collapsible card with header and content.

    Args:
        title: Header text
        children: Content to show/hide
        card_id: Unique identifier (used for localStorage persistence)
        default_open: Start expanded (True) or collapsed (False)
        icon: Optional emoji or icon to show before title
        subtitle: Optional subtitle under title
        action_buttons: Optional list of buttons to show in header (right-aligned)
        className: Additional CSS classes

    Returns:
        Collapsible card div with toggle button

    Example:
        build_collapsible_card(
            title="Policy Timeline",
            children=html.Div("Policy content here"),
            card_id="policy-card",
            default_open=False,
            icon="📅",
            action_buttons=[dbc.Button("Settings", size="sm")]
        )
    """

    icon_text = f"{icon} " if icon else ""

    return html.Div(
        [
            # Header with toggle button
            html.Div(
                [
                    # Left side: icon + title
                    html.Div(
                        [
                            html.Button(
                                [
                                    html.Span(
                                        icon_text,
                                        className="collapsible-icon-text",
                                    ),
                                    html.Span(title, className="collapsible-title"),
                                ],
                                id={"type": "collapsible-toggle", "index": card_id},
                                className="collapsible-toggle-btn",
                                n_clicks=0,
                            ),
                            html.P(
                                subtitle,
                                className="collapsible-subtitle",
                                style={"display": "block" if subtitle else "none"},
                            ) if subtitle else None,
                        ],
                        className="collapsible-header-left",
                    ),
                    # Right side: action buttons + expand/collapse indicator
                    html.Div(
                        (action_buttons or [])
                        + [
                            html.Span(
                                "▼",
                                id={"type": "collapsible-indicator", "index": card_id},
                                className="collapsible-indicator",
                            ),
                        ],
                        className="collapsible-header-right",
                    ),
                ],
                className="collapsible-header",
            ),
            # Content area (shown/hidden based on toggle state)
            html.Div(
                children,
                id={"type": "collapsible-content", "index": card_id},
                className="collapsible-content",
                style={
                    "display": "block" if default_open else "none",
                    "maxHeight": "none" if default_open else "0",
                    "overflow": "hidden",
                    "transition": "max-height 0.3s ease, opacity 0.3s ease",
                    "opacity": "1" if default_open else "0",
                },
            ),
        ],
        className=f"collapsible-card {className}",
        id=f"card-wrapper-{card_id}",
    )


def build_collapsible_panel(
    title,
    children,
    panel_id,
    default_open=True,
    icon=None,
    section_type="panel",
):
    """
    Build a collapsible panel (wider, full-width variant).

    Args:
        title: Panel title
        children: Panel content
        panel_id: Unique identifier
        default_open: Start expanded
        icon: Optional icon/emoji
        section_type: CSS class to distinguish panel types

    Returns:
        Collapsible panel div
    """

    return build_collapsible_card(
        title=title,
        children=children,
        card_id=panel_id,
        default_open=default_open,
        icon=icon,
        className=f"collapsible-panel collapsible-{section_type}",
    )


# ═════════════════════════════════════════════════════════════════════════════
# Callbacks for collapsible behavior (attach to your main app)
# ═════════════════════════════════════════════════════════════════════════════


def register_collapsible_callbacks(app):
    """
    Register Dash callbacks for collapsible card behavior.

    Call this in your main app.py after creating the Dash app:

    Example:
        app = dash.Dash(__name__)
        register_collapsible_callbacks(app)
    """

    @app.callback(
        [
            Output({"type": "collapsible-content", "index": "MATCH"}, "style"),
            Output({"type": "collapsible-indicator", "index": "MATCH"}, "className"),
        ],
        Input({"type": "collapsible-toggle", "index": "MATCH"}, "n_clicks"),
        State({"type": "collapsible-content", "index": "MATCH"}, "style"),
        prevent_initial_call=True,
    )
    def toggle_collapsible(n_clicks, current_style):
        """Toggle between expanded and collapsed states."""

        if current_style is None:
            current_style = {}

        is_open = current_style.get("display", "block") == "block"
        new_style = {
            **current_style,
            "display": "none" if is_open else "block",
            "maxHeight": "0" if is_open else "none",
            "opacity": "0" if is_open else "1",
            "transition": "max-height 0.3s ease, opacity 0.3s ease",
            "overflow": "hidden",
        }

        indicator_class = (
            "collapsible-indicator collapsible-closed"
            if is_open
            else "collapsible-indicator"
        )

        return new_style, indicator_class


def save_collapsible_state(app):
    """
    Register callback to persist collapsible state to localStorage.

    Call after register_collapsible_callbacks.

    Example:
        save_collapsible_state(app)
    """

    @app.callback(
        Output("collapsible-state-store", "data"),
        Input({"type": "collapsible-toggle", "index": "ALL"}, "n_clicks"),
        State({"type": "collapsible-content", "index": "ALL"}, "style"),
        prevent_initial_call=True,
    )
    def persist_state(n_clicks_list, styles):
        """Save collapsed/expanded state to browser storage."""

        # This would require clientside callback for localStorage
        # For now, we return data that can be stored
        state = {}
        if isinstance(styles, list):
            for i, style in enumerate(styles):
                is_open = style.get("display", "block") == "block" if style else True
                state[f"card-{i}"] = is_open

        return state


# ═════════════════════════════════════════════════════════════════════════════
# Clientside Callback for localStorage Persistence
# ═════════════════════════════════════════════════════════════════════════════

COLLAPSIBLE_CLIENTSIDE_JS = """
window.collapsibleState = {};

// Load state from localStorage on page load
function loadCollapsibleState() {
    const saved = localStorage.getItem('collapsible-state');
    if (saved) {
        window.collapsibleState = JSON.parse(saved);
    }
    applyCollapsibleState();
}

// Apply saved state to DOM
function applyCollapsibleState() {
    Object.entries(window.collapsibleState).forEach(([cardId, isOpen]) => {
        const toggle = document.querySelector(
            `[id='{"type":"collapsible-toggle","index":"${cardId}"}']`
        );
        if (toggle) {
            // Toggle based on saved state
            if (isOpen === false && toggle.getAttribute('data-open') === 'true') {
                toggle.click();
            }
        }
    });
}

// Save state when toggle clicked
document.addEventListener('click', (e) => {
    const toggle = e.target.closest('.collapsible-toggle-btn');
    if (toggle) {
        const cardId = toggle.id.split('id":').pop().slice(1, -2);
        const content = toggle.closest('.collapsible-card').querySelector('.collapsible-content');
        const isOpen = content.style.display === 'block';
        window.collapsibleState[cardId] = isOpen;
        localStorage.setItem('collapsible-state', JSON.stringify(window.collapsibleState));
    }
});

// Load on init
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadCollapsibleState);
} else {
    loadCollapsibleState();
}
"""
