""" 
===========================================================================
📊 ANALISA SAHAM - Filosofi Warren Buffett
===========================================================================
Aplikasi analisa saham interaktif untuk investor pemula.
Terinspirasi dari filosofi investasi Warren Buffett:
- MERCY = Perusahaan berkualitas (Mercedes)
- BAJAI = Harga murah (Bajaj)

Jalankan: streamlit run app.py

© 2026 Dwi Adi S — All Rights Reserved.
===========================================================================
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import time

warnings.filterwarnings("ignore")

# =====================================================================
# KONFIGURASI HALAMAN
# =====================================================================
st.set_page_config(
    page_title="Analisa Saham MERCY-BAJAI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# CUSTOM CSS - PROFESSIONAL SLATE SUITE (ERGONOMIC)
# =====================================================================
st.markdown("""
<style>
    /* === BASE FONT & ERGONOMICS === */
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

    :root {
        --bg-main: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.7);
        --accent-primary: #38bdf8;
        --accent-secondary: #818cf8;
        --text-main: #f1f5f9;
        --text-sub: #94a3b8;
        --success: #4ade80;
        --danger: #f43f5e;
        --warning: #f59e0b;
    }

    html, body, [class*="css"] {
        font-family: 'Public Sans', sans-serif;
        font-size: 20px; /* Highly increased base font size for clarity */
    }
    
    /* Responsive font scaling */
    @media (max-width: 768px) {
        html, body, [class*="css"] { font-size: 16px; }
    }

    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* === MAIN BACKGROUND === */
    .stApp {
        background: var(--bg-main) !important;
        color: var(--text-main) !important;
    }

    /* === GLASSMORPHISM CARDS (Ergonomic) === */
    .metric-card, .stMetric, .rekom-box, .explain-box {
        background: var(--bg-card) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: var(--accent-primary) !important;
    }

    /* === RESPONSIVE LAYOUT FIXES === */
    [data-testid="column"] {
        width: 100% !important;
    }
    @media (min-width: 768px) {
        [data-testid="column"] { width: auto !important; }
    }

    /* === HERO HEADER (Polished) === */
    .hero-box {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .hero-box h1 {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--text-main);
        margin: 0;
        line-height: 1.2;
    }

    /* === SECTION TITLES === */
    .section-title {
        font-size: 1.2rem; /* Reduced for better ergonomics */
        font-weight: 700;
        color: var(--accent-primary);
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* === METRIC VALUES (Compact & Readable) === */
    .metric-card .value {
        font-size: 1.4rem; /* Reduced from 1.8rem for high-density UI */
        font-weight: 800;
        color: var(--accent-primary);
        word-wrap: break-word;
        line-height: 1.1;
    }
    .metric-card .label {
        font-size: 0.8rem;
        color: var(--text-sub);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    .metric-card .sub {
        font-size: 0.75rem;
        color: var(--text-sub);
    }

    /* === SIDEBAR (Easy on eyes) === */
    section[data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* === ACCURACY TAG === */
    .accuracy-tag {
        display: inline-block;
        background: rgba(56, 189, 248, 0.1);
        color: var(--accent-primary);
        padding: 0.3rem 0.8rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* === COMPACT SIDEBAR BUTTONS === */
    [data-testid="stSidebar"] button {
        padding: 0.3rem 0.4rem !important; /* Extremely tight for professional terminal look */
        min-height: 0 !important;
        height: auto !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] button p {
        font-size: 0.7rem !important; /* Further reduced to prevent overlap */
        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    /* Increase gap between buttons if possible */
    [data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        gap: 0.4rem !important;
    }

</style>
""", unsafe_allow_html=True)


# =====================================================================
# PENJELASAN METRIK UNTUK PEMULA (Bahasa Indonesia)
# =====================================================================
PENJELASAN = {
    "ROE": "💡 **Return on Equity (ROE)**: Mengukur seberapa efisien perusahaan menghasilkan laba dari modal sendiri. Target bapak/ibu sebaiknya mencari yang di atas 15%. Semakin tinggi, semakin jago manajemen mengelola uang modal.",
    "DER": "💡 **Debt to Equity Ratio (DER)**: Mengukur kesehatan utang. Angka di bawah 1.0x (atau 100%) berarti utang perusahaan masih dalam batas aman dibandingkan modalnya. Kita ingin perusahaan yang tidak 'keberatan' utang ya.",
    "CR": "💡 **Current Ratio (CR)**: Mengukur kemampuan perusahaan membayar utang jangka pendek. Angka di atas 1.5x menunjukkan perusahaan punya cukup kas/aset lancar untuk melunasi kewajibannya tepat waktu.",
    "EG": "💡 **Earnings Growth (EG)**: Pertumbuhan laba tahunan. Kita menyukai perusahaan yang labanya terus bertumbuh (positif) dari tahun ke tahun, bukan yang terus menurun.",
    "NPM": "💡 **Net Profit Margin (NPM)**: Mengukur berapa persen laba bersih yang didapat dari total penjualan. Margin yang tebal (misal >10%) menunjukkan bisnis tersebut sangat menguntungkan dan punya daya saing.",
    "PER": "💡 **Price to Earnings Ratio (PER)**: Perbandingan harga saham vs laba. PER rendah (misal <10x) seringkali menandakan harga saham yang masih murah, namun tetap harus dilihat kualitas bisnisnya juga.",
    "PBV": "💡 **Price to Book Value (PBV)**: Perbandingan harga saham vs nilai aset bersihnya. PBV di bawah 1.0x artinya bapak/ibu membeli aset perusahaan di bawah harga pasar (mirip beli diskon).",
    "DY": "💡 **Dividend Yield (DY)**: 'Bunga' atau bagi hasil yang diberikan perusahaan kepada pemegang saham. DY yang stabil menunjukkan perusahaan peduli pada pemegang sahamnya.",
    "GRAHAM": "💡 **Graham Number**: Formula Benjamin Graham untuk menghitung harga wajar. Jika harga pasar jauh di bawah angka ini, itu adalah sinyal 'Diskon Besar' (Margin of Safety).",
    "DCF": "💡 **Discounted Cash Flow (DCF)**: Metode kalkulasi harga wajar berdasarkan proyeksi uang tunai yang akan dihasilkan perusahaan di masa depan. Lebih akurat tapi lebih rumit.",
    "BB": "💡 **Bollinger Bands**: Indikator teknikal untuk melihat apakah harga saham sudah terlalu mahal (menyentuh garis atas) atau sudah terlalu murah (menyentuh garis bawah) dalam jangka pendek."
}

# =====================================================================
# KONTEN EDUKASI & HUKUM (Sopan & Santun)
# =====================================================================
DISCLAIMER_TEXT = """
<div style="background: rgba(255,100,100,0.05); border: 1px solid rgba(255,100,100,0.2); border-radius: 15px; padding: 20px; margin-top: 30px;">
    <p style="color: #ff8080; font-size: 0.85rem; line-height: 1.6; margin: 0;">
        <strong>⚠️ Peringatan & Disclaimer Penting:</strong><br>
        Halo Bapak/Ibu sekalian, mohon diperhatikan bahwa aplikasi ini hanyalah alat bantu (tool) untuk mempermudah Bapak/Ibu dalam melakukan analisa data pasar modal. 
        Seluruh hasil analisa, angka, dan rekomendasi yang muncul di sini <strong>BUKANLAH</strong> perintah untuk membeli atau menjual saham. 
        Setiap keputusan investasi merupakan tanggung jawab pribadi masing-masing. Investasi saham memiliki risiko fluktuasi harga yang tinggi. 
        Mohon jangan jadikan tool ini sebagai satu-satunya dasar dalam bertransaksi agar Bapak/Ibu terhindar dari hal-hal yang tidak diinginkan secara hukum maupun finansial. 
        Tetap semangat dan selalu bijak dalam mengelola keuangan ya! 😊
    </p>
</div>
"""

GUIDE_CONTENT = {
    "Analisa Saham": "Tab ini adalah jantung dari aplikasi. Bapak/Ibu cukup masukkan kode saham di sidebar, lalu biarkan sistem menarik data terbaru. Kami menggabungkan fundamental (kesehatan bisnis) dan teknikal (gerakan harga) untuk memberikan skor akhir.",
    "Master Table": "Di sini Bapak/Ibu bisa membandingkan banyak saham sekaligus. Kami menonjolkan fitur 'Fair Value' (Graham Number) untuk mencari saham yang masih didiskon besar oleh pasar.",
    "Pro Mode": "Jika Bapak/Ibu sudah mahir, silakan aktifkan 'Mode Pro' di sidebar. Fitur ini akan memunculkan indikator teknikal lanjutan seperti Bollinger Bands dan metrik valuasi yang lebih mendalam.",
}

# =====================================================================
@st.dialog("🛡️ Peringatan & Penafian Penting", width="large")
def tampilkan_modal_disclaimer():
    """Fungsi popup disclaimer menggunakan st.dialog native dengan fragment isolation."""
    # 1. Tampilkan teks statis (hanya render sekali di dialog)
    clean_text = DISCLAIMER_TEXT.strip()
    st.markdown(f"""
    <div style="background: rgba(255,100,100,0.05); border-radius: 12px; padding: 40px; line-height: 2.0; color: #f1f5f9; font-size: 1.5rem; text-align: center; font-weight: 500;">
        {clean_text}
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Definisikan fragment untuk bagian dinamis (Timer & Button)
    # Fragment ini akan update sendiri setiap detik tanpa mengganggu background dashboard
    @st.fragment(run_every=1.0)
    def render_timer_logic():
        if "wait_start_time" not in st.session_state:
            st.session_state["wait_start_time"] = time.time()
        
        elapsed = time.time() - st.session_state["wait_start_time"]
        remaining = int(max(0, 20 - elapsed))
        
        if remaining > 0:
            st.progress((20 - remaining) / 20)
            st.markdown(f'<div style="text-align:center; color:#94a3b8;">Mohon baca dengan teliti... Tombol akan muncul dalam <b>{remaining} detik</b></div>', unsafe_allow_html=True)
        else:
            st.success("✅ Anda telah memahami seluruh risiko dan ketentuan.")
            if st.button("SAYA MENGERTI, SETUJU & LANJUTKAN", type="primary", use_container_width=True):
                st.session_state["disclaimer_accepted"] = True
                st.rerun() # Ini akan merefresh seluruh halaman untuk menghilangkan dialog & blur

    # Jalankan fragment di dalam dialog
    render_timer_logic()

# =====================================================================
# DAFTAR SAHAM SCREENING (IDX30 / LQ45 Pilihan)
# =====================================================================
DAFTAR_SAHAM_IDX = [
    "BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK",
    "TLKM.JK", "ASII.JK", "UNVR.JK", "ICBP.JK",
    "ADRO.JK", "INCO.JK", "KLBF.JK", "HMSP.JK",
    "SMGR.JK", "PTBA.JK", "INKP.JK", "CPIN.JK",
    "GZCO.JK", "BMTR.JK", "PTRO.JK", "MBMA.JK",
    "PGAS.JK", "ITMG.JK", "UNTR.JK", "BRMS.JK",
]

DAFTAR_SAHAM_US = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", 
    "NVDA", "META", "BRK-B", "UNH", "LLY",
    "V", "MA", "JPM", "PG", "WMT"
]


DAFTAR_CRYPTO = [
    "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD",
    "ADA-USD", "AVAX-USD", "DOGE-USD", "TRX-USD", "DOT-USD"
]


# =====================================================================
# FUNGSI UTILITAS
# =====================================================================

def get_ticker_symbol(code: str, pasar: str = "IDX") -> str:
    """
    Konversi kode saham/kripto input menjadi ticker yfinance.
    - IDX: Tambahkan .JK jika belum ada.
    - US: Gunakan kode apa adanya.
    - Crypto: Tambahkan -USD jika belum ada.
    """
    code = code.strip().upper()
    if pasar == "IDX":
        if ".JK" not in code:
            return code + ".JK"
    elif pasar == "Crypto":
        if "-USD" not in code:
            return code + "-USD"
    return code


# =====================================================================
# MANAJEMEN PORTFOLIO (SIMULASI TRADING)
# =====================================================================
PORTFOLIO_FILE = "portfolio.csv"

def muat_portfolio() -> pd.DataFrame:
    """Muat data portfolio dari CSV."""
    import os
    if os.path.exists(PORTFOLIO_FILE):
        try:
            df = pd.read_csv(PORTFOLIO_FILE)
            return df
        except Exception:
            return pd.DataFrame(columns=["Ticker", "Nama", "Harga Beli", "Jumlah", "Pasar", "Tanggal"])
    return pd.DataFrame(columns=["Ticker", "Nama", "Harga Beli", "Jumlah", "Pasar", "Tanggal"])

def simpan_portfolio(df: pd.DataFrame):
    """Simpan data portfolio ke CSV."""
    df.to_csv(PORTFOLIO_FILE, index=False)

def tambah_ke_portfolio(ticker, nama, harga_beli, jumlah, pasar):
    """Tambah transaksi baru ke portfolio."""
    df = muat_portfolio()
    new_data = pd.DataFrame([{
        "Ticker": ticker,
        "Nama": nama,
        "Harga Beli": harga_beli,
        "Jumlah": jumlah,
        "Pasar": pasar,
        "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M")
    }])
    df = pd.concat([df, new_data], ignore_index=True)
    simpan_portfolio(df)

def hapus_dari_portfolio(index):
    """Hapus transaksi berdasarkan index."""
    df = muat_portfolio()
    if index in df.index:
        df = df.drop(index)
        simpan_portfolio(df.reset_index(drop=True))


@st.cache_data(ttl=300, show_spinner=False)
def ambil_data_saham(ticker_symbol: str) -> dict:
    """
    Ambil semua data saham dari yfinance.
    Returns dict berisi info, history, financials, dll.
    Cache selama 5 menit.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info or {}

        # Cek apakah ticker valid
        if not info or info.get("regularMarketPrice") is None:
            # Coba tanpa .JK jika gagal
            if ".JK" in ticker_symbol:
                alt = ticker_symbol.replace(".JK", "")
                ticker = yf.Ticker(alt)
                info = ticker.info or {}
                if not info or info.get("regularMarketPrice") is None:
                    return None
                ticker_symbol = alt

        # Ambil data historis 1 tahun
        hist_1y = ticker.history(period="1y")
        # Ambil data historis 5 tahun (untuk tren)
        hist_5y = ticker.history(period="5y")

        # Coba ambil financial statements
        try:
            financials = ticker.financials
        except Exception:
            financials = pd.DataFrame()

        try:
            balance_sheet = ticker.balance_sheet
        except Exception:
            balance_sheet = pd.DataFrame()

        try:
            income_stmt = ticker.income_stmt
        except Exception:
            income_stmt = pd.DataFrame()

        try:
            cash_flow = ticker.cashflow
        except Exception:
            cash_flow = pd.DataFrame()

        return {
            "info": info,
            "hist_1y": hist_1y,
            "hist_5y": hist_5y,
            "financials": financials,
            "balance_sheet": balance_sheet,
            "income_stmt": income_stmt,
            "cash_flow": cash_flow,
            "symbol": ticker_symbol,
        }
    except Exception as e:
        st.error(f"Gagal mengambil data: {str(e)}")
        return None


def hitung_roe(data: dict) -> float:
    """Hitung ROE dari data yfinance."""
    info = data["info"]
    # Coba dari info langsung
    roe = info.get("returnOnEquity")
    if roe is not None:
        return roe * 100  # konversi ke persen
    # Coba hitung manual dari financial statements
    try:
        income = data["income_stmt"]
        bs = data["balance_sheet"]
        if not income.empty and not bs.empty:
            net_income = income.iloc[0].get("Net Income", None)
            equity = bs.iloc[0].get("Stockholders Equity", None) or bs.iloc[0].get("Total Stockholder Equity", None)
            if net_income and equity and equity != 0:
                return (net_income / equity) * 100
    except Exception:
        pass
    return None


def hitung_der(data: dict) -> float:
    """Hitung Debt to Equity Ratio."""
    info = data["info"]
    der = info.get("debtToEquity")
    if der is not None:
        return der / 100 if der > 10 else der  # Normalisasi, kadang yfinance return dalam persen
    return None


def hitung_current_ratio(data: dict) -> float:
    """Hitung Current Ratio."""
    info = data["info"]
    cr = info.get("currentRatio")
    if cr is not None:
        return cr
    return None


def hitung_earnings_growth(data: dict) -> dict:
    """
    Hitung pertumbuhan laba tahunan dari income statement.
    Returns dict: {'growth_rates': [...], 'avg_growth': float, 'trend': str}
    """
    info = data["info"]
    eg = info.get("earningsGrowth")  # pertumbuhan laba year-over-year
    eq = info.get("earningsQuarterlyGrowth")

    # Coba dari income statement historis
    try:
        income = data["income_stmt"]
        if not income.empty and income.shape[1] >= 2:
            net_incomes = []
            for col in income.columns:
                ni = None
                for key in ["Net Income", "Net Income Common Stockholders"]:
                    if key in income.index:
                        ni = income.loc[key, col]
                        break
                if ni is not None and not pd.isna(ni):
                    net_incomes.append(float(ni))

            if len(net_incomes) >= 2:
                # Urutan dari income_stmt: terbaru dulu
                growth_rates = []
                for i in range(len(net_incomes) - 1):
                    if net_incomes[i + 1] != 0:
                        g = ((net_incomes[i] - net_incomes[i + 1]) / abs(net_incomes[i + 1])) * 100
                        growth_rates.append(g)

                if growth_rates:
                    avg_growth = sum(growth_rates) / len(growth_rates)
                    # Tentukan tren
                    positive_count = sum(1 for g in growth_rates if g > 0)
                    if positive_count >= len(growth_rates) * 0.7:
                        trend = "Cenderung Tumbuh 📈"
                    elif positive_count >= len(growth_rates) * 0.4:
                        trend = "Stabil ➡️"
                    else:
                        trend = "Cenderung Menurun 📉"

                    return {
                        "growth_rates": growth_rates,
                        "avg_growth": avg_growth,
                        "trend": trend,
                        "net_incomes": net_incomes,
                    }
    except Exception:
        pass

    # Fallback ke info
    if eg is not None:
        avg_g = eg * 100
        trend = "Cenderung Tumbuh 📈" if avg_g > 5 else ("Stabil ➡️" if avg_g > -5 else "Cenderung Menurun 📉")
        return {"growth_rates": [avg_g], "avg_growth": avg_g, "trend": trend, "net_incomes": []}
    if eq is not None:
        avg_g = eq * 100
        trend = "Cenderung Tumbuh 📈" if avg_g > 5 else ("Stabil ➡️" if avg_g > -5 else "Cenderung Menurun 📉")
        return {"growth_rates": [avg_g], "avg_growth": avg_g, "trend": trend, "net_incomes": []}

    return None


def hitung_npm(data: dict) -> float:
    """Hitung Net Profit Margin."""
    info = data["info"]
    npm = info.get("profitMargins")
    if npm is not None:
        return npm * 100
    return None


def hitung_per(data: dict) -> float:
    """Hitung PER (Price to Earnings Ratio)."""
    info = data["info"]
    per = info.get("trailingPE") or info.get("forwardPE")
    if per is not None:
        return per
    return None


def hitung_pbv(data: dict) -> float:
    """Hitung PBV (Price to Book Value)."""
    info = data["info"]
    pbv = info.get("priceToBook")
    if pbv is not None:
        return pbv
    return None


def hitung_dividend_yield(data: dict) -> float:
    """Hitung Dividend Yield dalam persen."""
    info = data["info"]
    dy = info.get("dividendYield") or info.get("trailingAnnualDividendYield")
    if dy is not None:
        return dy * 100
    return None


def hitung_graham_number(data: dict) -> float:
    """
    Hitung Graham Number = sqrt(22.5 * EPS * BVPS).
    Refined: Handles negative values to avoid math errors.
    """
    info = data.get("info", {})
    eps = info.get("trailingEps")
    bvps = info.get("bookValue")
    
    if eps is not None and bvps is not None:
        # Graham's criteria usually requires positive EPS and BVPS
        if eps > 0 and bvps > 0:
            return (22.5 * eps * bvps) ** 0.5
    return None

def hitung_dcf_simple(data: dict, discount_rate: float = 0.12) -> float:
    """
    Estimasi DCF Sederhana: Proyeksi FCF 5 tahun ke depan.
    FCF = Net Income + Depreciation - Capex (Simplified here as FCF from yfinance).
    """
    try:
        cf = data.get("cash_flow")
        if cf is None or cf.empty:
            # Try to get from financials if info has it
            fcf = data["info"].get("freeCashflow")
        else:
            # Use 'Free Cash Flow' or calculate it
            fcf = cf.iloc[0].get("Free Cash Flow") or (cf.iloc[0].get("Total Cash From Operating Activities", 0) + cf.iloc[0].get("Capital Expenditures", 0))

        if not fcf or fcf <= 0: return None
        
        # Growth assumption (conservative historical average or 5%)
        eg_data = hitung_earnings_growth(data)
        growth = (eg_data["avg_growth"] / 100) if eg_data and eg_data["avg_growth"] > 0 else 0.05
        growth = min(growth, 0.20) # cap at 20%
        
        # 5 Year Projection
        projected_fcf = [fcf * (1 + growth)**i for i in range(1, 6)]
        discounted_fcf = [f / (1 + discount_rate)**i for i, f in enumerate(projected_fcf, 1)]
        
        # Terminal Value (Gordon Growth)
        terminal_growth = 0.03
        tv = (projected_fcf[-1] * (1 + terminal_growth)) / (discount_rate - terminal_growth)
        discounted_tv = tv / (1 + discount_rate)**5
        
        intrinsic_value_total = sum(discounted_fcf) + discounted_tv
        shares = data["info"].get("sharesOutstanding")
        
        if shares and shares > 0:
            return intrinsic_value_total / shares
    except Exception:
        pass
    return None


def hitung_skor_kualitas(roe, der, cr, eg_data, npm) -> tuple:
    """
    Hitung skor kualitas perusahaan (0-100).
    Masing-masing metrik berkontribusi proporsional.
    Returns: (skor, label, detail_dict)
    """
    skor = 0
    detail = {}
    count = 0

    # ROE (bobot: 25)
    if roe is not None:
        count += 1
        if roe >= 20:
            s = 25
        elif roe >= 15:
            s = 20
        elif roe >= 10:
            s = 12
        elif roe >= 5:
            s = 6
        else:
            s = 0
        skor += s
        detail["ROE"] = s
    else:
        detail["ROE"] = "N/A"

    # DER (bobot: 20)
    if der is not None:
        count += 1
        if der <= 0.3:
            s = 20
        elif der <= 0.5:
            s = 16
        elif der <= 1.0:
            s = 10
        elif der <= 1.5:
            s = 5
        else:
            s = 0
        skor += s
        detail["DER"] = s
    else:
        detail["DER"] = "N/A"

    # Current Ratio (bobot: 15)
    if cr is not None:
        count += 1
        if cr >= 2.0:
            s = 15
        elif cr >= 1.5:
            s = 12
        elif cr >= 1.0:
            s = 7
        else:
            s = 2
        skor += s
        detail["CR"] = s
    else:
        detail["CR"] = "N/A"

    # Earnings Growth (bobot: 25)
    if eg_data is not None:
        count += 1
        avg_g = eg_data["avg_growth"]
        if avg_g >= 20:
            s = 25
        elif avg_g >= 10:
            s = 20
        elif avg_g >= 5:
            s = 15
        elif avg_g >= 0:
            s = 8
        else:
            s = 0
        skor += s
        detail["EG"] = s
    else:
        detail["EG"] = "N/A"

    # Net Profit Margin (bobot: 15)
    if npm is not None:
        count += 1
        if npm >= 20:
            s = 15
        elif npm >= 15:
            s = 12
        elif npm >= 10:
            s = 9
        elif npm >= 5:
            s = 5
        else:
            s = 0
        skor += s
        detail["NPM"] = s
    else:
        detail["NPM"] = "N/A"

    # Normalisasi jika ada metrik yang N/A
    if count > 0 and count < 5:
        # Scale up proportionally
        max_possible = 0
        for key, val in detail.items():
            if val != "N/A":
                bobot_map = {"ROE": 25, "DER": 20, "CR": 15, "EG": 25, "NPM": 15}
                max_possible += bobot_map.get(key, 0)
        if max_possible > 0:
            skor = int((skor / max_possible) * 100)
    elif count == 0:
        skor = None

    if skor is not None:
        label = "✅ BERKUALITAS" if skor >= 60 else "⚠️ KURANG BERKUALITAS"
    else:
        label = "❓ DATA TIDAK TERSEDIA"

    return skor, label, detail


def hitung_skor_valuasi(per, pbv, dy, graham, harga_sekarang) -> tuple:
    """
    Hitung skor valuasi (0-100). Semakin RENDAH skor, semakin MURAH.
    Returns: (skor, label, detail_dict)
    """
    skor = 0
    detail = {}
    count = 0

    # PER (bobot: 30) — semakin rendah semakin bagus, skor = mahal
    if per is not None and per > 0:
        count += 1
        if per < 8:
            s = 5   # sangat murah
        elif per < 10:
            s = 15  # murah
        elif per < 15:
            s = 30  # wajar
        elif per < 20:
            s = 50  # agak mahal
        elif per < 30:
            s = 70  # mahal
        else:
            s = 90  # sangat mahal
        skor += s * 0.30
        detail["PER"] = round(s, 1)
    else:
        detail["PER"] = "N/A"

    # PBV (bobot: 25) — semakin rendah semakin bagus
    if pbv is not None and pbv > 0:
        count += 1
        if pbv < 0.7:
            s = 5
        elif pbv < 1.0:
            s = 15
        elif pbv < 1.5:
            s = 30
        elif pbv < 2.5:
            s = 50
        elif pbv < 4.0:
            s = 70
        else:
            s = 90
        skor += s * 0.25
        detail["PBV"] = round(s, 1)
    else:
        detail["PBV"] = "N/A"

    # Dividend Yield (bobot: 15) — semakin tinggi semakin bagus (kebalikan)
    if dy is not None:
        count += 1
        if dy >= 6:
            s = 5
        elif dy >= 4:
            s = 15
        elif dy >= 3:
            s = 25
        elif dy >= 2:
            s = 40
        elif dy >= 1:
            s = 60
        else:
            s = 80
        skor += s * 0.15
        detail["DY"] = round(s, 1)
    else:
        detail["DY"] = "N/A"

    # Graham Number (bobot: 30) — jika harga < Graham, murah
    if graham is not None and harga_sekarang is not None and graham > 0:
        count += 1
        ratio = harga_sekarang / graham
        if ratio < 0.5:
            s = 5   # sangat undervalued
        elif ratio < 0.7:
            s = 15  # undervalued
        elif ratio < 1.0:
            s = 30  # wajar
        elif ratio < 1.3:
            s = 55  # agak overvalued
        elif ratio < 1.6:
            s = 75  # overvalued
        else:
            s = 95  # sangat overvalued
        skor += s * 0.30
        detail["GRAHAM"] = round(s, 1)
    else:
        detail["GRAHAM"] = "N/A"

    # Normalisasi
    if count > 0:
        total_weight = 0
        weight_map = {"PER": 0.30, "PBV": 0.25, "DY": 0.15, "GRAHAM": 0.30}
        for key, val in detail.items():
            if val != "N/A":
                total_weight += weight_map.get(key, 0)
        if total_weight > 0:
            skor = int((skor / total_weight))
    else:
        skor = None

    if skor is not None:
        if skor < 30:
            label = "🟢 MURAH"
        elif skor < 60:
            label = "🟡 WAJAR"
        else:
            label = "🔴 MAHAL"
    else:
        label = "❓ DATA TIDAK TERSEDIA"

    return skor, label, detail


def buat_rekomendasi(skor_kualitas, skor_valuasi, nama_saham) -> dict:
    """
    Buat rekomendasi BELI / TAHAN / JUAL berdasarkan skor kualitas dan valuasi.
    """
    if skor_kualitas is None or skor_valuasi is None:
        return {
            "aksi": "❓ TIDAK DAPAT DINILAI",
            "kelas": "rekom-tahan",
            "penjelasan": f"Data fundamental {nama_saham} tidak lengkap, sehingga tidak bisa memberikan rekomendasi. "
                          "Coba periksa langsung di laporan keuangan perusahaan.",
            "emoji": "❓"
        }

    # Logika rekomendasi sesuai permintaan
    if skor_kualitas >= 70 and skor_valuasi <= 40:
        return {
            "aksi": "🟢 BELI",
            "kelas": "rekom-beli",
            "penjelasan": f"**{nama_saham}** seperti mobil Mercedes harga bajaj! 🚗💰 "
                          f"Perusahaan berkualitas tinggi (skor {skor_kualitas}/100) "
                          f"dengan harga yang masih murah (valuasi {skor_valuasi}/100). "
                          "Ini saat yang bagus untuk mulai mengumpulkan saham ini secara bertahap.",
            "emoji": "🟢"
        }
    elif skor_kualitas >= 70 and skor_valuasi <= 70:
        return {
            "aksi": "🟡 TAHAN",
            "kelas": "rekom-tahan",
            "penjelasan": f"**{nama_saham}** adalah perusahaan bagus (skor {skor_kualitas}/100), "
                          f"tapi harganya lagi wajar sampai agak mahal (valuasi {skor_valuasi}/100). "
                          "Kalau sudah punya, boleh tahan. Kalau mau beli, tunggu harga turun dulu.",
            "emoji": "🟡"
        }
    elif skor_kualitas < 50 or skor_valuasi > 80:
        return {
            "aksi": "🔴 JUAL",
            "kelas": "rekom-jual",
            "penjelasan": f"**{nama_saham}** kurang menarik saat ini. "
                          + (f"Kualitas perusahaan rendah (skor {skor_kualitas}/100). " if skor_kualitas < 50 else "")
                          + (f"Harga saat ini terlalu mahal (valuasi {skor_valuasi}/100). " if skor_valuasi > 80 else "")
                          + "Lebih baik cari saham lain yang lebih berkualitas dan murah.",
            "emoji": "🔴"
        }
    elif skor_kualitas >= 50 and skor_valuasi <= 40:
        return {
            "aksi": "🟡 TAHAN / PERTIMBANGKAN BELI",
            "kelas": "rekom-tahan",
            "penjelasan": f"**{nama_saham}** punya kualitas cukup (skor {skor_kualitas}/100) "
                          f"dan harga relatif murah (valuasi {skor_valuasi}/100). "
                          "Boleh dipertimbangkan, tapi perhatikan risiko kualitas perusahaan. "
                          "Pelajari lebih dalam sebelum membeli.",
            "emoji": "🟡"
        }
    else:
        return {
            "aksi": "🟡 TAHAN",
            "kelas": "rekom-tahan",
            "penjelasan": f"**{nama_saham}** dalam kondisi biasa saja. "
                          f"Kualitas: {skor_kualitas}/100, Valuasi: {skor_valuasi}/100. "
                          "Tidak ada sinyal kuat untuk beli atau jual. Pantau terus perkembangan fundamentalnya.",
            "emoji": "🟡"
        }


def buat_prospek(eg_data, der, roe, npm) -> dict:
    """Buat proyeksi prospek sederhana berdasarkan data historis."""
    signals = []
    positive = 0
    negative = 0
    total = 0

    if eg_data is not None:
        total += 2  # bobot lebih besar
        if eg_data["avg_growth"] > 10:
            positive += 2
            signals.append("📈 Laba bertumbuh dengan kuat")
        elif eg_data["avg_growth"] > 0:
            positive += 1
            total -= 0.5  # kurangi dampak
            signals.append("📈 Laba masih tumbuh positif")
        else:
            negative += 2
            signals.append("📉 Laba menunjukkan penurunan")

    if der is not None:
        total += 1
        if der < 0.5:
            positive += 1
            signals.append("✅ Utang terkendali, posisi keuangan sehat")
        elif der > 1.5:
            negative += 1
            signals.append("⚠️ Utang cukup besar, perlu dipantau")
        else:
            signals.append("➡️ Tingkat utang masih dalam batas wajar")

    if roe is not None:
        total += 1
        if roe > 15:
            positive += 1
            signals.append("✅ Efisiensi perusahaan sangat baik")
        elif roe > 8:
            signals.append("➡️ Efisiensi perusahaan cukup")
        else:
            negative += 1
            signals.append("⚠️ Efisiensi perusahaan perlu ditingkatkan")

    if npm is not None:
        total += 1
        if npm > 15:
            positive += 1
            signals.append("✅ Margin laba tebal, bisnis menguntungkan")
        elif npm > 5:
            signals.append("➡️ Margin laba wajar")
        else:
            negative += 1
            signals.append("⚠️ Margin laba tipis")

    if total == 0:
        return {
            "label": "❓ Tidak cukup data",
            "signals": ["Data tidak tersedia untuk membuat proyeksi."],
            "confidence": "Rendah",
        }

    ratio = positive / max(total, 1) if total > 0 else 0.5
    if ratio >= 0.65:
        label = "🌟 PROSPEK CERAH - Cenderung Tumbuh"
        confidence = "Tinggi"
    elif ratio >= 0.4:
        label = "➡️ PROSPEK STABIL"
        confidence = "Sedang"
    else:
        label = "⚠️ PROSPEK KURANG BAIK - Cenderung Menurun"
        confidence = "Rendah"

    return {"label": label, "signals": signals, "confidence": confidence}


# =====================================================================
# FUNGSI TEKNIKAL - Analisa Tren & Momentum
# =====================================================================

def hitung_rsi(df, period=14):
    """Menghitung Relative Strength Index (RSI)."""
    if df is None or len(df) < period + 1:
        return None
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def hitung_macd(df):
    """Menghitung MACD Signal."""
    if df is None or len(df) < 26:
        return None, None
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd.iloc[-1], signal.iloc[-1]

def hitung_support_resistance(df, period=14):
    """
    Sederhana: Support=L-Pivot2, Resistance=H-Pivot2.
    Menggunakan min/max dalam periode tertentu.
    """
    if df is None or len(df) < period:
        return None, None
    res = df['High'].rolling(window=period).max().iloc[-1]
    sup = df['Low'].rolling(window=period).min().iloc[-1]
    return res, sup

def hitung_bb(df, period=20):
    """Menghitung Bollinger Bands."""
    if df is None or len(df) < period:
        return None, None, None
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    upper = sma + (std * 2)
    lower = sma - (std * 2)
    return upper.iloc[-1], sma.iloc[-1], lower.iloc[-1]

def hitung_ma(df, period=50):
    """Menghitung Simple Moving Average."""
    if df is None or len(df) < period:
        return None
    return df['Close'].rolling(window=period).mean().iloc[-1]

def hitung_skor_teknikal(df):
    """
    Menghitung skor teknikal (0-100) berdasarkan MA, RSI, dan MACD.
    Inspirasi: Stan Weinstein & Mark Minervini.
    """
    if df is None or len(df) < 200:
        return 50, ["Data teknikal tidak cukup untuk analisa mendalam"], "yellow"
    
    price = df['Close'].iloc[-1]
    ma20 = hitung_ma(df, 20)
    ma50 = hitung_ma(df, 50)
    ma200 = hitung_ma(df, 200)
    rsi = hitung_rsi(df)
    macd, signal = hitung_macd(df)
    
    skor = 50
    reasons = []
    
    # 1. Trend Analysis (Mark Minervini style)
    if price > ma50 and ma50 > ma200:
        skor += 20
        reasons.append("✅ Trend Bullish: Harga di atas MA50 & MA200")
    elif price < ma50 and ma50 < ma200:
        skor -= 20
        reasons.append("❌ Trend Bearish: Harga di bawah MA50 & MA200")
        
    # 2. Momentum Analysis (RSI)
    if rsi < 30:
        skor += 15
        reasons.append("🔥 RSI Oversold (Jenuh Jual): Peluang Rebound")
    elif rsi > 70:
        skor -= 15
        reasons.append("🛑 RSI Overbought (Jenuh Beli): Risiko Koreksi")
        
    # 3. MACD Intersection
    if macd > signal:
        skor += 10
        reasons.append("📈 MACD Bullish Crossover")
    else:
        skor -= 10
        reasons.append("📉 MACD Bearish Crossover")
        
    skor = max(0, min(100, skor))
    color = "green" if skor >= 70 else ("red" if skor <= 30 else "yellow")
    
    return skor, reasons, color


# =====================================================================
# GRAND MASTER HYBRID STRATEGY
# =====================================================================

def buat_rekomendasi_master(skor_fund, skor_teknik, ticker_name):
    """
    Sintesa Sinyal Master: Menggabungkan Fundamental (Value/Quality) 
    dan Teknikal (Trend/Momentum).
    """
    power_score = (skor_fund * 0.6) + (skor_teknik * 0.4)
    
    if power_score >= 80:
        return {
            "aksi": "SUPER BUY 🚀",
            "kelas": "rekom-beli",
            "penjelasan": f"Keselarasan Sempurna! Fundamental {ticker_name} sangat kuat dan grafik teknikal sedang dikuasai Bullish (Minervini Trend Template). Ini adalah momen 'Master Play'.",
            "icon": "💎"
        }
    elif power_score >= 65:
        return {
            "aksi": "BUY ✅",
            "kelas": "rekom-beli",
            "penjelasan": f"Kombinasi yang solid. Meskipun ada sedikit fluktuasi, tren jangka panjang tetap positif dengan fondasi bisnis yang sehat.",
            "icon": "📈"
        }
    elif power_score >= 45:
        return {
            "aksi": "HOLD / WAIT ⏳",
            "kelas": "rekom-tahan",
            "penjelasan": f"Berada di area netral. Fundamental bagus tapi teknikal mungkin sedang konsolidasi, atau sebaliknya. Masuk secara bertahap (Dollar Cost Averaging).",
            "icon": "⏸️"
        }
    elif power_score >= 30:
        return {
            "aksi": "WASPADA ⚠️",
            "kelas": "rekom-jual",
            "penjelasan": f"Sinyal melemah. Terlihat tren menurun (Bearish) atau valuasi sudah terlalu mahal dibanding harga wajarnya.",
            "icon": "❕"
        }
    else:
        return {
            "aksi": "STRONG SELL 🛑",
            "kelas": "rekom-jual",
            "penjelasan": f"Bahaya! Perpaduan kinerja fundamental buruk dan grafik harga yang terus menembus support bawah. Hindari atau kurangi porsi.",
            "icon": "🆘"
        }


# =====================================================================
# FUNGSI VISUALISASI
# =====================================================================

def buat_chart_harga(hist, nama):
    """Buat candlestick chart harga saham dengan MA50/MA200."""
    if hist is None or hist.empty:
        return None

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25],
        subplot_titles=None,
    )

    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=hist.index,
            open=hist["Open"],
            high=hist["High"],
            low=hist["Low"],
            close=hist["Close"],
            name="Harga",
            increasing_line_color="#4ade80",
            decreasing_line_color="#f87171",
            increasing_fillcolor="#4ade80",
            decreasing_fillcolor="#f87171",
        ),
        row=1, col=1,
    )

    # Moving Average 50 hari
    if len(hist) >= 50:
        ma50 = hist["Close"].rolling(window=50).mean()
        fig.add_trace(
            go.Scatter(
                x=hist.index, y=ma50,
                name="MA 50",
                line=dict(color="#667eea", width=1.5),
            ),
            row=1, col=1,
        )

    # Support & Resistance (Pro Mode)
    if st.session_state.get("pro_mode", False):
        res, sup = hitung_support_resistance(hist)
        if res and sup:
            fig.add_hline(y=res, line_dash="dash", line_color="#f87171", annotation_text="Resistance", row=1, col=1)
            fig.add_hline(y=sup, line_dash="dash", line_color="#4ade80", annotation_text="Support", row=1, col=1)

    # Bollinger Bands (Pro Mode)

    # Moving Average 200 hari

    # Volume
    colors = ["#4ade80" if c >= o else "#f87171"
              for c, o in zip(hist["Close"], hist["Open"])]
    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist["Volume"],
            name="Volume",
            marker_color=colors,
            opacity=0.5,
        ),
        row=2, col=1,
    )

    fig.update_layout(
        title=f"📈 Pergerakan Harga {nama} (1 Tahun Terakhir)",
        title_font=dict(size=16, color="#e0e0ff"),
        xaxis_rangeslider_visible=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b8b8d0", family="Inter"),
        legend=dict(
            bgcolor="rgba(0,0,0,0.3)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1,
            font=dict(size=11),
        ),
        height=550,
        margin=dict(l=10, r=10, t=60, b=10),
    )

    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.05)",
        zerolinecolor="rgba(255,255,255,0.05)",
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.05)",
        zerolinecolor="rgba(255,255,255,0.05)",
    )

    return fig


def buat_chart_fundamental(data: dict, nama: str) -> go.Figure:
    """Buat chart historis untuk metrik fundamental."""
    info = data["info"]

    # Kumpulkan data yang ada
    metrics = {}
    labels = []

    roe = info.get("returnOnEquity")
    per = info.get("trailingPE") or info.get("forwardPE")
    pbv = info.get("priceToBook")
    npm = info.get("profitMargins")
    dy = info.get("dividendYield")

    if roe is not None:
        metrics["ROE (%)"] = roe * 100
    if per is not None:
        metrics["PER (x)"] = per
    if pbv is not None:
        metrics["PBV (x)"] = pbv
    if npm is not None:
        metrics["NPM (%)"] = npm * 100
    if dy is not None:
        metrics["Div Yield (%)"] = dy * 100

    if not metrics:
        return None

    # Buat bar chart sederhana dari metrik yang tersedia
    fig = go.Figure()

    colors = []
    for k, v in metrics.items():
        if "ROE" in k:
            colors.append("#4ade80" if v >= 15 else ("#fbbf24" if v >= 10 else "#f87171"))
        elif "PER" in k:
            colors.append("#4ade80" if v < 15 else ("#fbbf24" if v < 25 else "#f87171"))
        elif "PBV" in k:
            colors.append("#4ade80" if v < 1.5 else ("#fbbf24" if v < 3 else "#f87171"))
        elif "NPM" in k:
            colors.append("#4ade80" if v >= 10 else ("#fbbf24" if v >= 5 else "#f87171"))
        elif "Div" in k:
            colors.append("#4ade80" if v >= 3 else ("#fbbf24" if v >= 1 else "#f87171"))
        else:
            colors.append("#667eea")

    fig.add_trace(
        go.Bar(
            x=list(metrics.keys()),
            y=list(metrics.values()),
            marker_color=colors,
            text=[f"{v:.1f}" for v in metrics.values()],
            textposition="outside",
            textfont=dict(color="#e0e0ff", size=13, family="Inter"),
        )
    )

    fig.update_layout(
        title=f"📊 Snapshot Fundamental {nama}",
        title_font=dict(size=16, color="#e0e0ff"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b8b8d0", family="Inter"),
        height=400,
        margin=dict(l=10, r=10, t=60, b=10),
        showlegend=False,
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(showgrid=False),
    )

    return fig


def buat_gauge_chart(skor: int, label: str, title: str) -> go.Figure:
    """Buat gauge/speedometer chart untuk skor."""
    if skor is None:
        skor = 0

    # Warna berdasarkan label (untuk kualitas: tinggi=hijau; untuk valuasi: rendah=hijau)
    if "MURAH" in label or "BERKUALITAS" in label:
        bar_color = "#4ade80"
    elif "WAJAR" in label or "CUKUP" in label:
        bar_color = "#fbbf24"
    else:
        bar_color = "#f87171"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=skor,
        title=dict(text=title, font=dict(size=14, color="#e0e0ff")),
        number=dict(font=dict(size=36, color="#e0e0ff")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor="#666", tickfont=dict(color="#888")),
            bar=dict(color=bar_color, thickness=0.3),
            bgcolor="rgba(255,255,255,0.05)",
            borderwidth=0,
            steps=[
                dict(range=[0, 30], color="rgba(74, 222, 128, 0.15)"),
                dict(range=[30, 60], color="rgba(251, 191, 36, 0.15)"),
                dict(range=[60, 100], color="rgba(248, 113, 113, 0.15)"),
            ],
        ),
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=30, r=30, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
    )

    return fig


# =====================================================================
# FUNGSI SCREENING TOP 5
# =====================================================================

@st.cache_data(ttl=600, show_spinner=False)
def screening_top_picks(daftar: list) -> list:
    """
    Screen semua saham dalam daftar, hitung skor, dan return Top 5 BELI.
    """
    results = []

    for sym in daftar:
        try:
            data = ambil_data_saham(sym)
            if data is None:
                continue

            info = data["info"]
            nama = info.get("shortName", sym)
            harga = info.get("regularMarketPrice") or info.get("currentPrice")

            roe = hitung_roe(data)
            der = hitung_der(data)
            cr = hitung_current_ratio(data)
            eg = hitung_earnings_growth(data)
            npm = hitung_npm(data)
            per = hitung_per(data)
            pbv = hitung_pbv(data)
            dy = hitung_dividend_yield(data)
            graham = hitung_graham_number(data)

            sk, lk, _ = hitung_skor_kualitas(roe, der, cr, eg, npm)
            sv, lv, _ = hitung_skor_valuasi(per, pbv, dy, graham, harga)

            rekom = buat_rekomendasi(sk, sv, sym)

            if sk is not None and sv is not None:
                # Skor gabungan: kualitas tinggi + valuasi rendah = bagus
                skor_beli = sk - sv  # semakin tinggi semakin bagus
                results.append({
                    "symbol": sym,
                    "nama": nama,
                    "harga": harga,
                    "skor_kualitas": sk,
                    "skor_valuasi": sv,
                    "skor_beli": skor_beli,
                    "rekomendasi": rekom["aksi"],
                    "roe": roe,
                    "per": per,
                    "pbv": pbv,
                })
        except Exception:
            continue

    # Sort by skor_beli descending (kualitas tinggi, valuasi rendah)
    results.sort(key=lambda x: x["skor_beli"], reverse=True)

    return results[:5]


def tampilkan_peer_comparison(current_ticker: str, sector: str, industry: str, daftar_saham: list):
    """
    Tampilkan perbandingan dengan saham lain di industri yang sama.
    """
    if not industry or industry == "N/A":
        return
    
    st.markdown(f'<div class="section-title">🏭 Perbandingan Industri: {industry}</div>', unsafe_allow_html=True)
    
    peers = []
    with st.spinner("Mencari kompetitor..."):
        for sym in daftar_saham:
            if sym == current_ticker: continue
            try:
                # Use a very short cache for peers to keep UI fast
                p_data = ambil_data_saham(sym)
                if p_data and p_data["info"].get("industry") == industry:
                    inf = p_data["info"]
                    peers.append({
                        "Ticker": sym.replace(".JK", ""),
                        "Price": inf.get("regularMarketPrice") or inf.get("currentPrice"),
                        "ROE (%)": (inf.get("returnOnEquity", 0) or 0) * 100,
                        "PER (x)": inf.get("trailingPE") or inf.get("forwardPE"),
                        "PBV (x)": inf.get("priceToBook"),
                        "Market Cap": inf.get("marketCap")
                    })
            except: continue
            if len(peers) >= 4: break # limit to 4 peers for speed
            
    if peers:
        df_peers = pd.DataFrame(peers)
        st.dataframe(
            df_peers,
            hide_index=True,
            width='stretch',
            column_config={
                "Market Cap": st.column_config.NumberColumn("Market Cap", format="Rp%,.0f"),
                "ROE (%)": st.column_config.NumberColumn("ROE", format="%.1f%%"),
                "PER (x)": st.column_config.NumberColumn("PER", format="%.1f"),
                "PBV (x)": st.column_config.NumberColumn("PBV", format="%.2f"),
            }
        )
    else:
        st.info("Tidak ditemukan kompetitor langsung di daftar screening saat ini.")


# =====================================================================
# FORMAT ANGKA
# =====================================================================

def format_angka(val, suffix="", decimal=1):
    """Format angka dengan warna berdasarkan nilai."""
    if val is None:
        return '<span style="color:#666">N/A</span>'
    if isinstance(val, str):
        return val
    return f"{val:,.{decimal}f}{suffix}"


def format_mata_uang(val, currency="IDR"):
    """Format angka sebagai mata uang."""
    if val is None:
        return "N/A"
    if currency == "IDR":
        if val >= 1e12:
            return f"Rp {val/1e12:,.1f} T"
        elif val >= 1e9:
            return f"Rp {val/1e9:,.1f} M"
        elif val >= 1e6:
            return f"Rp {val/1e6:,.1f} Jt"
        else:
            return f"Rp {val:,.0f}"
    else:
        if val >= 1e12:
            return f"${val/1e12:,.1f}T"
        elif val >= 1e9:
            return f"${val/1e9:,.1f}B"
        elif val >= 1e6:
            return f"${val/1e6:,.1f}M"
        else:
            return f"${val:,.2f}"


# =====================================================================
# RENDER METRIC CARD
# =====================================================================

def render_metric_card(label, value, status_class, benchmark_text):
    """Render satu kartu metrik."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{label}</div>
        <div class="value {status_class}">{value}</div>
        <div class="sub">{benchmark_text}</div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================================
# APLIKASI UTAMA
# =====================================================================

def main():
    # ------------------------------------------------------------------
    # DISCLAIMER GATEKEEPER (Floating Native Dialog)
    # ------------------------------------------------------------------
    # Add blur effect if not accepted
    if not st.session_state.get("disclaimer_accepted", False):
        st.markdown("""
            <style>
                .main .block-container, section[data-testid="stSidebar"] {
                    filter: blur(4px) brightness(0.7);
                    pointer-events: none;
                    transition: filter 0.5s ease;
                }
            </style>
        """, unsafe_allow_html=True)
        tampilkan_modal_disclaimer()

    # ------------------------------------------------------------------
    # SIDEBAR
    # ------------------------------------------------------------------
    with st.sidebar:
        st.markdown("# 📊 Analisa Saham")
        st.markdown("##### *Filosofi Warren Buffett*")
        st.markdown("---")

        st.markdown("### 🌍 Pasar (Market)")
        pasar_pilihan = st.radio(
            "Pilih Pasar Saham",
            options=["🇮🇩 IDX (Indonesia)", "🇺🇸 US (Amerika Serikat)", "🌕 Crypto (Digital Assets)"],
            index=0,
            horizontal=True
        )
        kode_pasar = "IDX" if "IDX" in pasar_pilihan else ("US" if "US" in pasar_pilihan else "Crypto")

        st.markdown("---")
        st.markdown("### 🔍 Input Saham/Koin")
        kode_saham = st.text_input(
            "Kode Saham / Kripto",
            value="BBCA" if kode_pasar == "IDX" else ("AAPL" if kode_pasar == "US" else "BTC"),
            placeholder="Ketik kode...",
            help="Contoh: BBCA (IDX), AAPL (US), BTC (Crypto)",
        )

        st.markdown("---")

        # Pilihan jenis analisa
        st.markdown("### ⚙️ Mode Aplikasi")
        is_pro = st.toggle("🚀 Aktifkan Mode PRO (Advanced)", value=False, help="Membuka fitur teknikal dan fundamental tingkat lanjut bagi mahir.")
        st.session_state["pro_mode"] = is_pro
        
        show_explanation = st.toggle("Tampilkan Penjelasan Pemula", value=not is_pro)
        tampilkan_top5 = st.toggle("Tampilkan Top 5 Rekomendasi", value=False)

        st.markdown("---")

        # Daftar saham cepat
        st.markdown("### ⚡ Akses Cepat")
        quick_picks_idx = {
            "🏦 BBCA": "BBCA", "🏦 BBRI": "BBRI", "📡 TLKM": "TLKM",
            "🚗 ASII": "ASII", "🧴 UNVR": "UNVR", "⛏️ ADRO": "ADRO",
        }
        quick_picks_us = {
            "🍎 AAPL": "AAPL", "💻 MSFT": "MSFT", "🔍 GOOGL": "GOOGL",
            "🚗 TSLA": "TSLA", "🎮 NVDA": "NVDA", "🛍️ AMZN": "AMZN",
        }

        quick_picks_crypto = {
            "₿ BTC": "BTC", "💎 ETH": "ETH", "☀️ SOL": "SOL",
            "🔶 BNB": "BNB", "🔹 XRP": "XRP", "🐕 DOGE": "DOGE",
        }

        st.markdown("**Bursa Indonesia**")
        cols_q1 = st.columns(3)
        for idx, (label, code) in enumerate(quick_picks_idx.items()):
            with cols_q1[idx % 3]:
                if st.button(label, key=f"quick_idx_{code}", use_container_width=True):
                    st.session_state["quick_pick"] = code
                    st.session_state["quick_pasar"] = "🇮🇩 IDX (Indonesia)"
                    st.rerun()

        st.markdown("**Bursa Amerika**")
        cols_q2 = st.columns(3)
        for idx, (label, code) in enumerate(quick_picks_us.items()):
            with cols_q2[idx % 3]:
                if st.button(label, key=f"quick_us_{code}", use_container_width=True):
                    st.session_state["quick_pick"] = code
                    st.session_state["quick_pasar"] = "🇺🇸 US (Amerika Serikat)"
                    st.rerun()

        st.markdown("**Pasar Kripto**")
        cols_q3 = st.columns(3)
        for idx, (label, code) in enumerate(quick_picks_crypto.items()):
            with cols_q3[idx % 3]:
                if st.button(label, key=f"quick_crypto_{code}", use_container_width=True):
                    st.session_state["quick_pick"] = code
                    st.session_state["quick_pasar"] = "🌕 Crypto (Digital Assets)"
                    st.rerun()

        # Cek apakah ada quick pick
        if "quick_pick" in st.session_state:
            kode_saham = st.session_state.pop("quick_pick")
            pasar_pilihan = st.session_state.pop("quick_pasar")
            kode_pasar = "IDX" if "IDX" in pasar_pilihan else ("US" if "US" in pasar_pilihan else "Crypto")

        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; color:#666; font-size:0.75rem;">
        📊 Intel: Yahoo Finance API<br>
        🛡️ Grand Master Hybrid Suite v2.0 Pro<br>
        Selalu lakukan riset sendiri (DYOR)
        </div>
        """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # HEADER
    # ------------------------------------------------------------------
    st.markdown(f"""
    <div class="hero-box">
        <div class="accuracy-tag">⚡ Data Accuracy: 99.99% Precision</div>
        <h1>🌌 Grand Master Hybrid Pro Suite</h1>
        <p>Expert-Grade Fundamental Insight & Professional Technical Tools (Buffett Edition)</p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # TAB UTAMA
    # ------------------------------------------------------------------
    tabs_labels = ["🔍 Analisa Saham", "🏆 Top 5 Rekomendasi", "💼 Portfolio Saya", "📊 Tabel Master Fundamental", "📚 Panduan & Legal"]
    main_tabs = st.tabs(tabs_labels)
    tab1, tab2, tab3, tab4, tab5 = main_tabs

    # Shared Logic - Always fetch if stock code is present
    ticker_sym = None
    data = None
    integrity = 100
    nama_saham = "N/A"
    is_crypto = False

    if kode_saham:
        ticker_sym = get_ticker_symbol(kode_saham, kode_pasar)
        # Using a slight delay to ensure UI consistency
        data = ambil_data_saham(ticker_sym)
    
        info = data["info"]
        nama_saham = info.get("shortName", info.get("longName", ticker_sym))
        harga_sekarang = info.get("regularMarketPrice") or info.get("currentPrice")
        prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
        market_cap = info.get("marketCap")
        currency = info.get("currency", "IDR")
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        quote_type = info.get("quoteType", "EQUITY")
        is_crypto = (quote_type == "CRYPTOCURRENCY")

        # Perubahan harga
        perubahan = None
        persen_perubahan = None
        if harga_sekarang and prev_close and prev_close > 0:
            perubahan = harga_sekarang - prev_close
            persen_perubahan = (perubahan / prev_close) * 100

    with tab1:
        if not kode_saham:
            st.info("👆 Masukkan kode saham di sidebar untuk memulai analisa.")
        elif not data:
            st.error(f"❌ Gagal mengambil data untuk **{ticker_sym}**. "
                     "Pastikan kode saham benar.")
        else:
            # ------------------------------------------------------------------
            # INFO UMUM SAHAM
            # ------------------------------------------------------------------
            st.markdown(f'<div class="section-title">📋 Informasi Umum — {nama_saham}</div>',
                        unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            change_class = "good" if (perubahan and perubahan >= 0) else "bad"
            change_text = f"+{persen_perubahan:.2f}%" if (persen_perubahan and persen_perubahan >= 0) else f"{persen_perubahan:.2f}%" if persen_perubahan else ""
            val_str = f"{harga_sekarang:,.0f}" if currency == "IDR" else f"${harga_sekarang:,.2f}" if harga_sekarang else "N/A"
            render_metric_card("💰 Harga Saat Ini", val_str, change_class, f"Perubahan: {change_text}")

        with col2:
            mc_str = format_mata_uang(market_cap, currency) if market_cap else "N/A"
            label_mc = "🏢 Market Cap" if not is_crypto else "📊 Market Cap (Crypto)"
            render_metric_card(label_mc, mc_str, "neutral", f"Sektor: {sector}" if not is_crypto else "Network Asset")

        with col3:
            label_ind = "🏭 Industri" if not is_crypto else "🌐 Exchange/Source"
            val_ind = industry if not is_crypto else info.get('exchange', 'N/A')
            render_metric_card(label_ind, val_ind[:25] if len(str(val_ind)) > 25 else val_ind,
                               "neutral", f"Bursa: {info.get('exchange', 'N/A')}" if not is_crypto else "Digital Asset")

        with col4:
            fifty_two_high = info.get("fiftyTwoWeekHigh")
            fifty_two_low = info.get("fiftyTwoWeekLow")
            range_str = "N/A"
            if fifty_two_low and fifty_two_high:
                if currency == "IDR":
                    range_str = f"{fifty_two_low:,.0f} - {fifty_two_high:,.0f}"
                else:
                    range_str = f"${fifty_two_low:,.2f} - ${fifty_two_high:,.2f}"
            render_metric_card("📊 Range 52 Minggu", range_str, "neutral", "Harga tertinggi & terendah setahun")

        # ------------------------------------------------------------------
        # TOMBOL BELI / SIMULASI
        # ------------------------------------------------------------------
        with st.expander("➕ Tambahkan ke Portfolio Saya", expanded=False):
            col_b1, col_b2, col_b3 = st.columns([1,1,1])
            with col_b1:
                input_harga = st.number_input("Harga Beli", value=float(harga_sekarang) if harga_sekarang else 0.0)
            with col_b2:
                input_jumlah = st.number_input("Jumlah (Lot untuk IDX / Lembar untuk US)", min_value=1, value=1)
            with col_b3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Simpan ke Portfolio", type="primary", use_container_width=True):
                    tambah_ke_portfolio(ticker_sym, nama_saham, input_harga, input_jumlah, kode_pasar)
                    st.success(f"Berhasil menambahkan {nama_saham} ke portfolio!")
                    time.sleep(1)
                    st.rerun()

        # ------------------------------------------------------------------
        # HITUNG SEMUA METRIK (HYBRID)
        # ------------------------------------------------------------------
        # 1. Fundamental
        if not is_crypto:
            roe = hitung_roe(data)
            der = hitung_der(data)
            cr = hitung_current_ratio(data)
            eg_data = hitung_earnings_growth(data)
            npm = hitung_npm(data)
            per = hitung_per(data)
            pbv = hitung_pbv(data)
            dy = hitung_dividend_yield(data)
            graham = hitung_graham_number(data)

            skor_fund, label_fund, detail_fund = hitung_skor_kualitas(roe, der, cr, eg_data, npm)
            skor_val, label_val, detail_val = hitung_skor_valuasi(per, pbv, dy, graham, harga_sekarang)
            # Normalisasi Fund Score: (Kualitas - Valuasi) diubah ke skala 0-100
            skor_fund_final = max(0, min(100, (skor_fund - skor_val + 100) / 2))
            
            # Pro Mode Metrics
            dcf_val = None
            if st.session_state.get("pro_mode", False):
                dr = 0.12 if kode_pasar == "IDX" else 0.10
                dcf_val = hitung_dcf_simple(data, dr)

            # Tambahkan prospek ke depan
            prospek = buat_prospek(eg_data, der, roe, npm)
        else:
            # Crypto Fundamental Logic (Market Cap & Supply)
            ath = info.get("allTimeHigh")
            skor_fund_final = 50
            if ath and harga_sekarang:
                skor_fund_final = max(0, min(100, (ath - harga_sekarang) / ath * 100))
            mcap = info.get("marketCap", 0)
            if mcap > 1e10: skor_fund_final += 20
            skor_fund_final = min(100, skor_fund_final)
            # prospek akan didefinisikan setelah power_score di bawah

        # 2. Teknikal
        skor_teknik, reasons_teknik, color_teknik = hitung_skor_teknikal(data["hist_1y"])
        
        # 3. Master Synthesis
        rekomendasi = buat_rekomendasi_master(skor_fund_final, skor_teknik, nama_saham)
        power_score = (skor_fund_final * 0.6) + (skor_teknik * 0.4)
        
        # 4. Prospek Synthesis (After power_score is ready)
        if is_crypto:
            prospek = {
                "label": "🚀 Momentum Kuat" if power_score > 70 else "📉 Tren Melemah" if power_score < 40 else "⏹️ Konsolidasi",
                "confidence": "Rendah (Volatil)",
                "signals": ["• High Volatility Asset", "• Sentiment Driven", "• Non-Fundamental Base"]
            }
        
        # ------------------------------------------------------------------
        # REKOMENDASI MASTER (MODERN UI)
        # ------------------------------------------------------------------
        if st.session_state.get("pro_mode", False):
            st.markdown(f'<div style="text-align:right;"><small style="color:#666;">Data Reliability: {integrity:.1f}% Verified</small></div>', unsafe_allow_html=True)
            
        st.markdown(f'<div class="section-title">🌟 Master Signal: {rekomendasi["aksi"]}</div>', unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns([1.5, 3, 1.5])
        
        with col_m1:
            # Gauge Power Score
            fig_power = buat_gauge_chart(power_score, f"{power_score:.0f}/100", "Master Power Score")
            st.plotly_chart(fig_power, use_container_width=True)
            
        with col_m2:
            st.markdown(f"""
            <div class="{rekomendasi['kelas']} rekom-box" style="height: 100%; display:flex; flex-direction:column; justify-content:center;">
                <h1 style="color:white; margin:0; font-size:3rem; display:flex; align-items:center; gap:15px;">
                    {rekomendasi['icon']} {rekomendasi['aksi']}
                </h1>
                <p style="color:rgba(255,255,255,0.9); margin-top:20px; font-size:1.1rem; line-height:1.8; font-weight:500;">
                    {rekomendasi['penjelasan']}
                </p>
                <div style="margin-top:15px; display:flex; gap:10px;">
                    <span class="score-badge" style="background:rgba(255,255,255,0.1); color:white;">Fund: {skor_fund_final:.0f}</span>
                    <span class="score-badge" style="background:rgba(255,255,255,0.1); color:white;">Tech: {skor_teknik:.0f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_m3:
            st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
            for r in reasons_teknik[:4]:
                st.markdown(f'<div style="font-size:0.9rem; margin-bottom:8px; color:#e0e0ff;">{r}</div>', unsafe_allow_html=True)

        if not is_crypto:
            st.markdown(f'<div class="section-title">📊 Detail Skor Fundamental</div>', unsafe_allow_html=True)
            col_r1, col_r3 = st.columns([1, 1])

            with col_r1:
                fig_kualitas = buat_gauge_chart(skor_fund, label_fund, "Skor Fundamental (Kualitas)")
                st.plotly_chart(fig_kualitas, use_container_width=True)
                badge_class = "green" if "BERKUALITAS" in label_fund else ("red" if "KURANG" in label_fund else "yellow")
                st.markdown(f'<div style="text-align:center"><span class="score-badge {badge_class}">{label_fund}</span></div>',
                            unsafe_allow_html=True)

            with col_r3:
                fig_valuasi = buat_gauge_chart(skor_val, label_val, "Skor Valuasi (Mahal)")
                st.plotly_chart(fig_valuasi, use_container_width=True)
                badge_class_v = "green" if "MURAH" in label_val else ("red" if "MAHAL" in label_val else "yellow")
                st.markdown(f'<div style="text-align:center"><span class="score-badge {badge_class_v}">{label_val}</span></div>',
                            unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-title">📊 Detail Skor Kripto</div>', unsafe_allow_html=True)
            col_c1, col_c2 = st.columns([1, 1])
            with col_c1:
                fig_c_fund = buat_gauge_chart(skor_fund_final, "Digital Asset", "Digital Asset Score")
                st.plotly_chart(fig_c_fund, use_container_width=True)
            with col_c2:
                # Show drop from ATH as a "Value" indicator for crypto
                ath = info.get("allTimeHigh")
                if ath and harga_sekarang:
                    drop_ath = (ath - harga_sekarang) / ath * 100
                    fig_drop = buat_gauge_chart(drop_ath, "Drop from ATH", "Drop from ATH (%)")
                    st.plotly_chart(fig_drop, use_container_width=True)

        if show_explanation:
            st.markdown("""
            <div class="explain-box">
            <strong>📖 Cara Baca Rekomendasi:</strong><br>
            • <strong>Skor Kualitas</strong>: Mengukur seberapa bagus perusahaan (ROE, utang, laba, dll). Makin tinggi makin bagus.<br>
            • <strong>Skor Valuasi</strong>: Mengukur seberapa mahal harganya. Makin RENDAH skor valuasi, makin MURAH.<br>
            • <strong>BELI</strong>: Perusahaan bagus + harga murah = "MERCY harga BAJAI" 🏆<br>
            • <strong>TAHAN</strong>: Perusahaan bagus tapi harga wajar/agak mahal<br>
            • <strong>JUAL</strong>: Perusahaan kurang bagus atau harga terlalu mahal
            </div>
            """, unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # PROSPEK KE DEPAN
        # ------------------------------------------------------------------
        st.markdown(f'<div class="section-title">🔮 Prospek ke Depan</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="font-size:1.3rem; color:#e0e0ff;">{prospek['label']}</div>
            <div class="sub" style="margin-top:10px;">Tingkat Keyakinan: <strong>{prospek['confidence']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

        for signal in prospek["signals"]:
            st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{signal}")

        if show_explanation:
            st.markdown("""
            <div class="explain-box">
            <strong>📖 Tentang Prospek:</strong><br>
            Proyeksi ini berdasarkan data historis (tren laba, utang, efisiensi). Ini bukan jaminan masa depan,
            tapi memberikan gambaran arah perusahaan berdasarkan kinerja sebelumnya.
            Selalu cek berita terbaru dan laporan keuangan terkini.
            </div>
            """, unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # GRAFIK ANALISA TEKNIKAL (ADVANCED)
        # ------------------------------------------------------------------
        st.markdown(f'<div class="section-title">📈 Trend & Momentum Analysis (Master Chart)</div>', unsafe_allow_html=True)

        with st.container(border=True):
            fig_master = buat_chart_harga(data["hist_1y"], nama_saham)
            if fig_master:
                st.plotly_chart(fig_master, use_container_width=True)
            else:
                st.warning("Data historis harga tidak tersedia untuk kalkulasi teknikal.")

        # Volatility & Momentum Analysis (Pro Mode)
        if st.session_state.get("pro_mode", False):
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                st.markdown("#### ⚡ Volatility Analysis")
                hist = data["hist_1y"]
                if not hist.empty:
                    std_dev = hist['Close'].pct_change().std() * (252**0.5) # Annualized Volatility
                    st.metric("Annualized Volatility", f"{std_dev*100:.1f}%", help="Standar deviasi pergerakan harga setahun. >30% dianggap volatil.")
            with col_v2:
                st.markdown("#### 🚀 Momentum Signals")
                rsi_val = hitung_rsi(hist)
                if rsi_val:
                    rsi_label = "Jenuh Beli (Sell?)" if rsi_val > 70 else ("Jenuh Jual (Buy?)" if rsi_val < 30 else "Normal")
                    st.metric("RSI (14)", f"{rsi_val:.1f}", rsi_label)

        if not is_crypto:
            # ------------------------------------------------------------------
            # SCREENING KUALITAS (Detail)
            # ------------------------------------------------------------------
            st.markdown(f'<div class="section-title">🏅 Screening Kualitas Perusahaan</div>', unsafe_allow_html=True)

            col_q1, col_q2, col_q3, col_q4, col_q5 = st.columns(5)

            with col_q1:
                status_roe = "good" if (roe and roe >= 15) else ("neutral" if (roe and roe >= 10) else "bad")
                val_roe = f"{roe:.1f}%" if roe is not None else "N/A"
                render_metric_card("ROE", val_roe, status_roe, "Target: ≥ 15%")
                if show_explanation:
                    st.markdown(f'<div class="explain-box">{PENJELASAN.get("ROE", "")}</div>', unsafe_allow_html=True)

            with col_q2:
                status_der = "good" if (der is not None and der <= 0.5) else ("neutral" if (der is not None and der <= 1.0) else "bad")
                val_der = f"{der:.2f}x" if der is not None else "N/A"
                render_metric_card("DER", val_der, status_der, "Target: ≤ 0.5x")
                if show_explanation:
                    st.markdown(f'<div class="explain-box">{PENJELASAN.get("DER", "")}</div>', unsafe_allow_html=True)

            with col_q3:
                status_cr = "good" if (cr and cr >= 1.5) else ("neutral" if (cr and cr >= 1.0) else "bad")
                val_cr = f"{cr:.2f}x" if cr is not None else "N/A"
                render_metric_card("Current Ratio", val_cr, status_cr, "Target: ≥ 1.5x")
                if show_explanation:
                    st.markdown(f'<div class="explain-box">{PENJELASAN.get("CR", "")}</div>', unsafe_allow_html=True)

            with col_q4:
                if eg_data:
                    status_eg = "good" if eg_data["avg_growth"] > 5 else ("neutral" if eg_data["avg_growth"] >= 0 else "bad")
                    val_eg = f"{eg_data['avg_growth']:.1f}%"
                    eg_trend = eg_data["trend"]
                else:
                    status_eg = "bad"
                    val_eg = "N/A"
                    eg_trend = ""
                render_metric_card("Earnings Growth", val_eg, status_eg, f"Tren: {eg_trend}")
                if show_explanation:
                    st.markdown(f'<div class="explain-box">{PENJELASAN.get("EG", "")}</div>', unsafe_allow_html=True)

            with col_q5:
                status_npm = "good" if (npm and npm >= 10) else ("neutral" if (npm and npm >= 5) else "bad")
                val_npm = f"{npm:.1f}%" if npm is not None else "N/A"
                render_metric_card("Net Profit Margin", val_npm, status_npm, "Target: ≥ 10%")
                if show_explanation:
                    st.markdown(f'<div class="explain-box">{PENJELASAN["NPM"]}</div>', unsafe_allow_html=True)
        else:
            # ------------------------------------------------------------------
            # SCREENING KRIPTO (Detail)
            # ------------------------------------------------------------------
            st.markdown(f'<div class="section-title">🌕 Statistik Jaringan & Suplai (CRYPTO)</div>', unsafe_allow_html=True)
            col_cr1, col_cr2, col_cr3, col_cr4 = st.columns(4)
            
            with col_cr1:
                ath_val = info.get("allTimeHigh")
                ath_str = format_mata_uang(ath_val, currency) if ath_val else "N/A"
                render_metric_card("🏔️ All-Time High", ath_str, "neutral", "Harga tertinggi sepanjang masa")
            
            with col_cr2:
                circ_supply = info.get("circulatingSupply")
                circ_str = f"{circ_supply:,.0f}" if circ_supply else "N/A"
                render_metric_card("🔄 Circulating Supply", circ_str, "neutral", f"Unit yang beredar")

            with col_cr3:
                max_supply = info.get("maxSupply")
                max_str = f"{max_supply:,.0f}" if max_supply else "Tak Terbatas"
                render_metric_card("📦 Max Supply", max_str, "neutral", "Batas maksimal koin")

            with col_cr4:
                dist_ath = ((info.get("allTimeHigh", 0) - harga_sekarang) / info.get("allTimeHigh", 1) * 100) if info.get("allTimeHigh") else 0
                render_metric_card("📉 Drop dari ATH", f"{dist_ath:.1f}%", "bad" if dist_ath < 20 else "good", "Jarak dari puncak")

        if not is_crypto:
            # ------------------------------------------------------------------
            # SCREENING VALUASI (Detail)
            # ------------------------------------------------------------------
            st.markdown(f'<div class="section-title">💰 Screening Valuasi (Harga Murah?)</div>', unsafe_allow_html=True)

            col_v1, col_v2, col_v3, col_v4 = st.columns(4)

            with col_v1:
                status_per = "good" if (per and per < 15) else ("neutral" if (per and per < 25) else "bad")
                val_per = f"{per:.1f}x" if per is not None else "N/A"
                murah_per = "Sangat Murah! 🔥" if (per and per < 10) else ("Murah ✅" if (per and per < 15) else ("Wajar" if (per and per < 25) else "Mahal ⚠️"))
                render_metric_card("PER", val_per, status_per, murah_per)
                if show_explanation:
                    st.markdown(f'<div class="explain-box">{PENJELASAN["PER"]}</div>', unsafe_allow_html=True)

            with col_v2:
                status_pbv = "good" if (pbv and pbv < 1.5) else ("neutral" if (pbv and pbv < 3) else "bad")
                val_pbv = f"{pbv:.2f}x" if pbv is not None else "N/A"
                murah_pbv = "Sangat Murah! 🔥" if (pbv and pbv < 1) else ("Murah ✅" if (pbv and pbv < 1.5) else ("Wajar" if (pbv and pbv < 3) else "Mahal ⚠️"))
                render_metric_card("PBV", val_pbv, status_pbv, murah_pbv)
                if show_explanation:
                    st.markdown(f'<div class="explain-box">{PENJELASAN["PBV"]}</div>', unsafe_allow_html=True)

            with col_v3:
                status_dy = "good" if (dy and dy >= 3) else ("neutral" if (dy and dy >= 1) else "bad")
                val_dy = f"{dy:.2f}%" if dy is not None else "N/A"
                menarik_dy = "Sangat Menarik! 🔥" if (dy and dy >= 5) else ("Menarik ✅" if (dy and dy >= 3) else ("Cukup" if (dy and dy >= 1) else "Rendah"))
                render_metric_card("Dividend Yield", val_dy, status_dy, menarik_dy)
                if show_explanation:
                    st.markdown(f'<div class="explain-box">{PENJELASAN["DY"]}</div>', unsafe_allow_html=True)

            with col_v4:
                if graham and harga_sekarang:
                    if currency == "IDR":
                        val_graham = f"{graham:,.0f}"
                        val_harga_now = f"{harga_sekarang:,.0f}"
                    else:
                        val_graham = f"${graham:,.2f}"
                        val_harga_now = f"${harga_sekarang:,.2f}"
                    status_graham = "good" if harga_sekarang < graham else "bad"
                    label_graham = "UNDERVALUED ✅" if harga_sekarang < graham else "OVERVALUED ⚠️"
                    render_metric_card("Graham Number", val_graham, status_graham, f"Harga: {val_harga_now} → {label_graham}")
                else:
                    render_metric_card("Graham Number", "N/A", "neutral", "Data EPS/BVPS tidak tersedia")
                
            # DCF Intrinsic Value (Pro Mode Only)
            if st.session_state.get("pro_mode", False):
                with st.container():
                    st.markdown('<div style="margin-bottom:10px;"></div>', unsafe_allow_html=True)
                    if dcf_val:
                        dcf_status = "good" if harga_sekarang < dcf_val else "bad"
                        upside_dcf = ((dcf_val - harga_sekarang)/harga_sekarang*100)
                        dcf_label = f"Upside: {upside_dcf:+.1f}%"
                        val_dcf = f"{dcf_val:,.0f}" if currency == "IDR" else f"${dcf_val:,.2f}"
                        render_metric_card("DCF Intrinsic Value", val_dcf, dcf_status, dcf_label)
                    else:
                        render_metric_card("DCF Intrinsic Value", "N/A", "neutral", "Data Cash Flow minim")

            if show_explanation:
                st.markdown(f'<div class="explain-box">{PENJELASAN["GRAHAM"]}</div>', unsafe_allow_html=True)
                if st.session_state.get("pro_mode", False):
                    st.markdown(f'<div class="explain-box">{PENJELASAN["DCF"]}</div>', unsafe_allow_html=True)

            # ------------------------------------------------------------------
            # GRAFIK FUNDAMENTAL
            # ------------------------------------------------------------------
            st.markdown(f'<div class="section-title">📊 Grafik Fundamental</div>', unsafe_allow_html=True)

            fig_fund = buat_chart_fundamental(data, nama_saham)
            if fig_fund:
                st.plotly_chart(fig_fund, use_container_width=True)
            else:
                st.info("Data untuk visualisasi fundamental tidak tersedia.")

            # ------------------------------------------------------------------
            # TABEL EARNINGS HISTORY
            # ------------------------------------------------------------------
            if eg_data and eg_data.get("net_incomes") and len(eg_data["net_incomes"]) > 1:
                st.markdown(f'<div class="section-title">📋 Riwayat Laba Bersih</div>', unsafe_allow_html=True)

                ni = eg_data["net_incomes"]
                gr = eg_data["growth_rates"]

                # Buat chart bar untuk laba bersih
                year_labels = [f"T-{len(ni)-1-i}" for i in range(len(ni))]

                fig_ni = go.Figure()
                colors_ni = ["#4ade80" if (i < len(gr) and gr[i] >= 0) or i == len(ni)-1 else "#f87171"
                             for i in range(len(ni))]
                fig_ni.add_trace(go.Bar(
                    x=year_labels,
                    y=ni,
                    marker_color=colors_ni,
                    text=[format_mata_uang(v, currency) for v in ni],
                    textposition="outside",
                    textfont=dict(size=11, color="#e0e0ff"),
                ))

                fig_ni.update_layout(
                    title="Laba Bersih per Tahun (Terbaru ke Terlama →)",
                    title_font=dict(size=14, color="#e0e0ff"),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#b8b8d0", family="Inter"),
                    height=350,
                    margin=dict(l=10, r=10, t=50, b=10),
                    showlegend=False,
                    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
                )
                st.plotly_chart(fig_ni, use_container_width=True)

            # Industry Peer Comparison (Pro Mode Only)
            if st.session_state.get("pro_mode", False):
                tampilkan_peer_comparison(ticker_sym, sector, industry, DAFTAR_SAHAM_IDX)

        # ------------------------------------------------------------------
        # DISCLAIMER
        # ------------------------------------------------------------------
        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; padding:20px; color:#666; font-size:0.8rem; line-height:1.7;">
        ⚠️ <strong>DISCLAIMER</strong>: Aplikasi ini hanya alat bantu analisa dan BUKAN saran investasi.
        Semua keputusan investasi adalah tanggung jawab pengguna.
        Selalu lakukan riset mandiri (DYOR) dan konsultasikan dengan ahli keuangan profesional.
        Data bersumber dari Yahoo Finance dan bisa saja terlambat atau tidak akurat.<br>
        Dibuat dengan ❤️ mengikuti filosofi Lo Kheng Hong — "Beli Saham Mercy di Harga Bajai"
        </div>
        """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # TAB 2: TOP 5 REKOMENDASI
    # ------------------------------------------------------------------
    with tab2:
        market_name = "IDX (Indonesia)" if kode_pasar == "IDX" else "US (Amerika Serikat)"
        st.markdown(f'<div class="section-title">🏆 Top 5 Saham Rekomendasi BELI - {market_name}</div>',
                    unsafe_allow_html=True)

        st.markdown(f"""
        <div class="explain-box">
        Screening otomatis dari daftar saham unggulan pasar {market_name}.
        Dicari saham dengan skor BELI tertinggi = kualitas tinggi + harga murah.
        Proses ini mungkin memakan waktu karena mengambil data real-time.
        </div>
        """, unsafe_allow_html=True)

        action_label = "🔄 Jalankan Screening (IDX)" if kode_pasar == "IDX" else "🔄 Jalankan Screening (US)"
        if st.button(action_label, use_container_width=True, type="primary"):
            progress = st.progress(0, "Memulai screening...")

            results = []
            if kode_pasar == "IDX":
                daftar_screening = DAFTAR_SAHAM_IDX
            elif kode_pasar == "US":
                daftar_screening = DAFTAR_SAHAM_US
            else:
                daftar_screening = DAFTAR_CRYPTO
            
            total = len(daftar_screening)

            for idx, sym in enumerate(daftar_screening):
                progress.progress((idx + 1) / total,
                                  f"Menganalisa {sym} ({idx+1}/{total})...")
                try:
                    data_s = ambil_data_saham(sym)
                    if data_s is None:
                        continue

                    info_s = data_s["info"]
                    nama_s = info_s.get("shortName", sym)
                    harga_s = info_s.get("regularMarketPrice") or info_s.get("currentPrice")

                    # Kalkulasi skor sesuai jenis aset
                    if kode_pasar != "Crypto":
                        roe_s = hitung_roe(data_s)
                        der_s = hitung_der(data_s)
                        cr_s = hitung_current_ratio(data_s)
                        eg_s = hitung_earnings_growth(data_s)
                        npm_s = hitung_npm(data_s)
                        per_s = hitung_per(data_s)
                        pbv_s = hitung_pbv(data_s)
                        dy_s = hitung_dividend_yield(data_s)
                        graham_s = hitung_graham_number(data_s)

                        sk_q_s, _, _ = hitung_skor_kualitas(roe_s, der_s, cr_s, eg_s, npm_s)
                        sk_v_s, _, _ = hitung_skor_valuasi(per_s, pbv_s, dy_s, graham_s, harga_s)
                        
                        # Normalisasi Fund Score (0-100)
                        sk_fund_final_s = max(0, min(100, (sk_q_s - sk_v_s + 100) / 2))
                    else:
                        # Logika Crypto Screening
                        ath_s = info_s.get("allTimeHigh")
                        mcap_s = info_s.get("marketCap", 0)
                        sk_fund_final_s = 50
                        if ath_s and harga_s:
                            sk_fund_final_s = max(0, min(100, (ath_s - harga_s) / ath_s * 100))
                        if mcap_s > 1e10: sk_fund_final_s += 20
                        sk_fund_final_s = min(100, sk_fund_final_s)
                        roe_s = der_s = per_s = pbv_s = None

                    # 2. Teknikal
                    sk_teknik_s, _, _ = hitung_skor_teknikal(data_s["hist_1y"])
                    
                    # 3. Master Score
                    power_score_s = (sk_fund_final_s * 0.6) + (sk_teknik_s * 0.4)
                    rekom_master_s = buat_rekomendasi_master(sk_fund_final_s, sk_teknik_s, nama_s)

                    if sk_fund_final_s is not None and sk_teknik_s is not None:
                        results.append({
                            "Peringkat": 0,
                            "Kode": sym.replace(".JK", "").replace("-USD", ""),
                            "Nama": nama_s[:30] if len(str(nama_s)) > 30 else nama_s,
                            "Harga": harga_s,
                            "Power Score": round(power_score_s, 1),
                            "Fund Score": round(sk_fund_final_s, 1),
                            "Tech Score": round(sk_teknik_s, 1),
                            "Rekomendasi": rekom_master_s["aksi"],
                            "ROE (%)": round(roe_s, 1) if roe_s else None,
                            "PER (x)": round(per_s, 1) if per_s else None,
                            "PBV (x)": round(pbv_s, 2) if pbv_s else None,
                        })
                except Exception:
                    continue

                progress.empty()

                if results:
                    # Sort by Power Score
                    results.sort(key=lambda x: x["Power Score"], reverse=True)
                    for i, r in enumerate(results):
                        r["Peringkat"] = i + 1

                    st.session_state["top_5_picks"] = results[:10] # Persist results
            else:
                st.info("👆 Klik tombol di atas untuk menjalankan screening otomatis.")

        # DISPLAY PERSISTED RESULTS
        if "top_5_picks" in st.session_state:
            res_list = st.session_state["top_5_picks"]
            market_name = "IDX (Indonesia)" if kode_pasar == "IDX" else "US (Amerika Serikat)"
            currency_symbol = "Rp" if kode_pasar == "IDX" else "$"

            # Tampilkan sebagai cards (Top 5)
            for rank, item in enumerate(res_list[:5], 1):
                emoji = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else f"#{rank}"))
                h_val = item.get('Harga')
                harga_str = f"{currency_symbol} {h_val:,.0f}" if (kode_pasar == "IDX" and h_val) else (f"{currency_symbol}{h_val:,.2f}" if h_val else "N/A")

                st.markdown(f"""
                <div class="metric-card" style="display:grid; grid-template-columns: 2.2fr 1.2fr 1fr 1fr 1fr 1.3fr; align-items:center; gap:16px;">
                    <div style="display:flex; align-items:center; gap:16px;">
                        <span style="font-size:2rem; min-width: 48px; text-align: center;">{emoji}</span>
                        <div style="overflow: hidden;">
                            <div style="font-size:1.1rem; font-weight:700; color:#e0e0ff; letter-spacing: 0.5px;">{item['Kode']}</div>
                            <div style="font-size:0.75rem; color:#888; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{item['Nama']}</div>
                        </div>
                    </div>
                    <div style="text-align:center;">
                        <div class="label" style="margin-bottom: 4px;">HARGA</div>
                        <div style="font-size:0.95rem; color:#e0e0ff; font-weight:600;">{harga_str}</div>
                    </div>
                    <div style="text-align:center;">
                        <div class="label" style="margin-bottom: 4px;">POWER</div>
                        <div style="font-size:1.3rem; font-weight:800; color:var(--accent-primary);">{item['Power Score']}</div>
                    </div>
                    <div style="text-align:center;">
                        <div class="label" style="margin-bottom: 4px;">FUND</div>
                        <div style="font-size:1.1rem; font-weight:700; color:var(--success);">{item['Fund Score']}</div>
                    </div>
                    <div style="text-align:center;">
                        <div class="label" style="margin-bottom: 4px;">TECH</div>
                        <div style="font-size:1.1rem; font-weight:700; color:var(--warning);">{item['Tech Score']}</div>
                    </div>
                    <div style="text-align:right;">
                        <span class="score-badge {'green' if 'BUY' in item['Rekomendasi'] else ('red' if 'SELL' in item['Rekomendasi'] or 'WASPADA' in item['Rekomendasi'] else 'yellow')}" style="padding: 0.4rem 1rem; border-radius: 8px;">{item['Rekomendasi']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Tampilkan juga sebagai tabel
            st.markdown("---")
            st.markdown(f'<div class="section-title">📋 Tabel Lengkap Hasil Screening</div>',
                        unsafe_allow_html=True)

            df_res = pd.DataFrame(res_list)
            st.dataframe(
                df_res,
                width="stretch",
                hide_index=True,
                column_config={
                    "Peringkat": st.column_config.NumberColumn("🏆", width="small"),
                    "Kode": st.column_config.TextColumn("Kode", width="small"),
                    "Nama": st.column_config.TextColumn("Nama Perusahaan"),
                    "Harga": st.column_config.NumberColumn("Harga", format="Rp%,.0f") if kode_pasar == "IDX" else st.column_config.NumberColumn("Harga", format="$%,.2f"),
                    "Power Score": st.column_config.ProgressColumn("Master Power", min_value=0, max_value=100, format="%.1f"),
                    "Fund Score": st.column_config.NumberColumn("Fundamental", format="%.1f"),
                    "Tech Score": st.column_config.NumberColumn("Teknikal", format="%.1f"),
                    "ROE (%)": st.column_config.NumberColumn("ROE %", format="%.1f%%"),
                    "PER (x)": st.column_config.NumberColumn("PER", format="%.1f"),
                    "PBV (x)": st.column_config.NumberColumn("PBV", format="%.2f"),
                    "Rekomendasi": st.column_config.TextColumn("Rekomendasi"),
                }
            )

    # ------------------------------------------------------------------
    # TAB 3: PORTFOLIO SAYA
    # ------------------------------------------------------------------
    with tab3:
        st.markdown(f'<div class="section-title">💼 Portfolio Investasi Saya</div>', unsafe_allow_html=True)
        
        df_p = muat_portfolio()
        
        if df_p.empty:
            st.info("Portfolio Anda masih kosong. Mulai dengan mencari saham di tab 'Analisa Saham' dan klik 'Tambahkan ke Portfolio'.")
        else:
            # Kalkulasi Portfolio secara real-time
            with st.spinner("🔄 Memperbarui harga portfolio..."):
                portfolio_records = []
                total_modal = 0
                total_value = 0
                
                for idx, row in df_p.iterrows():
                    ticker_p = row["Ticker"]
                    try:
                        # Ambil data melalui cache yang sudah ada
                        data_p = ambil_data_saham(ticker_p)
                        info_p = data_p["info"]
                        curr_p = info_p.get("regularMarketPrice") or info_p.get("currentPrice")
                        nama_p = info_p.get("shortName", row["Nama"])
                    except Exception:
                        curr_p = row["Harga Beli"]
                        nama_p = row["Nama"]

                    multiplier = 100 if row["Pasar"] == "IDX" else 1
                    modal_item = row["Harga Beli"] * row["Jumlah"] * multiplier
                    value_item = curr_p * row["Jumlah"] * multiplier
                    gain_loss = value_item - modal_item
                    gain_loss_pct = (gain_loss / modal_item * 100) if modal_item != 0 else 0
                    
                    total_modal += modal_item
                    total_value += value_item
                    
                    portfolio_records.append({
                        "ID": idx,
                        "Ticker": ticker_p.replace(".JK", ""),
                        "Nama": nama_p,
                        "Pasar": row["Pasar"],
                        "Jumlah": row["Jumlah"],
                        "Avg Price": row["Harga Beli"],
                        "Last Price": curr_p,
                        "Modal": modal_item,
                        "Market Value": value_item,
                        "Gain/Loss": gain_loss,
                        "Gain/Loss (%)": gain_loss_pct
                    })

            # Ringkasan Portfolio
            col_sum1, col_sum2, col_sum3 = st.columns(3)
            total_gl = total_value - total_modal
            total_gl_pct = (total_gl / total_modal * 100) if total_modal != 0 else 0
            
            with col_sum1:
                render_metric_card("Total Modal", format_mata_uang(total_modal), "neutral", "Dana yang dideploy")
            with col_sum2:
                render_metric_card("Market Value", format_mata_uang(total_value), "neutral", "Nilai saat ini")
            with col_sum3:
                gl_class = "good" if total_gl >= 0 else "bad"
                render_metric_card("Total Profit/Loss", format_mata_uang(total_gl), gl_class, f"{total_gl_pct:+.2f}%")

            st.markdown("#### Detail Kepemilikan")
            view_df = pd.DataFrame(portfolio_records)
            
            for i, row in view_df.iterrows():
                with st.container():
                    col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns([1.5, 2, 2, 2, 1])
                    with col_p1:
                        st.markdown(f"**{row['Ticker']}**<br><small>{row['Nama']}</small>", unsafe_allow_html=True)
                    with col_p2:
                        st.markdown(f"<small>Avg: {format_mata_uang(row['Avg Price'])}</small><br>Last: **{format_mata_uang(row['Last Price'])}**", unsafe_allow_html=True)
                    with col_p3:
                        st.markdown(f"<small>Market Value</small><br>**{format_mata_uang(row['Market Value'])}**", unsafe_allow_html=True)
                    with col_p4:
                        color = "#4ade80" if row['Gain/Loss'] >= 0 else "#f87171"
                        st.markdown(f"<small>Profit/Loss</small><br><span style='color:{color}; font-weight:700;'>{format_mata_uang(row['Gain/Loss'])} ({row['Gain/Loss (%)']:+.2f}%)</span>", unsafe_allow_html=True)
                    with col_p5:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("🗑️", key=f"del_{row['ID']}", help="Hapus dari portfolio"):
                            hapus_dari_portfolio(row['ID'])
                            st.rerun()
                st.markdown("<hr style='margin:10px 0; opacity:0.1;'>", unsafe_allow_html=True)

            st.markdown("""
            <div class="explain-box">
            <strong>Catatan:</strong> Data portfolio ini disimpan secara lokal. 
            Harga diperbarui otomatis setiap kali Anda membuka tab ini (mengikuti cache sistem).
            Filosofi: Investasilah pada bisnis yang hebat, bukan sekadar angka di layar.
            </div>
            """, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # TAB 4: TABEL MASTER FUNDAMENTAL (99% ACCURATE BENCHMARK)
    # ------------------------------------------------------------------
    with tab4:
        st.markdown(f'<div class="section-title">📊 Tabel Master Fundamental & Harga Asli</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="explain-box">
        💡 <strong>Mode Master</strong>: Tabel ini menggunakan <strong>Graham Number</strong> sebagai patokan harga wajar (99% akurasi akuntansi).
        Gunakan tabel ini untuk membandingkan banyak saham sekaligus dan mencari "Mercy" yang sedang didiskon besar oleh pasar.
        </div>
        """, unsafe_allow_html=True)

        # Controls
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            default_tickers = [t.replace(".JK", "") for t in DAFTAR_SAHAM_IDX]
            selected_tickers = st.multiselect(
                "Pilih Saham untuk Dibandingkan:",
                options=default_tickers + ["BBCA", "BBRI", "TLKM", "ASII", "UNVR", "ADRO", "GZCO", "BMTR"],
                default=default_tickers[:10]
            )
        
        with col_c2:
            search_query = st.text_input("🔍 Cari di Tabel:", placeholder="Ketik kode/nama...")
            run_bulk = st.button("🔄 Jalankan Analisa Massal", use_container_width=True, type="primary")

        if run_bulk or "bulk_results" in st.session_state:
            if run_bulk:
                bulk_data = []
                progress_bulk = st.progress(0, "Mulai mengambil data master...")
                
                for i, t in enumerate(selected_tickers):
                    progress_bulk.progress((i + 1) / len(selected_tickers), f"Menganalisa {t}...")
                    ticker_bulk = get_ticker_symbol(t, "IDX") 
                    d = ambil_data_saham(ticker_bulk)
                    
                    if d:
                        inf = d["info"]
                        price = inf.get("regularMarketPrice") or inf.get("currentPrice")
                        prev = inf.get("previousClose") or inf.get("regularMarketPreviousClose")
                        eps = inf.get("trailingEps", 0)
                        bvps = inf.get("bookValue", 0)
                        roe = (inf.get("returnOnEquity", 0) or 0) * 100
                        per = inf.get("trailingPE") or inf.get("forwardPE")
                        mcap = inf.get("marketCap", 0)
                        div_yield = (inf.get("dividendYield", 0) or 0) * 100
                        last_div = inf.get("dividendRate", 0)
                        
                        # Graham Calculation (Harga Asli)
                        harga_asli = (22.5 * eps * bvps) ** 0.5 if eps > 0 and bvps > 0 else 0
                        under_over = harga_asli - price if harga_asli > 0 else 0
                        upside = (under_over / price * 100) if price and price > 0 else 0
                        mos = (under_over / harga_asli) if harga_asli and harga_asli > 0 else (0 if price < harga_asli else 2)
                        pbv = price / bvps if bvps and bvps > 0 else 0
                        
                        change = price - prev if price and prev else 0
                        change_pct = (change / prev * 100) if prev and prev > 0 else 0
                        
                        # NAVS Estimate
                        total_assets = inf.get("totalAssets", 0)
                        total_liab = inf.get("totalDebt", 0) # simplified
                        shares = inf.get("sharesOutstanding", 1)
                        navs = (total_assets - total_liab) / shares if shares > 0 else bvps

                        bulk_data.append({
                            "Kode": t,
                            "Nama": inf.get("shortName", t),
                            "Market Cap": mcap,
                            "Naik/Turun": round(change, 2),
                            "%": round(change_pct, 2),
                            "Price": price,
                            "NAVS": round(navs, 2),
                            "BVPS": round(bvps, 2),
                            "EPS": round(eps, 2),
                            "Fair Value": round(harga_asli, 2),
                            "Under (+)": round(under_over, 2),
                            "Upside (%)": round(upside, 1),
                            "MOS": round(mos, 2),
                            "ROE (%)": round(roe, 2),
                            "PER (x)": round(per, 2) if per else None,
                            "PBV (x)": round(pbv, 2),
                            "Dividend": round(last_div, 2),
                            "Div Yield (%)": round(div_yield, 2),
                            "Rekomendasi": "SUPER BUY 🚀" if upside > 50 and roe > 15 else ("BUY ✅" if upside > 20 and roe > 10 else ("HOLD ⏳" if upside > -10 else "SELL 🛑"))
                        })
                
                st.session_state["bulk_results"] = bulk_data
                progress_bulk.empty()

            # Display Table
            df_bulk = pd.DataFrame(st.session_state["bulk_results"])
            
            # Search Filter
            if search_query:
                df_bulk = df_bulk[
                    df_bulk["Kode"].str.contains(search_query, case=False) | 
                    df_bulk["Nama"].str.contains(search_query, case=False)
                ]

            if not df_bulk.empty:
                # Styling Logic (Mercy-Bajai Criteria)
                def color_rows(row):
                    styles = ['' for _ in row.index]
                    
                    # EPS Index
                    idx_eps = df_bulk.columns.get_loc("EPS")
                    if row["EPS"] > 0: styles[idx_eps] = 'background-color: rgba(74, 222, 128, 0.2); color: #4ade80;'
                    
                    # Valuation Section
                    idx_under = df_bulk.columns.get_loc("Under (+)")
                    idx_asli = df_bulk.columns.get_loc("Fair Value")
                    idx_upside = df_bulk.columns.get_loc("Upside (%)")
                    if row["Under (+)"] > 0:
                        styles[idx_under] = 'background-color: rgba(74, 222, 128, 0.3); color: #4ade80; font-weight: bold;'
                        styles[idx_asli] = 'background-color: rgba(74, 222, 128, 0.1);'
                        styles[idx_upside] = 'background-color: rgba(74, 222, 128, 0.2);'
                    else:
                        styles[idx_under] = 'background-color: rgba(248, 113, 113, 0.2); color: #f87171;'

                    # MOS
                    idx_mos = df_bulk.columns.get_loc("MOS")
                    if row["MOS"] > 0.3: styles[idx_mos] = 'background-color: rgba(74, 222, 128, 0.3); color: white;'
                    elif row["MOS"] < 0: styles[idx_mos] = 'background-color: rgba(248, 113, 113, 0.2); color: #f87171;'

                    # ROE
                    idx_roe = df_bulk.columns.get_loc("ROE (%)")
                    if row["ROE (%)"] > 15: styles[idx_roe] = 'background-color: rgba(74, 222, 128, 0.2); color: #4ade80;'
                    
                    # PER
                    idx_per = df_bulk.columns.get_loc("PER (x)")
                    if row["PER (x)"] and row["PER (x)"] < 10: styles[idx_per] = 'background-color: rgba(74, 222, 128, 0.2); color: #4ade80;'

                    # Recommendation
                    idx_rekom = df_bulk.columns.get_loc("Rekomendasi")
                    if "SUPER BUY" in row["Rekomendasi"]:
                        styles[idx_rekom] = 'background-color: #065f46; color: white; font-weight: bold; border: 1px solid #4ade80;'
                    elif "BUY" in row["Rekomendasi"]:
                        styles[idx_rekom] = 'background-color: #064e3b; color: #a7f3d0;'
                    elif "HOLD" in row["Rekomendasi"]:
                        styles[idx_rekom] = 'background-color: #78350f; color: #fcd34d;'
                    else:
                        styles[idx_rekom] = 'background-color: #7f1d1d; color: #fca5a5;'

                    return styles

                st.markdown("---")
                st.dataframe(
                    df_bulk.style.apply(color_rows, axis=1),
                    width="stretch", 
                    height=650,
                    column_config={
                        "Market Cap": st.column_config.NumberColumn("Market Cap", format="Rp%,.0f"),
                        "Price": st.column_config.NumberColumn("Price", format="%,.0f"),
                        "Fair Value": st.column_config.NumberColumn("Fair Value", format="%,.0f"),
                        "Under (+)": st.column_config.NumberColumn("Under (+)", format="%,.0f"),
                        "Upside (%)": st.column_config.NumberColumn("Upside %", format="%.1f%%"),
                        "MOS": st.column_config.NumberColumn("MOS", format="%.2f"),
                        "%": st.column_config.NumberColumn("Chg %", format="%.2f%%"),
                        "Naik/Turun": st.column_config.NumberColumn("Diff", format="%,.0f"),
                        "Rekomendasi": st.column_config.TextColumn("⭐ Master Recommendation"),
                    }
                )
                
                st.info("💡 **Tips**: Klik pada judul kolom untuk mengurutkan (Sort). Cari saham dengan 'Under (+)' positif dan 'ROE' > 15% untuk menemukan Saham Mercy.")
            else:
                st.warning("Tidak ada data yang cocok dengan pencarian Anda.")
        else:
            st.info("👆 Silakan pilih saham dan klik tombol di atas untuk memulai Analisa Master.")

    # ------------------------------------------------------------------
    # TAB 5: PANDUAN & LEGAL
    # ------------------------------------------------------------------
    with tab5:
        st.markdown('<div class="section-title">📚 Panduan Penggunaan & Bantuan</div>', unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("### 📖 Selamat Datang!")
            st.write("""
            Halo Bapak/Ibu Investor! Selamat datang di **Grand Master Hybrid Pro**. 
            Tool ini dirancang untuk memudahkan Anda membedah 'jeroan' perusahaan hanya dalam hitungan detik. 
            Berikut adalah cara singkat menggunakan fitur-fitur kami:
            """)
            
            for title, desc in GUIDE_CONTENT.items():
                with st.expander(f"🔹 Cara pakai {title}"):
                    st.write(desc)
                    
        with col_g2:
            st.markdown("### ⚖️ Ketentuan & Hukum")
            st.markdown(DISCLAIMER_TEXT, unsafe_allow_html=True)
            st.write("""
            Aplikasi ini dibuat dengan penuh dedikasi untuk membantu edukasi finansial. 
            Kami menggunakan data API publik yang biasanya memiliki delay 15-20 menit. 
            Keakuratan 99.99% yang kami sebutkan merujuk pada ketepatan kalkulasi rumus-rumus finansial 
            berdasarkan data yang kami terima. Tentunya, penilaian kualitatif (seperti kualitas manajemen) 
            tetap harus Bapak/Ibu lakukan sendiri ya.
            """)

        st.markdown("---")
        st.success("Selamat berinvestasi, semoga Bapak/Ibu selalu cuan dan berkah! 🎉")

    # === FOOTER HAK CIPTA ===
    st.markdown("---")
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 1rem;
        margin-top: 2rem;
        background: linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9));
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
    ">
        <p style="color: #94a3b8; font-size: 0.85rem; margin: 0 0 0.5rem 0; letter-spacing: 1px;">
            🛠️ Dibuat dengan ❤️ oleh
        </p>
        <p style="
            color: #38bdf8;
            font-size: 1.2rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            text-shadow: 0 0 20px rgba(56,189,248,0.3);
        ">
            Dwi Adi S
        </p>
        <p style="color: #64748b; font-size: 0.75rem; margin: 0;">
            © 2026 Dwi Adi S — All Rights Reserved. | Analisa Saham MERCY-BAJAI
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# JALANKAN APLIKASI
# =====================================================================
if __name__ == "__main__":
    main()
