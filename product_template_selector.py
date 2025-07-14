import pandas as pd
import streamlit as st
from pathlib import Path

# -----------------------
# Konfiguration
# -----------------------
DATA_FILE = Path(__file__).with_name("templates.csv")  # erwartet eine CSV in demselben Ordner wie dieses Skript
FTP_IMAGE_BASE_URL = "https://ftp.deinserver.de/bilder/"  # Ersetze durch den echten Pfad zum Bild-Ordner auf dem FTP-Server

# -----------------------
# Hilfsfunktionen
# -----------------------
@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    """Lädt die CSV-Datei und liefert einen DataFrame zurück.
    Erwartete Spaltennamen:
        Brand, ProductGroup, TemplateName, ImageFile, Language
    """
    if not path.exists():
        st.error(f"CSV-Datei {path} nicht gefunden.")
        st.stop()
    return pd.read_csv(path, dtype=str).fillna("")

# -----------------------
# Hauptanwendung
# -----------------------

def main():
    st.set_page_config(page_title="Template-Finder", page_icon="🗂️", layout="centered")

    # Sprache auswählen
    lang = st.radio("Sprache / Language", ["Deutsch", "English"], horizontal=True)
    is_german = lang == "Deutsch"

    title = "🗂️ Template-Finder" if is_german else "🗂️ Template Finder"
    st.title(title)

    intro_text = (
        "Wähle eine **Marke** und eine **Produktgruppe**, um die passenden Templates anzuzeigen."
        if is_german else
        "Select a **brand** and a **product group** to display the appropriate templates."
    )
    st.write(intro_text)

    df = load_data(DATA_FILE)

    # Nach Sprache filtern
    lang_code = "DE" if is_german else "EN"
    df = df[df["Language"] == lang_code]

    # 1. Marken-Auswahl
    brands = sorted(df["Brand"].unique())
    selected_brand = st.selectbox("Marke" if is_german else "Brand", brands, index=0)

    # 2. Produktgruppen gefiltert nach Marke
    filtered_by_brand = df[df["Brand"] == selected_brand]
    product_groups = sorted(filtered_by_brand["ProductGroup"].unique())
    selected_group = st.selectbox("Produktgruppe" if is_german else "Product Group", product_groups, index=0)

    # 3. Ergebnis-Templates
    result = filtered_by_brand[filtered_by_brand["ProductGroup"] == selected_group]

    st.divider()
    st.subheader("Gefundene Templates" if is_german else "Found Templates")

    if result.empty:
        st.info("Keine Templates gefunden." if is_german else "No templates found.")
    else:
        for _, row in result.iterrows():
            st.markdown(f"### {row['TemplateName']}")
            image_url = f"{FTP_IMAGE_BASE_URL}{row['ImageFile']}"
            st.image(image_url, use_column_width=True)

    st.divider()
    st.caption("© 2025 Digital Unit")


if __name__ == "__main__":
    main()
