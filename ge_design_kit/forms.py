"""
ge_design_kit.forms
---------------------
Styles CSS pour les widgets Streamlit NATIFS (text_input, selectbox,
toggle, button) — pas de composant CCv2 ici.
"""

import streamlit as st

# Préfixe pour les boutons "icône seule" (ex: bouton recherche rond) —
# même pattern de convention que SURFACE_VARIANTS dans surface.py.
ICON_BUTTON_KEY_PREFIX = "ge-btn-icon-"

# Dimensions du toggle (rail + curseur) — ajustables directement ici.
TOGGLE_TRACK_WIDTH_PX = 44
TOGGLE_TRACK_HEIGHT_PX = 24
TOGGLE_THUMB_SIZE_PX = 20

FORMS_CSS = f"""
[data-testid="stTextInputRootElement"] {{
    border-radius: var(--md-sys-shape-corner-extra-small) !important;
    border: 1px solid var(--md-sys-color-outline) !important;
    background: var(--md-sys-color-surface) !important;
    box-shadow: 0 1px 2px 0 rgba(18, 18, 23, 0.05) !important;
    height: 56px !important;
    padding: 0 calc(var(--spacing) * 3) !important;
    display: flex !important;
    align-items: center !important;
    align-self: stretch !important;
}}
[data-testid="stTextInputRootElement"] input[type="text"] {{
    background: transparent !important;
    border: none !important;
    height: 100% !important;
    font-size: 16px !important;
}}
[data-testid="stTextInputRootElement"]:focus-within {{
    border-color: var(--md-sys-color-primary) !important;
    box-shadow: 0 0 0 1px var(--md-sys-color-primary) !important;
}}
[data-testid="stSelectbox"] .react-aria-ComboBox [role="group"] {{
    border-radius: var(--md-sys-shape-corner-extra-small) !important;
    border: 1px solid var(--md-sys-color-outline) !important;
    background: var(--md-sys-color-surface) !important;
    box-shadow: 0 1px 2px 0 rgba(18, 18, 23, 0.05) !important;
    height: 56px !important;
    padding: 0 calc(var(--spacing) * 3) !important;
    display: flex !important;
    align-items: center !important;
    align-self: stretch !important;
}}
[data-testid="stSelectbox"] .react-aria-ComboBox [role="group"] input[role="combobox"] {{
    font-size: 16px !important;
}}
[class*="st-key-{ICON_BUTTON_KEY_PREFIX}"] button {{
    border-radius: var(--md-sys-shape-corner-full) !important;
    background: var(--md-sys-color-primary) !important;
    border: none !important;
    width: 56px !important;
    height: 56px !important;
    padding: 0 !important;
    min-width: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
}}
[class*="st-key-{ICON_BUTTON_KEY_PREFIX}"] button * {{
    color: var(--md-sys-color-on-primary) !important;
    font-size: 1.5rem;
}}
[data-testid="stCheckbox"] label > div:first-of-type {{
    width: {TOGGLE_TRACK_WIDTH_PX}px !important;
    height: {TOGGLE_TRACK_HEIGHT_PX}px !important;
}}
[data-testid="stCheckbox"] label > div:first-of-type > div {{
    width: {TOGGLE_THUMB_SIZE_PX}px !important;
    height: {TOGGLE_THUMB_SIZE_PX}px !important;
}}
[data-testid="stCheckbox"] label {{
    align-items: center !important;
}}
.st-key-ge-filter-row [data-testid="stHorizontalBlock"] {{
    align-items: center !important;
}}
.st-key-ge-search-form {{
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}}
.st-key-ge-surface-inset-selection-bar button {{
    border-radius: 30px !important;
    padding: 0 1rem;
}}
.st-key-ge-surface-inset-selection-bar button:disabled {{
    border: 1px solid var(--md-sys-color-state-opacity-12, rgba(0, 51, 85, 0.12)) !important;
}}
.st-key-ge-selection-bar-row [data-testid="stHorizontalBlock"] {{
    justify-content: space-between !important;
}}
.st-key-ge-selection-bar-row [data-testid="stColumn"] {{
    flex: 0 1 auto !important;
    width: auto !important;
}}
.st-key-ge-button-group {{
    display: flex !important;
    flex-direction: row !important;
    gap: calc(var(--spacing) * 2) !important;
    align-items: center !important;
}}
"""


def ge_label_spacer(height_px: int = 10):
    """
    Espaceur invisible de la hauteur d'un label de widget Streamlit
    (10px par défaut, calibré visuellement).
    """
    st.html(f'<div style="height:{height_px}px;"></div>')