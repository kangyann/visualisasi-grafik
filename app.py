import streamlit as st
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt

st.set_page_config(page_title="Model Matematika Interaktif", layout="wide")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Linear Programming", "EOQ", "Antrian M/M/1", "Break Even Point (BEP)", "Tentang"
])

# --- 1. Linear Programming ---
with tab1:
    st.header("Linear Programming Interaktif")

    st.markdown("**Fungsi Tujuan:**")
    c1 = st.number_input("Koefisien x", value=3.0)
    c2 = st.number_input("Koefisien y", value=5.0)

    st.markdown("**Kendala:**")
    a1 = st.number_input("a₁ (x + 2y ≤ b₁)", value=1.0)
    a2 = st.number_input("a₂ (x + 2y ≤ b₁)", value=2.0)
    b1 = st.number_input("b₁", value=6.0)

    a3 = st.number_input("a₃ (3x + 2y ≤ b₂)", value=3.0)
    a4 = st.number_input("a₄ (3x + 2y ≤ b₂)", value=2.0)
    b2 = st.number_input("b₂", value=12.0)

    c = [-c1, -c2]
    A = [[a1, a2], [a3, a4]]
    b = [b1, b2]
    bounds = [(0, None), (0, None)]

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if res.success:
        x, y = res.x
        st.success(f"x = {x:.2f}, y = {y:.2f}, Z = {-(res.fun):.2f}")

        x_vals = np.linspace(0, 20, 400)
        y1 = (b1 - a1 * x_vals) / a2
        y2 = (b2 - a3 * x_vals) / a4
        y3 = np.minimum(y1, y2)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x_vals, y1, label="Kendala 1")
        ax.plot(x_vals, y2, label="Kendala 2")
        ax.fill_between(x_vals, 0, y3, where=(y3 >= 0), color='orange', alpha=0.3)
        ax.plot(x, y, 'ro', label='Solusi Optimal')
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.set_title("Area Feasible")
        st.pyplot(fig)
    else:
        st.error("Solusi tidak ditemukan.")

# --- 2. EOQ ---
with tab2:
    st.header("EOQ (Economic Order Quantity)")

    D = st.number_input("Permintaan Tahunan (D)", value=1000.0)
    S = st.number_input("Biaya Pemesanan (S)", value=50.0)
    H = st.number_input("Biaya Penyimpanan per unit (H)", value=2.0)

    if D > 0 and S > 0 and H > 0:
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ: {EOQ:.2f} unit")

        Q = np.arange(1, int(EOQ*2))
        TC = (D / Q) * S + (Q / 2) * H

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(Q, TC, label="Total Cost")
        ax.axvline(EOQ, color='red', linestyle='--', label=f"EOQ ≈ {EOQ:.0f}")
        ax.set_xlabel("Order Quantity")
        ax.set_ylabel("Total Cost")
        ax.set_title("EOQ vs Total Cost")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Masukkan nilai D, S, dan H yang valid (> 0).")

# --- 3. Antrian M/M/1 ---
with tab3:
    st.header("Model Antrian M/M/1")

    lam = st.number_input("Laju Kedatangan (λ)", value=5.0, min_value=0.1)
    mu = st.number_input("Laju Pelayanan (μ)", value=8.0, min_value=0.1)

    if lam >= mu:
        st.error("Sistem tidak stabil: λ harus < μ")
    else:
        rho = lam / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = 1 / (mu - lam)
        Wq = rho / (mu - lam)

        st.success("Hasil:")
        st.write(f"ρ (utilisasi): {rho:.2f}")
        st.write(f"L (sistem): {L:.2f}")
        st.write(f"Lq (antrian): {Lq:.2f}")
        st.write(f"W (dalam sistem): {W:.2f} jam")
        st.write(f"Wq (dalam antrian): {Wq:.2f} jam")

        lambdas = np.linspace(0.1, mu - 0.1, 100)
        rhos = lambdas / mu
        L_vals = rhos / (1 - rhos)
        Lq_vals = rhos**2 / (1 - rhos)
        W_vals = 1 / (mu - lambdas)
        Wq_vals = rhos / (mu - lambdas)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(rhos, L_vals, label="L (Sistem)")
        ax.plot(rhos, Lq_vals, label="Lq (Antrian)")
        ax.plot(rhos, W_vals, label="W")
        ax.plot(rhos, Wq_vals, label="Wq")
        ax.set_xlabel("Utilisasi (ρ)")
        ax.set_ylabel("Nilai")
        ax.set_title("Antrian M/M/1")
        ax.legend()
        st.pyplot(fig)

# --- 4. BEP ---
with tab4:
    st.header("Break Even Point (BEP)")

    FC = st.number_input("Biaya Tetap (Fixed Cost)", value=10000.0)
    VC = st.number_input("Biaya Variabel per Unit", value=50.0)
    P = st.number_input("Harga Jual per Unit", value=100.0)

    if P > VC and FC > 0:
        BEP_unit = FC / (P - VC)
        BEP_rp = FC / (1 - VC / P)

        st.success(f"BEP Unit: {BEP_unit:.2f}")
        st.write(f"BEP Rupiah: Rp {BEP_rp:,.2f}")

        x = np.linspace(0, BEP_unit * 2, 100)
        revenue = x * P
        cost = FC + VC * x

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, revenue, label="Pendapatan")
        ax.plot(x, cost, label="Biaya Total")
        ax.axvline(BEP_unit, color='red', linestyle='--', label=f"BEP ≈ {BEP_unit:.0f} unit")
        ax.set_xlabel("Unit Terjual")
        ax.set_ylabel("Rupiah")
        ax.set_title("Break Even Point")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("P harus lebih besar dari VC, dan FC harus > 0.")

# --- 5. Tentang ---
with tab5:
    st.header("Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini memungkinkan Anda menghitung dan memvisualisasikan empat model matematika klasik:
    
    1. **Linear Programming**
    2. **EOQ (Economic Order Quantity)**
    3. **Antrian M/M/1**
    4. **Break Even Point (BEP)**

    Semua model dapat disesuaikan melalui input pengguna. Cocok untuk simulasi, analisis, dan edukasi.  
    👨‍💻 Dibuat oleh: Kang Yann
    """)
