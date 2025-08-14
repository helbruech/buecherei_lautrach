import streamlit as st
import pandas as pd
import os
import requests
from io import StringIO
from PIL import Image
from io import BytesIO


def load_original_data():
    url = 'https://raw.githubusercontent.com/helbruech/buecherei_lautrach/refs/heads/main/neuerwerbungen_2025-08-11_new.csv'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Failed to load data from GitHub.")
        return None

# --- Initiale Bücherliste nur einmal in Session State laden ---
if "books_list" not in st.session_state:
    df_csv_data = load_original_data()
    library = df_csv_data.to_dict('records')
    st.session_state.books_list = library

books_list = st.session_state.books_list

st.set_page_config(page_title="📚 Buchverwaltung", layout="wide")
st.title("📚 Buchverwaltung der Bücherei Lautrach")

# --- Suchfeld ---
search_term = st.text_input("🔍 Suchbegriff in allen Feldern")

def search_books(term):
    term = term.lower().strip()
    if not term:
        return books_list
    return [
        book for book in books_list
        if any(term in str(v).lower() for v in book.values())
    ]

matches = search_books(search_term)

# --- Session State für Navigation ---
if "current_book_index" not in st.session_state:
    st.session_state.current_book_index = 0

# Index begrenzen (z. B. wenn sich Trefferanzahl geändert hat)
st.session_state.current_book_index = min(st.session_state.current_book_index, max(0, len(matches) - 1))

# --- Navigation-Buttons ---
col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
with col_nav1:
    if st.button("⬅️ Vorheriges Buch"):
        st.session_state.current_book_index = max(0, st.session_state.current_book_index - 1)
with col_nav3:
    if st.button("Nächstes Buch ➡️"):
        st.session_state.current_book_index = min(len(matches) - 1, st.session_state.current_book_index + 1)

# --- Auswahl per Selectbox (optional zusätzlich) ---
with col_nav2:
    if matches:
        selected_isbn = st.selectbox(
            "Buch auswählen",
            [b["ISBN"] for b in matches],
            index=st.session_state.current_book_index,
            format_func=lambda isbn: next((b["00_Kurztitel"] for b in matches if b["ISBN"] == isbn), ""),
            key="book_select"
        )
        # Falls Selectbox geändert wird → Index aktualisieren
        if selected_isbn:
            new_index = next((i for i, b in enumerate(matches) if b["ISBN"] == selected_isbn), st.session_state.current_book_index)
            st.session_state.current_book_index = new_index
    else:
        selected_isbn = None

# --- Layout: Links Auswahl, Rechts Bearbeitung ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Suchtreffer")

    # CSV-Speichern-Button
    if st.button("💾 Buchbestand auf Disk speichern"):
        pd.DataFrame(books_list).to_csv("books_list.csv", index=False, encoding="utf-8")
        st.success("📂 Bücherliste gespeichert als books_list.csv")

    if selected_isbn:
        book = next((b for b in books_list if b["ISBN"] == selected_isbn), None)
        if book:
            cover_url = "https://portal.dnb.de/opac/mvb/cover?isbn={book['ISBN']}&size=m"
            response = requests.get(cover_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=f"ISBN: {book['ISBN']}", use_container_width=True)
            else:
                st.info("Kein Cover vorhanden.")

with col2:
    st.subheader("✏️ Buch bearbeiten")

    if selected_isbn:
        book = next((b for b in books_list if b["ISBN"] == selected_isbn), None)
        if book:
            autor = st.text_input("Autor", value=book.get("00_Erstautor", ""))
            titel = st.text_input("Titel", value=book.get("00_Kurztitel", ""))
            isbn = st.text_input("ISBN Nummer", value=book.get("ISBN", ""))
            jahr = st.text_input("Erscheinungsjahr", value=str(book.get("00_Erscheinungsjahr", "")))
            sachgruppe = st.text_input("Sachgruppe", value=book.get("00_Sachgruppe", ""))
            aufgenommen = st.text_input("In Bestand aufgenommen im Jahr", value=book.get("aufgenommen", ""))
            aussortiert = st.text_input("Aussortiert im Jahr", value=book.get("aufgenommen", ""))
            preis = st.text_input("Preis", value=book.get("00_Preis", ""))
            kommentar = st.text_input("Kommentar", value=book.get("Kommentar", ""))

            if st.button("💾 Änderungen speichern"):
                book.update({
                    "00_Erstautor": autor,
                    "00_Kurztitel": titel,
                    "ISBN": isbn,
                    "00_Erscheinungsjahr": jahr,
                    "00_Sachgruppe": sachgruppe,
                    "aufgenommen": aufgenommen,
                    "aussortiert": aussortiert,
                    "preis": preis,
                    "Kommentar": kommentar
                })
                st.success("✅ Änderungen übernommen (nicht vergessen: Buchbestand auf Disk speichern!)")
