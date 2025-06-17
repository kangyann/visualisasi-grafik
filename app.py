import streamlit as st
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Model Matematika Interaktif", layout="wide")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Linear Programming", "EOQ", "Antrian M/M/1", "Break Even Point (BEP)", "Tentang"]
)

# --- 1. Linear Programming ---
with tab1:
    st.header("Linear Programming Interaktif")

    st.markdown("**📚 STUDI KASUS: Optimalisasi Produksi Produk**")
    st.markdown(
        "Sebuah pabrik memproduksi dua jenis produk: Produk X dan Produk Y. Tujuan dari manajer produksi adalah memaksimalkan keuntungan total dengan tetap memperhatikan keterbatasan sumber daya yang tersedia (misalnya tenaga kerja, bahan baku, atau waktu mesin)."
    )
    st.latex(r"Rumus : Z = c_1x + c_2y")
    c1Col, c2Col = st.columns([1, 1])
    with c1Col:
        c1 = st.number_input("Koefisien (x)", value=3)
    with c2Col:
        c2 = st.number_input("Koefisien (y)", value=5)
    st.latex(f"Z = {c1}x + {c2}y")
    st.markdown("Fungsi yang ingin dimaksimalkan:")
    st.markdown(
        f"Artinya:<br>Keuntungan dari setiap unit Produk X = Rp{c1} <br> Keuntungan dari setiap unit Produk Y = Rp{c2} <br>x = jumlah unit Produk X yang diproduksi <br>y = jumlah unit Produk Y yang diproduksi",
        unsafe_allow_html=True,
    )
    st.markdown("**Kendala:**")
    b1Col, a1Col, a2Col = st.columns([1, 1, 1])
    with b1Col:
        b1 = st.number_input("b₁", value=6)
    with a1Col:
        a1 = st.number_input("a₁ (x + 2y ≤ b₁)", value=1)
    with a2Col:
        a2 = st.number_input("a₂ (x + 2y ≤ b₁)", value=2)
    st.latex(rf"x + 2y \leq {b1}")
    st.text(
        "Misalnya: batasan tenaga kerja — setiap Produk X butuh 1 jam, Produk Y butuh 2 jam, maksimal 6 jam tersedia"
    )

    b2Col, a3Col, a4Col = st.columns([1, 1, 1])
    with b2Col:
        b2 = st.number_input("b₂", value=12)
    with a3Col:
        a3 = st.number_input("a₃ (3x + 2y ≤ b₂)", value=3)
    with a4Col:
        a4 = st.number_input("a₄ (3x + 2y ≤ b₂)", value=2)
    st.latex(rf"3x + 2y \leq {b2}")
    st.text(
        "Misalnya: batasan bahan baku — Produk X butuh 3 unit, Produk Y butuh 2 unit, maksimal 12 unit tersedia."
    )
    c = [-c1, -c2]
    A = [[a1, a2], [a3, a4]]
    b = [b1, b2]
    bounds = [(0, None), (0, None)]

    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method="highs")

    if res.success:
        x, y = res.x
        st.success(f"x = {x:.2f}, y = {y:.2f}, Z = {-(res.fun):.2f}")

        x_vals = np.linspace(0, 20, 400)
        y1 = (b1 - a1 * x_vals) / a2
        y2 = (b2 - a3 * x_vals) / a4
        y3 = np.minimum(y1, y2)

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(x_vals, y1, label="Kendala 1")
        ax.plot(x_vals, y2, label="Kendala 2")
        ax.fill_between(x_vals, 0, y3, where=(y3 >= 0), color="orange", alpha=0.3)
        ax.plot(x, y, "ro", label="Solusi Optimal")
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        ax.set_title("Area Feasible")

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.image(buf, width=480)
        st.markdown("### ✍️ Penjelasan:")
        st.markdown(
            """
        - Garis biru dan oranye adalah batas dari dua kendala.
        - Area berwarna oranye muda adalah **wilayah feasible** (layak).
        - Titik merah adalah **solusi optimal** yang memaksimalkan fungsi tujuan Z.
        """
        )
    else:
        st.error("Solusi tidak ditemukan.")

# --- 2. EOQ ---
with tab2:
    st.header("EOQ (Economic Order Quantity)")

    st.latex(r"EOQ = \sqrt{\frac{2DS}{H}}")

    st.markdown(
        """
    Keterangan:
    - `D` = Permintaan tahunan (unit/tahun)
    - `S` = Biaya pemesanan per order (tetap)
    - `H` = Biaya penyimpanan per unit per tahun
    """
    )

    st.divider()

    # Studi kasus
    with st.expander("📄 Studi Kasus: Toko Kertas NuvPaper"):
        st.markdown(
            """
    **NuvPaper** menjual kertas A4 dalam jumlah besar. Tiap tahun permintaan mencapai **1.000 unit**.

    **Masalah:** Manajer logistik ingin tahu berapa jumlah pembelian optimal sekali order agar biaya total minimum.

    **Data Diketahui:**

    | Komponen                  | Nilai        | Keterangan                             |
    |---------------------------|--------------|-----------------------------------------|
    | Permintaan Tahunan (D)    | 1.000 unit   | Total kebutuhan pelanggan               |
    | Biaya Pemesanan per Order (S) | Rp 50.000 | Biaya tetap tiap kali pesan             |
    | Biaya Penyimpanan per Unit per Tahun (H) | Rp 2.000 | Biaya gudang, kerusakan, dll             |
        """
        )

    st.divider()

    # Form input EOQ
    st.subheader("🧮 Hitung EOQ Kamu Sendiri")

    colD, colS, colH = st.columns([1, 1, 1])
    with colD:
        D = st.number_input("Permintaan Tahunan (D)", value=1000)
    with colS:
        S = st.number_input("Biaya Pemesanan (S)", value=50000)
    with colH:
        H = st.number_input("Biaya Penyimpanan per unit (H)", value=2000)

    if D > 0 and S > 0 and H > 0:
        EOQ = np.sqrt((2 * D * S) / H)
        st.success(f"EOQ: {EOQ:.2f} unit")

        Q = np.arange(1, int(EOQ * 2))
        TC = (D / Q) * S + (Q / 2) * H

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(Q, TC, label="Total Cost")
        ax.axvline(EOQ, color="red", linestyle="--", label=f"EOQ ≈ {EOQ:.0f}")
        ax.set_xlabel("Order Quantity")
        ax.set_ylabel("Total Cost")
        ax.set_title("EOQ vs Total Cost")
        ax.legend()
        # st.pyplot(fig)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.image(buf, width=480)
        st.markdown("### ✍️ Penjelasan:")
        st.markdown(
            f"""
        - Permintaan tahunan: **{D:.0f} unit**
        - Biaya pemesanan: **Rp {S:,.0f}**
        - Biaya penyimpanan: **Rp {H:,.0f} per unit**
        - Jadi, pemesanan optimal adalah **{EOQ:.2f} unit** setiap kali pesan.
        """
        )
    else:
        st.warning("Masukkan nilai D, S, dan H yang valid (> 0).")

# --- 3. Antrian M/M/1 ---
with tab3:
    st.header("Model Antrian M/M/1")
    with st.expander("📄 Studi Kasus: NuvBank Customer Service"):
        st.markdown("""
        NuvBank memiliki satu loket layanan. Setiap jam:
        - Rata-rata **5 pelanggan** datang (λ)
        - Rata-rata **8 pelanggan** dapat dilayani (μ)

        Tujuan: Menghitung performa antrian dan waktu tunggu rata-rata.
        """)

    st.divider()
    colLam, colMu = st.columns([1, 1])
    with colLam:
        lam = st.number_input("Laju Kedatangan (λ)", value=5, min_value=1)
    with colMu:
        mu = st.number_input("Laju Pelayanan (μ)", value=8, min_value=1)

    if lam >= mu:
        st.error("Sistem tidak stabil: λ harus < μ")
    else:
        rho = lam / mu
        L = rho / (1 - rho)
        Lq = rho**2 / (1 - rho)
        W = 1 / (mu - lam)
        Wq = rho / (mu - lam)
        st.latex(r"\rho = \frac{\lambda}{\mu} = " + f"{rho:.3f}")
        st.latex(r"L = \frac{\lambda}{\mu - \lambda} = " + f"{L:.9f}")
        st.latex(r"L_q = \frac{\lambda^2}{\mu(\mu - \lambda)} = " + f"{Lq:.9f}")
        st.latex(r"W = \frac{1}{\mu - \lambda} = " + f"{W:.9f} jam")
        st.latex(r"W_q = \frac{\lambda}{\mu(\mu - \lambda)} = " + f"{Wq:.9f} jam")

        st.success("Hasil:")
        st.markdown(f"""
        - ρ (utilisasi): **{rho:.2f}**
        - L (sistem): **{L:.2f} orang**
        - Lq (antrian): **{Lq:.2f} orang**
        - W (dalam sistem): **{W:.2f} jam**
        - Wq (dalam antrian): **{Wq:.2f} jam**
        """)

        lambdas = np.linspace(0.5, mu - 0.1, 100)
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

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.image(buf, width=480)

        st.markdown(
            """
        ### 📌 Penjelasan Grafik:
        - **Semakin besar λ**, sistem semakin sibuk.
        - Ketika λ hampir menyamai μ, **semua metrik melonjak**: antrian dan waktu meningkat tajam.
        - Model valid **hanya jika λ < μ**.
        """
        )

# --- 4. BEP ---
with tab4:
    st.header("Break Even Point (BEP)")
    st.markdown("Model **Break Even Point (BEP)** menunjukkan titik impas, yaitu saat pendapatan sama dengan biaya total.")
    st.latex(r"Rumus : BEP = \frac{FC}{P - VC}")
    st.divider()

    with st.expander("📄 Studi Kasus: NuvDrink"):
        st.markdown("""
        - Biaya Tetap: Rp 10.000.000
        - Biaya Variabel per unit: Rp 5.000
        - Harga Jual per unit: Rp 12.000

        Tujuan: Menentukan jumlah minimal produk yang harus dijual agar tidak rugi.
        """)

    st.divider()
    FC = st.number_input("Biaya Tetap (Fixed Cost)", value=10000000)
    VC = st.number_input("Biaya Variabel per Unit", value=5000)
    P = st.number_input("Harga Jual per Unit", value=12000)

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
        ax.axvline(
            BEP_unit, color="red", linestyle="--", label=f"BEP ≈ {BEP_unit:.0f} unit"
        )
        ax.set_xlabel("Unit Terjual")
        ax.set_ylabel("Rupiah")
        ax.set_title("Break Even Point")
        ax.legend()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        st.image(buf, width=480)

        st.markdown(
            """
        ### 📌 Penjelasan Grafik:
        - Garis **biru**: pendapatan (TR = P × Q)
        - Garis **orange**: biaya total (TC = FC + VC × Q)
        - Titik **potong biru** adalah titik impas (BEP)
        - Sebelah kiri BEP: Rugi, Sebelah kanan BEP: Untung
        """
        )
    else:
        st.warning("P harus lebih besar dari VC, dan FC harus > 0.")

# --- 5. Tentang ---
with tab5:
    st.header("Tentang Aplikasi")
    st.markdown(
        """
    Aplikasi ini memungkinkan Anda menghitung dan memvisualisasikan empat model matematika klasik:
    
    1. **Linear Programming**
    2. **EOQ (Economic Order Quantity)**
    3. **Antrian M/M/1**
    4. **Break Even Point (BEP)**

    Semua model dapat disesuaikan melalui input pengguna. Cocok untuk simulasi, analisis, dan edukasi.  
    👨‍💻 Dibuat oleh: Kelompok 6
    """
    )
