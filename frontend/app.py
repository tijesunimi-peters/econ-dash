import dash
import dash_bootstrap_components as dbc
from layouts import build_layout
from callbacks import register_callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
)
app.title = "Economic Dashboard — US & Canada"
app.layout = build_layout()
register_callbacks(app)

if __name__ == "__main__":
    from config import DASH_HOST, DASH_PORT, DASH_DEBUG
    app.run(debug=DASH_DEBUG, host=DASH_HOST, port=DASH_PORT)
