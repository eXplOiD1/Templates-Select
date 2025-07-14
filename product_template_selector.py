import pandas as pd
import streamlit as st
from pathlib import Path

# -----------------------
# Konfiguration
# -----------------------
DATA_FILE = Path(__file__).with_name("templates.csv")  # erwartet eine CSV in demselben Ordner wie dieses Skript

# -----------------------
# Hilfsfunktionen
# -----------------------
@st.cache_data(show_spinner=False)
def load_data(path: Path) -> pd.DataFrame:
    """Lädt die CSV-Datei und liefert einen DataFrame zurück.
    Erwartete Spaltennamen:
        Brand, ProductGroup, TemplateName, TemplateContent
    """
    if not path.exists():
        st.error(f"CSV-Datei {path} nicht gefunden.")
        st.stop()
    return pd.read_csv(path, dtype=str).fillna("")

# -----------------------
# Hauptanwendung
# -----------------------

def main():
    st.set_page_config(page_title="Template‑Finder", page_icon="🗂️", layout="centered")
    st.title("🗂️ Template‑Finder")
    st.write("Wähle eine **Marke** und eine **Produktgruppe**, um die passenden Templates anzuzeigen.")

    df = load_data(DATA_FILE)

    # 1. Marken‑Auswahl
    brands = sorted(df["Brand"].unique())
    selected_brand = st.selectbox("Marke auswählen", brands, index=0)

    # 2. Produktgruppen gefiltert nach Marke
    filtered_by_brand = df[df["Brand"] == selected_brand]
    product_groups = sorted(filtered_by_brand["ProductGroup"].unique())
    selected_group = st.selectbox("Produktgruppe auswählen", product_groups, index=0)

    # 3. Ergebnis‑Templates
    result = filtered_by_brand[filtered_by_brand["ProductGroup"] == selected_group]

    st.divider()
    st.subheader("Gefundene Templates")

    if result.empty:
        st.info("Für diese Kombination wurden keine Templates gefunden.")
    else:
        for _, row in result.iterrows():
            st.markdown(f"### {row['TemplateName']}")
            # Anzeige des Template‑Inhalts (hier als Code‑Block, kann angepasst werden)
            st.code(row["TemplateContent"], language="html")
            # Optionaler Download‑Button pro Template
            st.download_button(
                label="Template herunterladen",
                data=row["TemplateContent"],
                file_name=f"{row['TemplateName']}.html",
                mime="text/html",
            )

    st.divider()
    st.caption("© 2025 Digital Unit – Streamlit‑App zum schnellen Finden von Vorlagen.")


if __name__ == "__main__":
    main()
