import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Global Dollar Shortage Simulator", page_icon="💵", layout="wide")

st.title("💵 The Global Dollar Shortage Paradox")
st.caption("An interactive macro-finance sandbox: from global funding shocks to Vietnamese firm-level liquidity risk.")

st.info(
    " A positive funding gap means scheduled USD payments are not fully covered."
)

with st.sidebar:
    st.header("Company balance sheet — next 90 days")
    usd_payments = st.slider("USD payments due ($m)", 1.0, 30.0, 10.0, 0.5)
    usd_assets = st.slider("Liquid USD assets ($m)", 0.0, 15.0, 2.0, 0.5)
    usd_receipts = st.slider("Expected USD receipts ($m)", 0.0, 25.0, 5.0, 0.5)
    usd_refinancing = st.slider("Expected USD refinancing ($m)", 0.0, 15.0, 2.0, 0.5)

    st.header("Global shock")
    us_rate_shock = st.slider("US funding-rate shock (percentage points)", 0.0, 5.0, 1.0, 0.25)
    export_shock = st.slider("USD export receipts lost ($m)", 0.0, 25.0, 1.0, 0.5)
    refinancing_lost = st.slider("Dollar refinancing lost ($m)", 0.0, 15.0, 1.0, 0.5)
    vnd_depreciation = st.slider("VND depreciation against USD (%)", 0, 30, 5, 1)

# Apply absolute USD shocks, ensuring values don't drop below zero
effective_receipts = max(0.0, usd_receipts - export_shock)
effective_refinancing = max(0.0, usd_refinancing - refinancing_lost)
funding_gap = max(0.0, usd_payments - usd_assets - effective_receipts - effective_refinancing)
coverage = min(100.0, (usd_assets + effective_receipts + effective_refinancing) / usd_payments * 100)

rate_sensitivity = us_rate_shock * (usd_refinancing * 0.02)
fx_revaluation = usd_payments * vnd_depreciation / 100

m1, m2, m3, m4 = st.columns(4)
m1.metric("USD funding gap", f"${funding_gap:.2f}m", "Uncovered" if funding_gap > 0 else "Covered")
m2.metric("Payment coverage", f"{coverage:.1f}%")
m3.metric("USD receipts after shock", f"${effective_receipts:.2f}m")
m4.metric("Refinancing after shock", f"${effective_refinancing:.2f}m")

left, right = st.columns(2)

with left:
    st.subheader("1. Where the dollars go")

    fig = go.Figure()

    # Obligation stack
    fig.add_trace(
        go.Bar(
            name="Payments due",
            x=["Obligation"],
            y=[usd_payments],
            text=[f"${usd_payments:.1f}m"],
            textposition="auto",
            marker_color="indianred"
        )
    )

    # Available resources stack
    fig.add_trace(
        go.Bar(
            name="Liquid assets",
            x=["Available Resources"],
            y=[usd_assets],
            text=[f"${usd_assets:.1f}m"],
            textposition="auto",
            marker_color="lightgreen"
        )
    )
    
    fig.add_trace(
        go.Bar(
            name="USD receipts",
            x=["Available Resources"],
            y=[effective_receipts],
            text=[f"${effective_receipts:.1f}m"],
            textposition="auto",
            marker_color="mediumseagreen"
        )
    )
    
    fig.add_trace(
        go.Bar(
            name="Refinancing",
            x=["Available Resources"],
            y=[effective_refinancing],
            text=[f"${effective_refinancing:.1f}m"],
            textposition="auto",
            marker_color="seagreen"
        )
    )

    fig.update_layout(
        barmode="stack",
        title="Obligations versus available dollar sources",
        yaxis_title="USD millions",
        xaxis_title="",
        template="plotly_white",
        showlegend=True,
        dragmode="zoom"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("2. Stress-test the refinancing channel")

    # Generate shock increments up to the total available expected refinancing
    shocks = np.arange(0.0, usd_refinancing + 0.5, 0.5) if usd_refinancing > 0 else [0.0]

    gaps = [
        max(
            0,
            usd_payments - (
                usd_assets
                + effective_receipts
                + max(0.0, usd_refinancing - s)
            )
        )
        for s in shocks
    ]

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=shocks,
            y=gaps,
            mode="lines+markers",
            line=dict(width=3),
            marker=dict(size=7),
            hovertemplate=(
                "Refinancing lost: $%{x:.2f}m"
                "<br>Funding gap: $%{y:.2f}m"
                "<extra></extra>"
            )
        )
    )

    fig2.update_layout(
        title="How rollover stress changes the funding gap",
        xaxis_title="Amount of refinancing lost ($m)",
        yaxis_title="Funding gap (USD millions)",
        template="plotly_white",
        hovermode="x unified",
        dragmode="zoom"
    )

    st.plotly_chart(fig2, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### Company A — Exporter")
    a_payments = st.number_input("A: USD payments due ($m)", min_value=0.0, value=10.0, step=0.5)
    a_assets = st.number_input("A: liquid USD assets ($m)", min_value=0.0, value=2.0, step=0.5)
    a_receipts = st.number_input("A: expected USD receipts ($m)", min_value=0.0, value=8.0, step=0.5)
    a_rollover = st.number_input("A: expected refinancing ($m)", min_value=0.0, value=1.0, step=0.5)
    
    # Applying the absolute $m shock directly
    a_gap = max(0.0, a_payments - a_assets - max(0.0, a_receipts - export_shock) - max(0.0, a_rollover - refinancing_lost))
    st.metric("A: funding gap", f"${a_gap:.2f}m")

with col_b:
    st.markdown("### Company B — Domestic seller")
    b_payments = st.number_input("B: USD payments due ($m)", min_value=0.0, value=8.0, step=0.5)
    b_assets = st.number_input("B: liquid USD assets ($m)", min_value=0.0, value=0.5, step=0.5)
    b_receipts = st.number_input("B: expected USD receipts ($m)", min_value=0.0, value=1.0, step=0.5)
    b_rollover = st.number_input("B: expected refinancing ($m)", min_value=0.0, value=2.0, step=0.5)
    
    # Applying the absolute $m shock directly
    b_gap = max(0.0, b_payments - b_assets - max(0.0, b_receipts - export_shock) - max(0.0, b_rollover - refinancing_lost))
    st.metric("B: funding gap", f"${b_gap:.2f}m")

st.caption(
    f"If the VND depreciates by {vnd_depreciation}%, the VND value of the ${usd_payments:.2f}m "
    f"USD payment obligation rises by {vnd_depreciation}% relative to its initial VND value. "
    f"For scale, the increase equals {fx_revaluation:.2f} USD-million-equivalent at the original exchange rate."
)