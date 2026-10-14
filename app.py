
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Churn Intelligence | Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "Customer-Churn.csv"

BG = "#080D1A"
PANEL = "#10182A"
BORDER = "#25324B"
PURPLE = "#9B7BFF"
CYAN = "#39D6E8"
TEXT = "#F0F4FF"
MUTED = "#92A0BA"


# --------------------------------------------------
# PREMIUM MIDNIGHT PRO THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --bg: #080D1A;
        --panel: #10182A;
        --border: #25324B;
        --purple: #9B7BFF;
        --cyan: #39D6E8;
        --text: #F0F4FF;
        --muted: #92A0BA;
    }

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 85% 0%, #192044 0%, transparent 38%),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(8, 13, 26, 0.85);
    }

    [data-testid="stSidebar"] {
        background: #0B1222;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text);
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    h1, h2, h3 {
        color: var(--text) !important;
        letter-spacing: -0.035em;
    }

    p, label, .stMarkdown {
        color: var(--text);
    }

    .hero {
        padding: 8px 0 26px 0;
    }

    .eyebrow {
        color: var(--cyan);
        font-size: 0.73rem;
        font-weight: 700;
        letter-spacing: 0.19em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: clamp(2rem, 4vw, 3.15rem);
        font-weight: 800;
        letter-spacing: -0.065em;
        line-height: 1.1;
        margin: 0;
        color: var(--text);
    }

    .hero-title span {
        color: var(--purple);
    }

    .hero-subtitle {
        color: var(--muted);
        font-size: 0.98rem;
        line-height: 1.7;
        margin-top: 12px;
        max-width: 680px;
    }

    .section-heading {
        font-size: 1.08rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        margin: 16px 0 14px 0;
    }

    .section-caption {
        color: var(--muted);
        font-size: 0.84rem;
        margin-top: -8px;
        margin-bottom: 16px;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #121C31, #0D1526);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 19px 20px;
        min-height: 125px;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.13);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: clamp(1.35rem, 2.2vw, 2rem) !important;
        font-weight: 750 !important;
        letter-spacing: -0.04em;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.78rem !important;
    }

    div[data-testid="stPlotlyChart"] {
        background: linear-gradient(145deg, #10182A, #0C1424);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 8px 8px 0 8px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    .stSelectbox label,
    .stMultiSelect label {
        color: #C8D2E6 !important;
        font-size: 0.83rem !important;
        font-weight: 600 !important;
    }

    .stButton button,
    .stDownloadButton button {
        background: linear-gradient(100deg, #8C6BFF, #6950D8);
        color: white;
        border: 1px solid #A28AFF;
        border-radius: 9px;
        font-weight: 650;
        transition: all 0.2s ease;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        border-color: var(--cyan);
        color: white;
        box-shadow: 0 0 18px rgba(57, 214, 232, 0.15);
    }

    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    hr {
        border-color: var(--border);
    }

    .footer {
        color: var(--muted);
        font-size: 0.76rem;
        text-align: center;
        padding-top: 26px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# DATA LOADING AND CLEANING
# --------------------------------------------------
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    # Clean text columns
    for column in data.select_dtypes(include=["object"]).columns:
        data[column] = data[column].str.strip()

    # Convert numeric columns safely
    for column in ["tenure", "MonthlyCharges", "TotalCharges"]:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column].replace("", pd.NA),
                errors="coerce",
            )

    return data


if not DATA_FILE.exists():
    st.error(
        "Dataset not found. Place Customer-Churn.csv "
        "in the same folder as app.py."
    )
    st.stop()

try:
    df = load_data(str(DATA_FILE))
except Exception as error:
    st.error(f"Could not read the dataset: {error}")
    st.stop()

required_columns = [
    "Churn",
    "Contract",
    "InternetService",
    "tenure",
    "MonthlyCharges",
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(
        "The dataset is missing columns expected by this dashboard: "
        + ", ".join(missing_columns)
    )
    st.info(
        "Check that Customer-Churn.csv is the original customer churn "
        "dataset, or adapt the column names in app.py."
    )
    st.stop()

df["Churn"] = df["Churn"].astype("string").str.strip()


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">CUSTOMER ANALYTICS / OVERVIEW</div>
        <div class="hero-title">Churn <span>Intelligence.</span></div>
        <div class="hero-subtitle">
            Explore customer retention, identify churn patterns, and
            understand the factors shaping your customer base.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 20px 0;">
            <div style="color:#39D6E8;font-size:0.7rem;
                        font-weight:700;letter-spacing:0.17em;">
                ANALYTICS WORKSPACE
            </div>
            <div style="color:#F0F4FF;font-size:1.45rem;
                        font-weight:800;letter-spacing:-0.05em;
                        margin-top:6px;">
                Data Explorer
            </div>
            <div style="color:#92A0BA;font-size:0.8rem;
                        margin-top:6px;">
                Refine the customer view
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Filters")

    contract_options = sorted(
        df["Contract"].dropna().astype(str).unique().tolist()
    )
    internet_options = sorted(
        df["InternetService"].dropna().astype(str).unique().tolist()
    )

    selected_contracts = st.multiselect(
        "Contract type",
        options=contract_options,
        default=contract_options,
        help="Choose one or more contract types.",
    )

    selected_internet = st.multiselect(
        "Internet service",
        options=internet_options,
        default=internet_options,
        help="Choose one or more service types.",
    )

    churn_options = ["All", "Yes", "No"]
    selected_churn = st.selectbox(
        "Churn status",
        options=churn_options,
        index=0,
    )

    st.divider()

    st.caption(f"Dataset rows: {len(df):,}")
    st.caption("Source: Customer-Churn.csv")


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
filtered = df[
    df["Contract"].astype(str).isin(selected_contracts)
    & df["InternetService"].astype(str).isin(selected_internet)
].copy()

if selected_churn != "All":
    filtered = filtered[
        filtered["Churn"].str.lower() == selected_churn.lower()
    ].copy()


# --------------------------------------------------
# KPI METRICS
# --------------------------------------------------
total_customers = len(filtered)

churn_mask = filtered["Churn"].str.lower().eq("yes").fillna(False)
churn_rate = churn_mask.mean() * 100 if total_customers else 0

avg_monthly = (
    filtered["MonthlyCharges"].mean()
    if total_customers
    else None
)

avg_tenure = (
    filtered["tenure"].mean()
    if total_customers
    else None
)

st.markdown(
    '<div class="section-heading">Performance overview</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Key customer metrics for your current filter selection.'
    '</div>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Customers in view",
    f"{total_customers:,}",
)

m2.metric(
    "Churn rate",
    f"{churn_rate:.1f}%",
)

m3.metric(
    "Avg. monthly charges",
    f"${avg_monthly:,.2f}" if pd.notna(avg_monthly) else "N/A",
)

m4.metric(
    "Avg. tenure",
    f"{avg_tenure:.1f} months" if pd.notna(avg_tenure) else "N/A",
)


# --------------------------------------------------
# CHART THEME
# --------------------------------------------------
def style_chart(fig, height=350):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, sans-serif",
            color=TEXT,
            size=12,
        ),
        margin=dict(l=18, r=18, t=28, b=18),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=MUTED, size=11),
        ),
        hoverlabel=dict(
            bgcolor="#151F34",
            bordercolor=BORDER,
            font=dict(color=TEXT, family="Inter, sans-serif"),
        ),
    )

    fig.update_xaxes(
        gridcolor="rgba(146,160,186,0.10)",
        linecolor=BORDER,
        zerolinecolor=BORDER,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )

    fig.update_yaxes(
        gridcolor="rgba(146,160,186,0.10)",
        linecolor=BORDER,
        zerolinecolor=BORDER,
        tickfont=dict(color=MUTED),
        title_font=dict(color=MUTED),
    )

    return fig


# --------------------------------------------------
# CHARTS
# --------------------------------------------------
st.markdown("---")
st.markdown(
    '<div class="section-heading">Retention insights</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Explore churn distribution and customer behavior.'
    '</div>',
    unsafe_allow_html=True,
)

left, right = st.columns(2, gap="large")

with left:
    st.markdown("#### Churn by contract")

    if not filtered.empty:
        contract_data = (
            filtered.groupby(["Contract", "Churn"], dropna=False)
            .size()
            .reset_index(name="Customers")
        )

        fig_contract = px.bar(
            contract_data,
            x="Contract",
            y="Customers",
            color="Churn",
            barmode="group",
            color_discrete_map={
                "Yes": PURPLE,
                "No": CYAN,
            },
            category_orders={
                "Churn": ["No", "Yes"],
            },
            labels={
                "Contract": "Contract type",
                "Customers": "Customers",
                "Churn": "Churn status",
            },
        )

        fig_contract.update_traces(
            marker_line_width=0,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Customers: %{y:,}<br>"
                "Churn: %{fullData.name}<extra></extra>"
            ),
        )

        fig_contract.update_layout(bargap=0.32)
        st.plotly_chart(
            style_chart(fig_contract),
            use_container_width=True,
        )
    else:
        st.info("No customers match these filters.")

with right:
    st.markdown("#### Monthly charges distribution")

    charge_data = filtered.dropna(subset=["MonthlyCharges"])

    if not charge_data.empty:
        fig_charges = px.histogram(
            charge_data,
            x="MonthlyCharges",
            nbins=28,
            color_discrete_sequence=[PURPLE],
            labels={
                "MonthlyCharges": "Monthly charges ($)",
                "count": "Customers",
            },
        )

        fig_charges.update_traces(
            marker_line_color=BG,
            marker_line_width=1,
            opacity=0.88,
            hovertemplate=(
                "Monthly charges: $%{x:.2f}<br>"
                "Customers: %{y}<extra></extra>"
            ),
        )

        st.plotly_chart(
            style_chart(fig_charges),
            use_container_width=True,
        )
    else:
        st.info("No monthly-charge data is available for these filters.")


# --------------------------------------------------
# TENURE DISTRIBUTION
# --------------------------------------------------
st.markdown("---")
st.markdown("#### Customer tenure distribution")

tenure_data = filtered.dropna(subset=["tenure"])

if not tenure_data.empty:
    fig_tenure = px.histogram(
        tenure_data,
        x="tenure",
        nbins=30,
        color_discrete_sequence=[CYAN],
        labels={
            "tenure": "Tenure (months)",
            "count": "Customers",
        },
    )

    fig_tenure.update_traces(
        marker_line_color=BG,
        marker_line_width=1,
        opacity=0.88,
        hovertemplate=(
            "Tenure: %{x} months<br>"
            "Customers: %{y}<extra></extra>"
        ),
    )

    st.plotly_chart(
        style_chart(fig_tenure, height=320),
        use_container_width=True,
    )
else:
    st.info("No tenure data is available for these filters.")


# --------------------------------------------------
# CUSTOMER DATA TABLE
# --------------------------------------------------
st.markdown("---")
st.markdown(
    '<div class="section-heading">Customer records</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Review the filtered dataset or export the current view.'
    '</div>',
    unsafe_allow_html=True,
)

if filtered.empty:
    st.info("No records match the selected filters.")
else:
    st.dataframe(
        filtered.head(100),
        use_container_width=True,
        hide_index=True,
    )

    csv_data = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download filtered data (CSV)",
        data=csv_data,
        file_name="filtered_customer_churn.csv",
        mime="text/csv",
        use_container_width=False,
    )

    st.caption(
        f"Showing up to 100 of {len(filtered):,} matching records. "
        "The CSV download includes all matching records."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="footer">
        CHURN INTELLIGENCE &nbsp;·&nbsp; CUSTOMER ANALYTICS
        <br><br>
        Built with Python, Streamlit, Pandas and Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
