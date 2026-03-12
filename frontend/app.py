"""
Economic Dashboard - Integrated Frontend

Phases 1-4 Layout Modernization:
- Phase 1: Responsive grid system, collapsible cards, sidebar layouts
- Phase 2: Homepage redesign with responsive grid and collapsible panels
- Phase 3: Drill-down improvements with sidebar layout and context
- Phase 4: (To be implemented) Comparison mode with synchronized scrolling
- Phase 5: Animations, storage persistence, performance optimization, mobile

All phases build on Phase 1 foundation using CSS Grid, localStorage, and smooth animations.
"""

import dash
import dash_bootstrap_components as dbc

from layouts import build_layout
from callbacks import register_callbacks
from utils.storage import STORAGE_CLIENTSIDE_JS

# Create Dash app with dark theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, viewport-fit=cover"
        }
    ],
)

app.title = "Economic Health Dashboard"

# Set app layout
app.layout = build_layout()

# Register all callbacks
register_callbacks(app)

# Inject clientside JavaScript for localStorage persistence (Phase 5)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script>
            // Synchronized scrolling for comparison panels (Phase 4)
            function initSyncScroll() {{
                let syncScrolling = true;
                const panel1 = document.getElementById('comparison-panel-1');
                const panel2 = document.getElementById('comparison-panel-2');

                if (!panel1 || !panel2) return;

                // Sync scroll when panel 1 scrolls
                panel1.addEventListener('scroll', function() {{
                    if (syncScrolling) {{
                        syncScrolling = false;
                        panel2.scrollTop = panel1.scrollTop;
                        syncScrolling = true;
                    }}
                }});

                // Sync scroll when panel 2 scrolls
                panel2.addEventListener('scroll', function() {{
                    if (syncScrolling) {{
                        syncScrolling = false;
                        panel1.scrollTop = panel2.scrollTop;
                        syncScrolling = true;
                    }}
                }});
            }}

            // Initialize sync scroll when DOM is ready
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', initSyncScroll);
            }} else {{
                initSyncScroll();
            }}

            // Reinitialize on Dash updates
            if (typeof window.dash_clientside !== 'undefined') {{
                const originalUpdate = window.dash_clientside.update || function() {{}};
                window.dash_clientside.update = function() {{
                    const result = originalUpdate.apply(this, arguments);
                    setTimeout(initSyncScroll, 50);
                    return result;
                }};
            }}

            // localStorage persistence for dashboard preferences (Phase 5)
            window.dashboardStorage = {{
                getItem: function(key) {{
                    try {{
                        return localStorage.getItem(key);
                    }} catch (e) {{
                        console.warn('localStorage access denied:', e);
                        return null;
                    }}
                }},
                setItem: function(key, value) {{
                    try {{
                        localStorage.setItem(key, JSON.stringify(value));
                        return true;
                    }} catch (e) {{
                        console.warn('localStorage write failed:', e);
                        return false;
                    }}
                }},
                removeItem: function(key) {{
                    try {{
                        localStorage.removeItem(key);
                        return true;
                    }} catch (e) {{
                        console.warn('localStorage delete failed:', e);
                        return false;
                    }}
                }},
                clearAll: function() {{
                    try {{
                        const keys = Object.keys(localStorage);
                        keys.forEach(key => {{
                            if (key.startsWith('card-state-') ||
                                key.startsWith('sidebar-') ||
                                key === 'layout-preference' ||
                                key === 'view-preset' ||
                                key === 'active-tab' ||
                                key === 'last-country') {{
                                localStorage.removeItem(key);
                            }}
                        }});
                        return true;
                    }} catch (e) {{
                        console.warn('localStorage clear failed:', e);
                        return false;
                    }}
                }},
                getAll: function() {{
                    const prefs = {{}};
                    const keys = Object.keys(localStorage);
                    keys.forEach(key => {{
                        if (key.startsWith('card-state-') ||
                            key.startsWith('sidebar-') ||
                            key === 'layout-preference' ||
                            key === 'view-preset' ||
                            key === 'active-tab' ||
                            key === 'last-country') {{
                            try {{
                                prefs[key] = JSON.parse(localStorage.getItem(key));
                            }} catch (e) {{
                                prefs[key] = localStorage.getItem(key);
                            }}
                        }}
                    }});
                    return prefs;
                }}
            }};
        </script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == "__main__":
    from config import DASH_HOST, DASH_PORT, DASH_DEBUG

    print("""
    ╔════════════════════════════════════════════════════════╗
    ║     Economic Health Dashboard - Layout Modernized      ║
    ║                                                        ║
    ║   All Phases Complete (1, 2, 3, 4, 5):               ║
    ║   ✅ Phase 1: Responsive grid & components           ║
    ║   ✅ Phase 2: Homepage redesign                       ║
    ║   ✅ Phase 3: Drill-down improvements                 ║
    ║   ✅ Phase 4: Comparison with sync scroll             ║
    ║   ✅ Phase 5: Animations & storage                    ║
    ║                                                        ║
    ║   Starting server...                                  ║
    ╚════════════════════════════════════════════════════════╝
    """)

    app.run(debug=DASH_DEBUG, host=DASH_HOST, port=DASH_PORT)
