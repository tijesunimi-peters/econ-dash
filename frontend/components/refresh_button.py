"""
Data Refresh Button Component

Displays a refresh button with:
- Last refresh timestamp
- Next refresh available time (24-hour throttle)
- Loading state during refresh
- Success/error notifications
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime
from styles import COLORS


def build_refresh_button(last_refresh_time=None, next_refresh_time=None, is_loading=False, is_scheduled=False):
    """
    Build a data refresh button component.

    Args:
        last_refresh_time: ISO datetime string of last refresh
        next_refresh_time: ISO datetime string when next refresh is available
        is_loading: Boolean indicating if refresh is in progress
        is_scheduled: Boolean indicating if refresh is scheduled/queued

    Returns:
        Dash component with refresh button and status info
    """
    # Format timestamps for display
    last_refresh_text = "Never"
    next_refresh_text = "Anytime"
    status_text = ""

    if last_refresh_time:
        try:
            last_dt = datetime.fromisoformat(last_refresh_time.replace('Z', '+00:00'))
            last_refresh_text = last_dt.strftime('%Y-%m-%d %H:%M UTC')
        except:
            last_refresh_text = "Unknown"

    if next_refresh_time:
        try:
            next_dt = datetime.fromisoformat(next_refresh_time.replace('Z', '+00:00'))
            now = datetime.now(next_dt.tzinfo) if next_dt.tzinfo else datetime.now()
            time_diff = next_dt - now
            if time_diff.total_seconds() > 0:
                hours = int(time_diff.total_seconds() // 3600)
                minutes = int((time_diff.total_seconds() % 3600) // 60)
                if hours > 0:
                    next_refresh_text = f"In {hours}h {minutes}m"
                else:
                    next_refresh_text = f"In {minutes}m"
            else:
                next_refresh_text = "Available now"
        except:
            next_refresh_text = "Unknown"

    can_refresh = not next_refresh_time or next_refresh_text == "Available now"

    # Set status text based on state
    if is_loading:
        status_text = "Refresh in progress..."
    elif is_scheduled:
        status_text = "Refresh scheduled..."
    elif not can_refresh:
        status_text = f"Available {next_refresh_text}"
    else:
        status_text = "Ready to refresh"

    # Determine button state
    is_disabled = is_loading or is_scheduled or not can_refresh
    button_icon = "🔄 Refresh Data"
    if is_loading:
        button_icon = "⏳ Refreshing..."
    elif is_scheduled:
        button_icon = "⏱️ Scheduled..."

    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    button_icon,
                    id="refresh-button",
                    className="refresh-btn",
                    disabled=is_disabled,
                    style={
                        "width": "100%",
                        "backgroundColor": COLORS["primary"] if (can_refresh and not is_loading and not is_scheduled) else COLORS["text_muted"],
                        "borderColor": COLORS["primary"] if (can_refresh and not is_loading and not is_scheduled) else COLORS["border"],
                        "color": COLORS["text"],
                        "fontWeight": "600",
                        "padding": "10px 16px",
                        "borderRadius": "6px",
                        "border": f"1px solid {COLORS['border']}",
                        "cursor": "pointer" if (can_refresh and not is_loading and not is_scheduled) else "not-allowed",
                        "transition": "all 0.2s ease",
                        "opacity": "0.7" if is_disabled else "1"
                    },
                    n_clicks=0
                )
            ], width=12)
        ], style={"marginBottom": "12px"}),

        # Status indicator
        dbc.Row([
            dbc.Col([
                html.Div(
                    status_text,
                    style={
                        "fontSize": "0.85rem",
                        "color": COLORS["positive"] if can_refresh and not is_disabled else COLORS["warning"],
                        "fontWeight": "500",
                        "marginBottom": "8px",
                        "textAlign": "center"
                    }
                )
            ], width=12)
        ], style={"marginBottom": "8px"}) if status_text else html.Div(),

        # Status info
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Span("Last Refresh:", style={"fontWeight": "600", "color": COLORS["text"]}),
                        html.Span(
                            last_refresh_text,
                            style={
                                "marginLeft": "8px",
                                "color": COLORS["text_secondary"],
                                "fontSize": "0.9rem"
                            }
                        ),
                    ], style={"marginBottom": "6px", "fontSize": "0.9rem"}),

                    html.Div([
                        html.Span("Next Refresh:", style={"fontWeight": "600", "color": COLORS["text"]}),
                        html.Span(
                            next_refresh_text,
                            style={
                                "marginLeft": "8px",
                                "color": COLORS["positive"] if can_refresh else COLORS["warning"],
                                "fontSize": "0.9rem",
                                "fontWeight": "600"
                            }
                        ),
                    ], style={"fontSize": "0.9rem"}),
                ], style={
                    "padding": "8px 12px",
                    "backgroundColor": COLORS["surface"],
                    "borderRadius": "4px",
                    "border": f"1px solid {COLORS['border']}",
                    "fontSize": "0.85rem"
                })
            ], width=12)
        ]),

        # Persistent store for refresh timestamp (survives browser refresh)
        dcc.Store(
            id="refresh-timestamp-store",
            data={
                "last_refresh": last_refresh_time,
                "next_refresh": next_refresh_time,
                "is_scheduled": False
            },
            storage_type="local"  # Persist to browser localStorage
        ),

        # Toast/notification area
        html.Div(id="refresh-notification", style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "zIndex": "9999"
        }),

        # Interval to periodically check if refresh should auto-clear
        dcc.Interval(
            id="refresh-state-interval",
            interval=5000,  # Check every 5 seconds
            n_intervals=0
        ),

    ], style={
        "padding": "16px",
        "backgroundColor": COLORS["surface"],
        "borderRadius": "8px",
        "border": f"1px solid {COLORS['border']}",
        "marginBottom": "16px"
    })


def build_refresh_toast(message, status="success", visible=False):
    """
    Build a toast notification for refresh status.

    Args:
        message: Toast message text
        status: 'success', 'error', or 'info'
        visible: Boolean to show/hide toast

    Returns:
        Dash component with toast notification
    """
    color_map = {
        "success": {"bg": "#1a3a1a", "border": COLORS["positive"], "text": COLORS["positive"]},
        "error": {"bg": "#3a1a1a", "border": COLORS["negative"], "text": COLORS["negative"]},
        "info": {"bg": "#1a2a3a", "border": COLORS["primary"], "text": COLORS["primary"]}
    }

    colors = color_map.get(status, color_map["info"])

    return dbc.Toast(
        message,
        id="refresh-toast",
        header=f"Data Refresh - {status.title()}",
        is_open=visible,
        dismissable=True,
        icon="success" if status == "success" else "danger" if status == "error" else "info",
        style={
            "position": "fixed",
            "top": "20px",
            "right": "20px",
            "zIndex": "9999",
            "backgroundColor": colors["bg"],
            "borderColor": colors["border"],
            "color": colors["text"]
        }
    )
