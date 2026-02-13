import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Standard professional styling
plt.style.use('ggplot')

def generate_visual_artifacts(df: pd.DataFrame, ticker: str, target_dir: Path):
    """Generates all analytical charts for a specific ticker and persists to the target directory."""
    ticker_df = df[df["ticker"] == ticker].copy()
    if ticker_df.empty: return

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Drift Series
    _plot_drift_series(ticker_df, ticker, target_dir)
    
    # 2. Momentum Comparison
    _plot_momentum_comparison(ticker_df, ticker, target_dir)

def _plot_drift_series(df: pd.DataFrame, ticker: str, out_dir: Path):
    df["label"] = df.apply(lambda r: f"Q{int(r['fiscal_quarter'])}\n{str(int(r['fiscal_year']))[2:]}", axis=1)
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["label"], df["drift_score"], marker='o', color="#2980b9", linewidth=2, label="Drift Score")
    plt.fill_between(df["label"], df["drift_score"], 0, where=(df["drift_score"] >= 0), color="green", alpha=0.1)
    plt.fill_between(df["label"], df["drift_score"], 0, where=(df["drift_score"] < 0), color="red", alpha=0.1)
    
    plt.axhline(0, color='black', linewidth=1)
    plt.title(f"{ticker}: Management Narrative Drift")
    plt.tight_layout()
    plt.savefig(out_dir / "drift_series.png", dpi=300)
    plt.close()

def _plot_momentum_comparison(df: pd.DataFrame, ticker: str, out_dir: Path):
    df["label"] = df.apply(lambda r: f"Q{int(r['fiscal_quarter'])} {int(r['fiscal_year'])}", axis=1)
    
    plt.figure(figsize=(10, 5))
    plt.plot(df["label"], df["financial_momentum"], marker='s', label="Financial Momentum", color="#2c3e50")
    plt.plot(df["label"], df["narrative_momentum"], marker='o', label="Narrative Momentum", color="#f39c12")
    
    plt.title(f"{ticker}: Component Momentum Trajectory")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(out_dir / "momentum_comparison.png", dpi=300)
    plt.close()
