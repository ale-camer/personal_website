# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os

# --- Third-party ---
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Project ---

# =============================================================================
# VISUALIZATIONS
# =============================================================================
def plot_forecasts(
        observed: list, last_forecast: list, next_forecast: list, 
        periodicity: int, save_dir: str
    ) -> None:

    TITLE = "Seasonal Forecast Visualization"
    X_LABEL = "Period"
    Y_LABEL = "Value"
    LEGEND_TITLE = "Series"
    GRID_COLOR = 'rgba(200,200,200,0.25)'
    LEGEND_BG_COLOR = 'rgba(255,255,255,0.5)'

    SERIES_CONFIG = {
        "observed": {"name": "Observed Series", "color": "#1f77b4", "dash": "solid", "marker": "circle"},
        "last_fc": {"name": "Forecast (Last Period)", "color": "#d62728", "dash": "dash", "marker": "circle-open"},
        "next_fc": {"name": "Forecast (Next Period)", "color": "#2ca02c", "dash": "dot", "marker": "diamond-open"},
    }

    x_values = list(range(1, len(observed) + 1))
    x_last_fc = [x + 0.15 for x in x_values[-periodicity:]]
    x_next_fc = list(range(len(observed) + 1, len(observed) + 1 + periodicity))

    def create_trace(x, y, config):
        return go.Scatter(
            x=x, y=y, mode='lines+markers', name=config["name"],
            line=dict(color=config["color"], width=3, dash=config["dash"]),
            marker=dict(size=6, symbol=config["marker"])
        )

    fig = go.Figure()

    fig.add_trace(create_trace(x_values, observed, SERIES_CONFIG["observed"]))
    fig.add_trace(create_trace(x_last_fc, last_forecast, SERIES_CONFIG["last_fc"]))
    fig.add_trace(create_trace(x_next_fc, next_forecast, SERIES_CONFIG["next_fc"]))

    fig.update_layout(
        autosize=True,
        title=dict(text=TITLE, x=0.5, xanchor='center', font=dict(size=20, family='Arial', color='#111')),
        xaxis=dict(title=X_LABEL, showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
        yaxis=dict(title=Y_LABEL, showgrid=True, gridcolor=GRID_COLOR, zeroline=False),
        legend=dict(
            title=LEGEND_TITLE,
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5,
            bgcolor=LEGEND_BG_COLOR,
            bordercolor='rgba(0,0,0,0.1)',
            borderwidth=1
        ),
        template='plotly_white',
        margin=dict(l=50, r=30, t=70, b=70)
    )

    fig.write_image(os.path.join(save_dir, 'forecast_plot.png'), scale=2)

def plot_acf_pacf(acf_values: list, pacf_values: list, save_dir: str):

    BASE_ANNOTATION = dict(
        showarrow=True,
        arrowhead=3,
        ax=0,
        ay=-40,
        font=dict(size=16, color="black")
    )

    def max_non100(values):
        filtered = [(i, v) for i, v in enumerate(values) if v < 100]
        return max(filtered, key=lambda x: x[1]) if filtered else (None, None)

    def add_bar_with_annotation(fig, row, col, values, color):
        max_lag, max_val = max_non100(values)
        annotation_params = {
            **BASE_ANNOTATION, "x": max_lag, "y": max_val,
            "text": f"Lag {max_lag}<br>{max_val}%", "row": row, "col": col
        }

        fig.add_trace(go.Bar(x=lags, y=values, marker_color=color), row=row, col=col)
        fig.add_hline(y=max_val, line=dict(color='black', dash='dash'), row=row, col=col)
        fig.add_annotation(**annotation_params)
        fig.update_xaxes(title_text="Lag", row=row, col=col)
        fig.update_yaxes(title_text="Correlation (%)", row=row, col=col)

    lags = list(range(len(acf_values)))

    fig = make_subplots(rows=1, cols=2, subplot_titles=("ACF", "PACF"))
    add_bar_with_annotation(fig, row=1, col=1, values=acf_values, color="#1f77b4")
    add_bar_with_annotation(fig, row=1, col=2, values=pacf_values, color="#d62728")

    fig.update_layout(
        autosize=True,
        template="plotly_white",
        showlegend=False,
        title=dict(
            text="Autocorrelation and Partial Autocorrelation",
            x=0.5, xanchor='center',
            font=dict(size=20, family='Arial', color='#111')
        ),
        margin=dict(l=50, r=30, t=80, b=50)
    )

    fig.write_image(os.path.join(save_dir, 'acf_pacf_plot.png'), scale=2)