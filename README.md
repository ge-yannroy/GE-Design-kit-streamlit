# GE-DESIGN-KIT pour Streamlit

Composants réutilisables pour habiller une app Streamlit aux couleurs et à la typographie **GE-DESIGN**.

---

## Installation

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Le kit n'est pas un package pip, copier le dossier `ge_design_kit/`, `assets/` et `.streamlit/config.toml` tels quels à la racine du projet, à côté du fichier `app.py`.

⚠️ Nécessite une version **récente** de Streamlit (Custom Components v2). En cas d'erreur liée à `st.components.v2` : `pip install --upgrade streamlit`.

---

## Démarrage rapide

```python
import streamlit as st
from ge_design_kit import inject_ge_styles, ge_topbar, TOPBAR_SLOT_KEY

st.set_page_config(page_title="Mon app", layout="wide")

inject_ge_styles()  # polices + tokens + CSS, 1 seul appel, tout en haut

with st.container(key=TOPBAR_SLOT_KEY):
    ge_topbar(app_name="GE", user_label="Mon compte")

st.logo("assets/mon_logo.svg", size="small")
```

À partir de là : composants `ge_*` et widgets Streamlit natifs (`st.text_input`, `st.selectbox`, `st.button`, `st.toggle`) sont stylés GE-DESIGN automatiquement. Voir `app.py` pour un exemple complet et fonctionnel (sidebar, breadcrumb, cartes, tableau, filtres).

**`.streamlit/config.toml` est obligatoire**, sans lui, les composants `ge_*` restent stylés mais les widgets natifs (titres, boutons...) gardent l'apparence Streamlit par défaut.

---

## Composants

| Composant | Rôle | Paramètres clés | Retour |
|---|---|---|---|
| `inject_ge_styles()` | Charge tout (polices/tokens/layout). À appeler 1x, tout en haut. | - | - |
| `ge_topbar(app_name, user_label)` | Bandeau institutionnel fixe en haut. À wrapper dans `st.container(key=TOPBAR_SLOT_KEY)`. | `app_name="GE"`, `user_label="Mon compte"` | - |
| `ge_sidebar(items, title, active_id, key)` | Menu latéral. À utiliser dans `with st.sidebar:`. | `items`: `[{"id","label","icon","has_children"?}]` ou `{"divider":True}` | id cliqué ou `None` |
| `ge_breadcrumb(items, key)` | Fil d'Ariane, dernier item = page courante (non cliquable). | `items`: `[{"id","label"}]` | id cliqué ou `None` |
| `ge_surface(key, variant)` | Conteneur de page, peut contenir n'importe quel widget (contrairement à `ge_card`). | `variant="card"` (blanc+ombre) ou `"inset"` (teinté, sans ombre) | context manager |
| `ge_card(title, content, icon, button_label, key)` | Card figée (titre+texte+bouton). Composant CCv2, ne peut pas contenir d'autres widgets. | tous optionnels sauf `title`/`content` | `True` si bouton cliqué |
| `ge_kpi(value, label, key)` | KPI card simple, sans interaction. | tous requis | - |
| `ge_label_spacer(height_px=10)` | Aligne un bouton sans label avec des champs voisins labellisés. | - | - |
| `ICON_BUTTON_KEY_PREFIX` | Constante, wrapper un bouton dans `st.container(key=f"{PREFIX}xxx")` pour un style icône ronde. | - | - |

Icônes : nom **Material Symbols** (ex: `"search"`), pas d'emoji, liste sur [fonts.google.com/icons](https://fonts.google.com/icons).

Détails complets de chaque fonction (docstrings) directement dans le code source de `ge_design_kit/`.

---

## Widgets natifs stylés automatiquement

Une fois `inject_ge_styles()` appelé : `st.text_input`, `st.selectbox`, `st.toggle`, `st.button`/`st.form_submit_button` (types `"secondary"`/`"tertiary"`), titres (`st.title`, `#`/`##`/`###`).

**Non stylable** : `st.dataframe` (rendu sur `<canvas>`, pas de CSS possible.

---

## Pièges à connaître (pour étendre le kit)

- **Jamais de `<balise>` littérale dans un commentaire CSS** , tout passe par `st.html()` → DOMPurify, qui peut interpréter le contenu d'un commentaire comme du vrai HTML et casser tout le CSS qui suit.
- **`st.markdown(unsafe_allow_html=True)` casse sur les lignes vides** , préférer `st.html()` pour du CSS/HTML multi-lignes.
- **Ne jamais cibler les classes `st-emotion-cache-*`** (instables, régénérées à chaque build) , chercher un `data-testid` ou un rôle ARIA stable à la place.
- **`st.container(key="...")`** génère une classe `.st-key-<key>` , le moyen fiable de cibler un élément précis en CSS.
- **`height:100%` casse si un seul niveau de la chaîne de parents n'a pas de hauteur définie** , Streamlit imbrique beaucoup de wrappers ; en cas de doute, préférer une hauteur fixe calibrée visuellement.
- **On ne peut pas modifier `st.session_state[key]` après instanciation du widget dans le run courant** , pour un reset programmatique, poser un drapeau et l'appliquer au début du run suivant.

---

## Ressources

[Docs Streamlit](https://docs.streamlit.io) · [Custom Components v2](https://docs.streamlit.io/develop/concepts/custom-components/components-v2) · [Material Symbols](https://fonts.google.com/icons)