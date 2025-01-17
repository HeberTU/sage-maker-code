"""Plotting module."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from numpy.typing import ArrayLike


def partial_dependency_plot(
    data: pd.DataFrame, feature_name: str
) -> pd.DataFrame:
    """Plot the target partial dependence.

    Args:
        data: pd.DataFrame.
            Data Frame containing the data to analyze.
        feature_name: str
            feature name.

    Returns:
        pd.DataFrame
            Aggregated data.
    """
    agg_data = (
        data.groupby(by=feature_name, as_index=False)
        .agg(tx_fraud=("tx_fraud", "mean"), trx=("tx_datetime", "count"))
        .assign(tx_fraud_delta=lambda df: df.tx_fraud / data.tx_fraud.mean())
    )

    fig, ax1 = plt.subplots(figsize=(10, 4))

    # Creating a twin Axes sharing the xaxis
    ax2 = ax1.twinx()

    # Bar plot (trx) plotted first
    bar = sns.barplot(
        x=agg_data[feature_name],
        y=agg_data["trx"],
        ax=ax2,
        color="yellow",
        alpha=0.5,
        label="Transaction Count",
    )
    ax2.set_ylabel("Transaction Count")
    ax2.set_ylim(
        0, max(agg_data["trx"]) * 1.1
    )  # Adjust to ensure bars don't touch the top

    # Get bar positions
    bar_positions = bar.get_xticks()

    # Line plot (tx_fraud_delta) plotted secondly, so it's on top
    sns.lineplot(
        x=bar_positions,
        y=agg_data["tx_fraud_delta"],
        ax=ax1,
        label="E[fraud | hour] / E[fraud]",
        marker="o",
    )
    ax1.axhline(y=1, color="r", linestyle="--", label="Constant (1)")
    ax1.set_title(f"Partial dependence on {feature_name}")
    ax1.set_xlabel(feature_name)
    ax1.set_ylabel("Delta")
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5)

    # Combining legends from both ax1 and ax2
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)

    plt.tight_layout()
    plt.show()
    return agg_data


def scatter_plot(
    data: pd.DataFrame,
    feature_name: str,
    n_samples: int = 30000,
) -> None:
    """Plot a joint distribution with scatter plot in the center.

    Args:
        data: pd.DataFrame.
            Data Frame containing the data to analyze.
        feature_name: str
            feature name.
        n_samples: int = 30000
            Number of samples.
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.scatterplot(
        data=data.sample(n_samples, random_state=0),
        x=feature_name,
        y="tx_fraud",
    )
    ax.set_title(f"Partial dependence on {feature_name}")
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()


def plot_precision_recall_curve(
    precision: ArrayLike,
    recall: ArrayLike,
    pr_auc: float,
    pr_auc_random: float,
) -> None:
    """Plot the Precision-Recall Area Under the Curve.

    Args:
        precision: ArrayLike
            Precision values.
        recall: ArrayLike
            Recall values.
        pr_auc: float
            Model's Precision-Recall Area Under the Curve
        pr_auc_random: float
            Random Precision-Recall Area Under the Curve

    Returns:
        None
    """
    pr_curve, ax = plt.subplots(figsize=(8, 5))
    ax.step(recall, precision, label=f"AP-AUC Model = {round(pr_auc, 3)}")
    ax.set_title("Precision-Recall Curve Test Data", fontsize=12)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.set_xlim([-0.01, 1.01])
    ax.set_ylim([-0.01, 1.01])

    ax.set_xlabel("Recall: Detected Frauds / Total Frauds", fontsize=10)
    ax.set_ylabel(
        "Precision:  Detected Frauds / Predicted Frauds", fontsize=10
    )
    ax.plot(
        [0, 1],
        [pr_auc_random, pr_auc_random],
        "r--",
        label=f"AP-AUC Random = {round(pr_auc_random, 3)}",
    )
    ax.legend(loc="upper right")
    plt.show()


def plot_precision_recall_with_thresholds(
    precision: ArrayLike,
    recall: ArrayLike,
    thresholds: ArrayLike,
    target_precision: float = 0.8,
) -> None:
    """Plot Precision vs Recall for different thresholds.

    Args:
        precision: ArrayLike
            Precision values.
        recall: ArrayLike
            Recall values.
        thresholds: ArrayLike
            Threshold values corresponding to precision and recall values.
        target_precision: float = 0.8
            Target precision.

    Returns:
        None
    """
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot Precision and Recall curves
    ax.plot(thresholds, precision[:-1], "b--", label="Precision")
    ax.plot(thresholds, recall[:-1], "r--", label="Recall")

    # Find threshold closest to 80% precision
    close_80_precision = np.argmin(np.abs(precision - target_precision))
    threshold_80_precision = thresholds[close_80_precision]

    # Add vertical line to the plot at the threshold where precision is closest
    # to 80%
    ax.axvline(x=threshold_80_precision, color="g", linestyle="--")

    _text = (
        f"Threshold for {target_precision*100}%"
        f" Precision: {threshold_80_precision:.2f}"
    )
    # Add text near the vertical line with smaller font size
    ax.text(
        threshold_80_precision + 0.01,
        0.5,
        _text,
        rotation=0,
        verticalalignment="center",
        fontsize=8,
    )

    # Configure axis and plot properties
    ax.set_title("Precision vs Recall for different thresholds", fontsize=12)
    ax.set_xlabel("Threshold", fontsize=10)
    ax.set_ylabel("Value", fontsize=10)
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.set_xlim([min(thresholds), max(thresholds)])
    ax.set_ylim([0, 1])

    # Place the legend inside the plot in the best location
    ax.legend(loc="best")

    # Show the plot
    plt.show()


def plot_combined_precision_recall(
    precision: ArrayLike,
    recall: ArrayLike,
    thresholds: ArrayLike,
    pr_auc: float,
    pr_auc_random: float,
    target_precision: float = 0.8,
) -> None:
    """Plot Precision-Recall and Precision vs Recall for different thresholds.

    Args:
        precision: ArrayLike
            Precision values.
        recall: ArrayLike
            Recall values.
        thresholds: ArrayLike
            Threshold values corresponding to precision and recall values.
        pr_auc: float
            Model's Precision-Recall Area Under the Curve.
        pr_auc_random: float
            Random Precision-Recall Area Under the Curve.
        target_precision: float
            Target precision.

    Returns:
        None
    """
    # Set up the figure and axes
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

    # Plot Precision-Recall curve on the first axis
    ax1.step(
        recall,
        precision,
        color="#ffd966ff",
        label=f"AP-AUC Model = {round(pr_auc, 3)}",
    )
    ax1.set_title("Precision-Recall Curve Test Data", fontsize=12)
    ax1.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax1.set_xlim([-0.01, 1.01])
    ax1.set_ylim([-0.01, 1.01])
    ax1.set_xlabel("Recall: Detected Frauds / Total Frauds", fontsize=10)
    ax1.set_ylabel(
        "Precision: Detected Frauds / Predicted Frauds", fontsize=10
    )
    ax1.plot(
        [0, 1],
        [pr_auc_random, pr_auc_random],
        color="#93c47dff",
        linestyle="--",
        label=f"AP-AUC Random = {round(pr_auc_random, 3)}",
    )
    ax1.legend(loc="best")

    # Plot Precision and Recall curves on the second axis
    ax2.plot(thresholds, precision[:-1], "b--", label="Precision")
    ax2.plot(thresholds, recall[:-1], "r--", label="Recall")

    # Find threshold closest to target precision
    close_target_precision = np.argmin(np.abs(precision - target_precision))
    threshold_target_precision = thresholds[close_target_precision]

    # Add vertical line to the plot at the threshold where precision is closest
    # to target precision
    ax2.axvline(x=threshold_target_precision, color="black", linestyle="--")
    _text = (
        f"Threshold for {target_precision*100}%"
        f" Precision: {threshold_target_precision:.2f}"
    )
    ax2.text(
        threshold_target_precision + 0.01,
        0.5,
        _text,
        rotation=0,
        verticalalignment="center",
        fontsize=8,
    )

    # Configure axis properties
    ax2.set_title("Precision vs Recall for different thresholds", fontsize=12)
    ax2.set_xlabel("Threshold", fontsize=10)
    ax2.set_ylabel("Value", fontsize=10)
    ax2.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax2.set_xlim([min(thresholds), max(thresholds)])
    ax2.set_ylim([0, 1])
    ax2.legend(loc="best")

    # Display the plots
    plt.tight_layout()
    plt.show()
