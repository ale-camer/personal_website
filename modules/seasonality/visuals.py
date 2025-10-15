# =============================================================================
# IMPORTS
# =============================================================================
# --- Standard library ---
import os
import matplotlib.pyplot as plt

# --- Third-party ---

# --- Project ---

# =============================================================================
# VISUALIZATIONS
# =============================================================================
def plot_forecasts(
        observed: list, last_forecast: list, next_forecast: list,
        periodicity: int, save_dir: str
    ) -> None:

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    x_values = list(range(1, len(observed) + 1))
    x_last_fc = x_values[-periodicity:]
    x_next_fc = list(range(len(observed) + 1, len(observed) + 1 + periodicity))

    ax.plot(x_values, observed, label="Observed Series", color="#1f77b4", marker='o', linestyle='-')
    ax.plot(x_last_fc, last_forecast, label="Forecast (Last Period)", color="#d62728", marker='o', linestyle='--')
    ax.plot(x_next_fc, next_forecast, label="Forecast (Next Period)", color="#2ca02c", marker='o', linestyle=':')

    ax.set_title("Seasonal Forecast Visualization", fontsize=16, pad=20)
    ax.set_xlabel("Period", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    
    ax.legend(
        title="Series",
        loc='upper center', 
        bbox_to_anchor=(0.5, -0.15),
        fancybox=True, 
        shadow=True, 
        ncol=3
    )

    fig.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(os.path.join(save_dir, 'forecast_plot.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)

def plot_acf_pacf(acf_values, pacf_values, save_dir: str):

    lags = list(range(len(acf_values)))
    def plot_bar_with_annotation(ax, values, color, title):
        ax.bar(lags, values, color=color)
        filtered = [(i, v) for i, v in enumerate(values) if v < 100]
        if filtered:
            max_lag, max_val = max(filtered, key=lambda x: x[1])
            ax.axhline(max_val, color='black', linestyle='--')

            ax.annotate(
                f"Lag {max_lag}\n{max_val:.1f}%",
                xy=(max_lag, max_val),
                xytext=(max_lag, max_val + 5),
                arrowprops=dict(facecolor='black', arrowstyle="->"),
                fontsize=12,
                ha='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5)
            )
        ax.set_xlabel("Lag")
        ax.set_ylabel("Correlation (%)")
        ax.set_title(title)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    plot_bar_with_annotation(axes[0], acf_values, "#1f77b4", "ACF")
    plot_bar_with_annotation(axes[1], pacf_values, "#d62728", "PACF")
    fig.suptitle("Autocorrelation and Partial Autocorrelation", fontsize=20)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(save_dir, 'acf_pacf_plot.png'), dpi=150, bbox_inches='tight')
    plt.close(fig)