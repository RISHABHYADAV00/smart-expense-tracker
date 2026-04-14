# ============================================================
# Smart Expense Analyzer
# Author: RISHABH 
# Description: A Streamlit web app to analyze personal expenses
#              from a CSV file using Pandas and Matplotlib.
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

# ── Page Configuration ────────────────────────────────────────
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for a cleaner look ────────────────────────────
st.markdown("""
    <style>
        /* Main title styling */
        .main-title {
            font-size: 2.4rem;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 0.2rem;
        }
        .sub-title {
            font-size: 1rem;
            color: #6b7280;
            margin-bottom: 1.5rem;
        }
        /* Metric card styling */
        div[data-testid="metric-container"] {
            background-color: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 16px 20px;
        }
        /* Insight box */
        .insight-box {
            background-color: #eff6ff;
            border-left: 5px solid #3b82f6;
            border-radius: 6px;
            padding: 14px 18px;
            margin-bottom: 12px;
            color: #1e3a5f;
            font-size: 0.95rem;
        }
        /* Warning box */
        .warning-box {
            background-color: #fff7ed;
            border-left: 5px solid #f97316;
            border-radius: 6px;
            padding: 14px 18px;
            margin-bottom: 12px;
            color: #7c2d12;
            font-size: 0.95rem;
        }
        /* Section header */
        .section-header {
            font-size: 1.2rem;
            font-weight: 600;
            color: #111827;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 6px;
            margin-bottom: 16px;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# ── Helper: Category Suggestions ─────────────────────────────
SUGGESTIONS = {
    "food":          "🍽️  Try meal prepping at home and reduce food delivery orders to save significantly.",
    "shopping":      "🛍️  Avoid impulse purchases. Use a 24-hour rule — wait before buying non-essentials.",
    "travel":        "✈️  Book tickets in advance and prefer economy options to optimize travel costs.",
    "entertainment": "🎬  Review subscription services. Cancel unused ones and use free alternatives.",
    "transport":     "🚌  Use public transport or carpool when possible to cut daily commute costs.",
    "health":        "💊  Prefer generic medicines and schedule preventive checkups to avoid bigger bills.",
    "education":     "📚  Look for free online resources (Coursera audits, YouTube) before paid courses.",
    "bills":         "📋  Automate bill payments to avoid late fees and review plans for better deals.",
    "rent":          "🏠  Consider sharing accommodation or negotiating lease terms to reduce rent.",
    "others":        "💡  Track these miscellaneous expenses closely — they tend to add up quickly.",
}

def get_suggestion(category: str) -> str:
    """Return a spending suggestion for the given category (case-insensitive)."""
    return SUGGESTIONS.get(category.lower(), "💡  Keep tracking this category to identify saving opportunities.")


# ── Helper: Validate Uploaded DataFrame ──────────────────────
REQUIRED_COLUMNS = {"date", "category", "amount"}

def validate_dataframe(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Check that the uploaded CSV has the required columns.
    Returns (is_valid: bool, error_message: str).
    """
    uploaded_cols = set(df.columns.str.strip().str.lower())
    missing = REQUIRED_COLUMNS - uploaded_cols
    if missing:
        return False, f"Missing column(s): **{', '.join(missing)}**. Please check your CSV."
    return True, ""


# ── Helper: Clean & Prepare Data ─────────────────────────────
def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names, parse dates, and clean Amount column.
    Returns a cleaned DataFrame.
    """
    # Normalize column names → lowercase + strip whitespace
    df.columns = df.columns.str.strip().str.lower()

    # Parse Date column (handle multiple common formats)
    df["date"] = pd.to_datetime(df["date"], dayfirst=False, errors="coerce")

    # Remove currency symbols / commas from Amount; convert to float
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace(r"[₹$,]", "", regex=True)
        .str.strip()
    )
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Capitalize Category for display
    df["category"] = df["category"].astype(str).str.strip().str.title()

    # Drop rows where Amount or Date is invalid
    df.dropna(subset=["amount", "date"], inplace=True)
    df = df[df["amount"] > 0]

    return df.reset_index(drop=True)


# ── Helper: Pie Chart ─────────────────────────────────────────
def plot_pie_chart(category_totals: pd.Series) -> plt.Figure:
    """Generate a styled pie/donut chart for category-wise distribution."""
    colors = [
        "#3b82f6", "#10b981", "#f59e0b", "#ef4444",
        "#8b5cf6", "#06b6d4", "#f97316", "#ec4899",
        "#14b8a6", "#6366f1",
    ]
    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        category_totals.values,
        labels=None,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors[: len(category_totals)],
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
        pctdistance=0.78,
    )
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    # Custom legend
    legend_patches = [
        mpatches.Patch(color=colors[i], label=f"{cat}  (₹{val:,.0f})")
        for i, (cat, val) in enumerate(category_totals.items())
    ]
    ax.legend(
        handles=legend_patches,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        fontsize=9,
        frameon=False,
    )
    ax.set_title("Expense Distribution by Category", fontsize=13, fontweight="bold", pad=14)
    fig.tight_layout()
    return fig


# ── Helper: Bar Chart ─────────────────────────────────────────
def plot_bar_chart(category_totals: pd.Series) -> plt.Figure:
    """Generate a horizontal bar chart for category-wise spending."""
    colors = [
        "#3b82f6", "#10b981", "#f59e0b", "#ef4444",
        "#8b5cf6", "#06b6d4", "#f97316", "#ec4899",
        "#14b8a6", "#6366f1",
    ]
    fig, ax = plt.subplots(figsize=(7, max(3.5, len(category_totals) * 0.7)))

    bars = ax.barh(
        category_totals.index,
        category_totals.values,
        color=colors[: len(category_totals)],
        edgecolor="white",
        height=0.55,
    )

    # Value labels inside bars
    for bar, val in zip(bars, category_totals.values):
        ax.text(
            bar.get_width() * 0.97,
            bar.get_y() + bar.get_height() / 2,
            f"₹{val:,.0f}",
            va="center",
            ha="right",
            fontsize=9,
            color="white",
            fontweight="bold",
        )

    ax.set_xlabel("Total Amount Spent (₹)", fontsize=10)
    ax.set_title("Category-wise Spending", fontsize=13, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", labelsize=10)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════

def main():
    # ── Sidebar ──────────────────────────────────────────────
    with st.sidebar:
        st.image(
            "https://img.icons8.com/fluency/96/money-bag.png",
            width=72,
        )
        st.markdown("## 💰 Smart Expense Tracker")
        st.markdown(
            "Upload your expense CSV file to instantly analyze your spending patterns, "
            "visualize categories, and get actionable saving tips."
        )
        st.markdown("---")
        st.markdown("**Required CSV columns:**")
        st.code("Date, Category, Amount", language="text")
        st.markdown("---")
        st.markdown("**Sample CSV format:**")
        st.code(
            "Date,Category,Amount\n"
            "2024-01-05,Food,450\n"
            "2024-01-06,Transport,120\n"
            "2024-01-07,Shopping,800",
            language="text",
        )
        st.markdown("---")
        st.caption("Built with ❤️ using Streamlit · Pandas · Matplotlib")

    # ── Page Header ──────────────────────────────────────────
    st.markdown('<p class="main-title">💰 Smart Expense Tracker</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-title">Upload your expense data and get instant insights, charts & saving tips.</p>',
        unsafe_allow_html=True,
    )

    # ── File Upload ──────────────────────────────────────────
    uploaded_file = st.file_uploader(
        "📂 Upload your CSV file",
        type=["csv"],
        help="The CSV must contain Date, Category, and Amount columns.",
    )

    # Load sample data button (helpful for first-time users)
    use_sample = st.button("▶ Try with Sample Data", type="secondary")

    # ── Determine Data Source ─────────────────────────────────
    df_raw = None

    if use_sample:
        # Load bundled sample CSV
        try:
            df_raw = pd.read_csv("data.csv")
            st.success("✅ Sample data loaded successfully!")
        except FileNotFoundError:
            st.error("❌ `data.csv` not found. Please place it in the project folder.")
            return

    elif uploaded_file is not None:
        try:
            df_raw = pd.read_csv(uploaded_file)
            st.success(f"✅ File **{uploaded_file.name}** uploaded successfully!")
        except Exception as e:
            st.error(f"❌ Could not read file: {e}")
            return

    # If no data yet, show a placeholder
    if df_raw is None:
        st.info("👆 Upload a CSV file above or click **Try with Sample Data** to get started.")
        return

    # ── Validate Columns ──────────────────────────────────────
    is_valid, error_msg = validate_dataframe(df_raw)
    if not is_valid:
        st.error(f"❌ Invalid CSV format. {error_msg}")
        return

    # ── Clean & Prepare Data ──────────────────────────────────
    df = prepare_data(df_raw.copy())

    if df.empty:
        st.warning("⚠️ No valid rows found after cleaning. Check your Amount and Date values.")
        return

    # ── Compute Summary Statistics ────────────────────────────
    total_expense   = df["amount"].sum()
    num_transactions = len(df)
    avg_per_txn     = df["amount"].mean()
    date_range      = f"{df['date'].min().strftime('%d %b %Y')}  →  {df['date'].max().strftime('%d %b %Y')}"

    category_totals = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    top_category    = category_totals.idxmax()
    top_amount      = category_totals.max()

    # ── KPI Metrics Row ───────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-header">📊 Summary</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💸 Total Expenses",   f"₹{total_expense:,.2f}")
    col2.metric("🧾 Transactions",      f"{num_transactions}")
    col3.metric("📈 Avg per Transaction", f"₹{avg_per_txn:,.2f}")
    col4.metric("📅 Date Range",        date_range)

    # ── Highest Spending Insight ──────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-header">🔍 Top Spending Insight</p>', unsafe_allow_html=True)

    pct = (top_amount / total_expense) * 100
    st.markdown(
        f'<div class="insight-box">'
        f"💡 You spent the most on <strong>{top_category}</strong> — "
        f"<strong>₹{top_amount:,.2f}</strong> ({pct:.1f}% of total expenses)."
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Charts ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-header">📉 Spending Visualizations</p>', unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns([1, 1.1])

    with chart_col1:
        st.subheader("Pie Chart")
        fig_pie = plot_pie_chart(category_totals)
        st.pyplot(fig_pie)
        plt.close(fig_pie)

    with chart_col2:
        st.subheader("Bar Chart")
        fig_bar = plot_bar_chart(category_totals)
        st.pyplot(fig_bar)
        plt.close(fig_bar)

    # ── Category Breakdown Table ──────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-header">📋 Category Breakdown</p>', unsafe_allow_html=True)

    breakdown_df = category_totals.reset_index()
    breakdown_df.columns = ["Category", "Total Spent (₹)"]
    breakdown_df["% of Total"] = (breakdown_df["Total Spent (₹)"] / total_expense * 100).round(2)
    breakdown_df["Total Spent (₹)"] = breakdown_df["Total Spent (₹)"].apply(lambda x: f"₹{x:,.2f}")
    breakdown_df["% of Total"] = breakdown_df["% of Total"].apply(lambda x: f"{x}%")
    st.dataframe(breakdown_df, use_container_width=True, hide_index=True)

    # ── Smart Suggestions ─────────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="section-header">💡 Smart Saving Suggestions</p>', unsafe_allow_html=True)

    for cat in category_totals.index:
        suggestion = get_suggestion(cat)
        cat_pct = (category_totals[cat] / total_expense) * 100

        # Use warning style for categories taking >30% of budget
        box_class = "warning-box" if cat_pct > 30 else "insight-box"
        label = f"⚠️ High Spend — {cat}" if cat_pct > 30 else cat

        st.markdown(
            f'<div class="{box_class}">'
            f"<strong>{label}</strong><br>{suggestion}"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ── Raw Data Preview ──────────────────────────────────────
    st.markdown("---")
    with st.expander("🗂️ View Raw Data", expanded=False):
        # Format date and amount for display
        display_df = df.copy()
        display_df["date"]   = display_df["date"].dt.strftime("%d %b %Y")
        display_df["amount"] = display_df["amount"].apply(lambda x: f"₹{x:,.2f}")
        display_df.columns   = display_df.columns.str.title()
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(display_df)} record(s) after cleaning.")

    # ── Footer ───────────────────────────────────────────────
    st.markdown("---")
    st.caption("Smart Expense Analyzer · Built with Streamlit, Pandas & Matplotlib · v1.0")


# ── Entry Point ───────────────────────────────────────────────
if __name__ == "__main__":
    main()
