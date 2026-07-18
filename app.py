import streamlit as st
import pandas as pd
from ge_design_kit import (
    inject_ge_styles, TOPBAR_SLOT_KEY, ge_topbar, ge_breadcrumb, ge_surface,
    ge_label_spacer, ICON_BUTTON_KEY_PREFIX, ge_kpi, ge_sidebar,
)

st.set_page_config(page_title="MemIA — POC GE-DESIGN", layout="wide")

# ── Polices + tokens + layout GE-DESIGN ──
inject_ge_styles()

# ── Bandeau GE plein-largeur, au-dessus de tout ──
# Wrappé dans un container à clé fixe pour que layout.py puisse
# collapser proprement son slot de flux.
with st.container(key=TOPBAR_SLOT_KEY):
    ge_topbar(app_name="GE", user_label="Mon compte")

# ── Logo MemIA (app) dans l'en-tête natif de la sidebar, à côté du collapse ──
st.logo("assets/memia_logo.svg", size="small")

# ── Etat de navigation simple ──
if "current_page" not in st.session_state:
    st.session_state.current_page = "operation"
# ── Compteur de sélection (placeholder — sera piloté par les cases à
# cocher du futur tableau d'opérations) ──
if "selected_count" not in st.session_state:
    st.session_state.selected_count = 0
# ── Drapeau de reset différé : on ne peut PAS écrire directement dans
# st.session_state.operations_table après que ce widget ait déjà été
# instancié dans le run courant (StreamlitAPIException). Le bouton
# "Annuler" s'exécute forcément APRÈS st.dataframe() dans le code (à
# cause du pattern st.empty(), cf. plus bas), donc on se contente de
# poser ce drapeau ici, et on applique le vrai reset tout en haut du
# PROCHAIN run — avant que le widget ne soit recréé. ──
if st.session_state.get("reset_operations_selection"):
    st.session_state.operations_table = {"selection": {"rows": []}}
    st.session_state.reset_operations_selection = False

# ── Sidebar native (position fixe, collapse natif) + composant à l'intérieur ──
with st.sidebar:
    selected = ge_sidebar(
        items=[
            {"id": "operation", "label": "Opération", "icon": "add_circle"},
            {"id": "configuration", "label": "Configuration", "icon": "settings"},
            {"id": "interpretation", "label": "Interprétation", "icon": "assignment", "has_children": True},
            {"id": "analyse", "label": "Analyse", "icon": "scatter_plot", "has_children": True},
            {"id": "verification", "label": "Vérification", "icon": "verified_user", "has_children": True},
            {"id": "recherche", "label": "Recherche", "icon": "search"},
        ],
        active_id=st.session_state.current_page,
        key="main_sidebar",
    )
    if selected:
        st.session_state.current_page = selected
        st.rerun()

# ── Contenu principal : plein-largeur (pas de st.columns pour la sidebar) ──
ge_breadcrumb(items=[
    {"id": "home", "label": "Accueil"},
    {"id": "operations", "label": "Sélectionner une opération"},
])
st.title("Sélectionner une opération")

# ── Tout le contenu de la page vit dans UNE seule carte GE-DESIGN ──
with ge_surface("operations"):
    st.subheader("Choisir la votation à analyser")

    with ge_surface("kpi-row", variant="inset"):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            ge_kpi(4, "Opérations disponibles", key="kpi_total")
        with c2:
            ge_kpi(2, "Analyses terminées", key="kpi_done")
        with c3:
            ge_kpi(1, "Analyse en cours", key="kpi_progress")
        with c4:
            ge_kpi(1, "Non démarrée", key="kpi_none")

        st.divider()

        # ── Ligne de filtres : widgets natifs, stylés via forms.py ──
        with st.container(key="ge-filter-row"):
            fc1, fc3, fc4, fc5, fc6 = st.columns([3.6, 1.3, 1.3, 1.3, 1.8])
            with fc1:
                # st.form lie le champ et le bouton : Entrée dans le champ
                # déclenche la même soumission qu'un clic sur le bouton
                with st.form(key="search-form", border=False):
                    ic1, ic2 = st.columns([5, 1])
                    with ic1:
                        search_term = st.text_input(
                            "Rechercher une opération",
                            placeholder="Rechercher une opération...",
                            key="op_search",
                        )
                    with ic2:
                        with st.container(key=f"{ICON_BUTTON_KEY_PREFIX}search"):
                            ge_label_spacer()
                            searched = st.form_submit_button("", icon=":material/search:")
                    if searched:
                        st.session_state.last_search = search_term
            with fc3:
                scrutin_type = st.selectbox(
                    "Type de scrutin",
                    options=["Tous", "Votation", "Élection"],
                    key="filter_scrutin",
                )
            with fc4:
                date_filter = st.selectbox(
                    "Date",
                    options=["Tous", "17.06.2025", "09.02.2025", "22.10.2025"],
                    key="filter_date",
                )
            with fc5:
                canal_filter = st.selectbox(
                    "Canal",
                    options=["Tous", "Correspondance", "Urne"],
                    key="filter_canal",
                )
            with fc6:
                show_done = st.toggle("Opérations terminées", value=True, key="filter_done")

    # ── Barre de sélection : réservée ICI visuellement ──
    selection_bar_slot = st.empty()

    # ── Tableau des opérations : st.dataframe natif avec sélection ──
    # réelle (checkboxes gérées par Streamlit, aucun CSS custom). ──
    operations_df = pd.DataFrame([
        {
            "Opération": "Votation fédérale", "Date": "17.06.2025",
            "Type de scrutin": "Votation", "Canal": "Correspondance",
            "Statut analyse": "🟢 Analysée", "Clusters": 3,
            "Dernière analyse": "18.06.2025 14h32",
        },
        {
            "Opération": "Votation cantonale", "Date": "17.06.2025",
            "Type de scrutin": "Votation", "Canal": "Urne",
            "Statut analyse": "🟢 Analysée", "Clusters": 0,
            "Dernière analyse": "18.06.2025 14h00",
        },
        {
            "Opération": "Votation communale", "Date": "17.06.2025",
            "Type de scrutin": "Votation", "Canal": "Correspondance",
            "Statut analyse": "🟡 En cours", "Clusters": None,
            "Dernière analyse": None,
        },
        {
            "Opération": "Votation fédérale", "Date": "17.06.2025",
            "Type de scrutin": "Votation", "Canal": "Urne",
            "Statut analyse": "⚪ Non démarrée", "Clusters": None,
            "Dernière analyse": None,
        },
        {
            "Opération": "Élection du Conseil d'État", "Date": "09.02.2025",
            "Type de scrutin": "Élection", "Canal": "Correspondance",
            "Statut analyse": "🟢 Analysée", "Clusters": 1,
            "Dernière analyse": "10.02.2025 09h15",
        },
        {
            "Opération": "Élection du Conseil national", "Date": "09.02.2025",
            "Type de scrutin": "Élection", "Canal": "Urne",
            "Statut analyse": "🟢 Analysée", "Clusters": 5,
            "Dernière analyse": "10.02.2025 11h20",
        },
        {
            "Opération": "Votation fédérale", "Date": "09.02.2025",
            "Type de scrutin": "Votation", "Canal": "Correspondance",
            "Statut analyse": "🟡 En cours", "Clusters": None,
            "Dernière analyse": None,
        },
        {
            "Opération": "Votation cantonale", "Date": "22.10.2025",
            "Type de scrutin": "Votation", "Canal": "Urne",
            "Statut analyse": "⚪ Non démarrée", "Clusters": None,
            "Dernière analyse": None,
        },
        {
            "Opération": "Élection municipale", "Date": "22.10.2025",
            "Type de scrutin": "Élection", "Canal": "Correspondance",
            "Statut analyse": "🟢 Analysée", "Clusters": 2,
            "Dernière analyse": "23.10.2025 08h45",
        },
        {
            "Opération": "Votation communale", "Date": "22.10.2025",
            "Type de scrutin": "Votation", "Canal": "Urne",
            "Statut analyse": "🟢 Analysée", "Clusters": 0,
            "Dernière analyse": "23.10.2025 10h05",
        },
    ])

    # ── Application des filtres de la ligne au-dessus (recherche/type/ ──
    # date/canal/toggle) sur les données AVANT de les passer au tableau. ──
    filtered_df = operations_df.copy()

    # Recherche : n'applique que le terme SOUMIS (via Entrée ou clic sur
    # la loupe, cf. st.form plus haut) — pas de filtrage à chaque frappe.
    search_value = st.session_state.get("last_search", "")
    if search_value:
        filtered_df = filtered_df[
            filtered_df["Opération"].str.contains(search_value, case=False, na=False)
        ]

    if scrutin_type != "Tous":
        filtered_df = filtered_df[filtered_df["Type de scrutin"] == scrutin_type]
    if date_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Date"] == date_filter]

    if canal_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Canal"] == canal_filter]

    # "Opérations terminées" OFF (défaut) : cache les opérations déjà
    # analysées — l'utilisateur voit d'abord ce qui demande son attention.
    if not show_done:
        filtered_df = filtered_df[~filtered_df["Statut analyse"].str.contains("Analysée")]

    display_df = filtered_df.drop(columns=["Type de scrutin", "Canal"])

    event = st.dataframe(
        display_df,
        key="operations_table",
        hide_index=True,
        width="stretch",
        on_select="rerun",
        selection_mode="multi-row",
        column_config={
            "Opération": st.column_config.TextColumn("Opération", width="large"),
            "Clusters": st.column_config.NumberColumn("Clusters", format="%d"),
        },
    )

    # event.selection.rows = index des lignes cochées sur CE run —
    # alimente à la fois le compteur affiché plus haut et l'état global
    # de sélection réutilisable ailleurs dans l'app (session_state).
    selected_rows = event.selection.rows
    st.session_state.selected_count = len(selected_rows)
    count = st.session_state.selected_count

    # ── Remplissage du placeholder réservé plus haut, avec le compte ──
    # à jour de CE run — même structure/CSS qu'avant, juste déplacée. ──
    with selection_bar_slot.container():
        with ge_surface("selection-bar", variant="inset"):
            with st.container(key="ge-selection-bar-row"):
                sb_left, sb_right = st.columns(2)
                with sb_left:
                    st.markdown(f"**Nombre d'opération(s) sélectionnée(s) : {count}**")
                    if st.button(
                        "Annuler la sélection",
                        icon=":material/close:",
                        type="tertiary",
                        disabled=(count == 0),
                        key="btn_clear_selection",
                    ):
                        # On ne peut pas modifier session_state.operations_table
                        # ICI (le widget a déjà été instancié plus haut dans ce
                        # run) — on pose juste le drapeau, le vrai reset aura
                        # lieu au tout début du PROCHAIN run (cf. haut du fichier).
                        st.session_state.reset_operations_selection = True
                        st.rerun()
                with sb_right:
                    with st.container(key="ge-button-group"):
                        st.button(
                            "Comparer",
                            type="secondary",
                            disabled=(count == 0),
                            key="btn_compare",
                        )
                        st.button(
                            "Exporter",
                            type="secondary",
                            disabled=(count == 0),
                            key="btn_export",
                        )

st.caption(f"Debug — page active : `{st.session_state.current_page}`")