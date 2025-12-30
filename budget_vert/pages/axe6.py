import streamlit as st
import pandas as pd
from pathlib import Path

# Configuration de la page
st.set_page_config(page_title="Budget vert - Axe 6")

# Titre et description
st.title("🌱 Budget Vert - Axe 6 : Préservation de la biodiversité et la protection des espaces naturels")
st.markdown("""
Cet outil utilise un **arbre de décision** basé sur le tableau synthèse page 16-17 de l'**Annexe technique "Biodiversité"** de l'I4CE. N'hésitez pas à consulter cette annexe pour plus de détails.

Répondez aux questions pour obtenir le classement de votre dépense.
""")

st.subheader("Questionnaire")

# Dictionnaire des rubriques et de leurs questions/réponses
rubriques = {
    "Changement d'usage des terres et des mers": {
        "question": "Quel est l'impact de la dépense sur le changement d'usage des terres ou des mers ?",
        "options": {
            "Dépense visant un impact favorable direct sur la biodiversité, permanent et gain écologique.": "Très favorable",
            "Impact indirect favorable sur la biodiversité, ou actions de sensibilisation sur le changement d'usage des terres ou des mers.": "Favorable sous conditions",
            "Dépense n'ayant pas d'impact direct sur le changement d'usage des sols ou des mers.": "Neutre",
            "Dépense incompatible avec l'objectif Zéro artificialisation nette ou générant une reformulation du milieu.": "Défavorable",
            "Dépense ne pouvant être classée en raison d'un manque d'information.": "À approfondir"
        }
    },
    "Surexploitation des ressources naturelles": {
        "question": "Quel est l'impact de la dépense sur la surexploitation des ressources naturelles ?",
        "options": {
            "Dépense visant à améliorer la qualité ou la quantité de la ressource naturelle, ou à éviter sa dégradation.": "Très favorable",
            "Dépense permettant un impact indirect bénéfique sur les stocks de ressources naturelles.": "Favorable sous conditions",
            "Dépense n'ayant pas d'impact direct sur l'exploitation des ressources naturelles.": "Neutre",
            "Dépense conduisant à une altération de la qualité ou de la quantité de la ressource naturelle.": "Défavorable",
            "Dépense ne pouvant être classée en raison d'un manque d'information.": "À approfondir"
        }
    },
    "Pollutions": {
        "question": "Quel est l'impact de la dépense sur les pollutions ?",
        "options": {
            "Dépense permettant une dépollution effective et durable.": "Très favorable",
            "Dépense permettant une réduction indirecte des niveaux de pollution.": "Favorable sous conditions",
            "Dépense n'ayant pas d'impact direct sur les pollutions.": "Neutre",
            "Dépense conduisant à une augmentation des niveaux de pollution.": "Défavorable",
            "Dépense ne pouvant être classée en raison d'un manque d'information.": "À approfondir"
        }
    },
    "Espèces exotiques envahissantes": {
        "question": "Quel est l'impact de la dépense sur les espèces exotiques envahissantes ?",
        "options": {
            "Dépense pour des actions curatives contre les espèces exotiques envahissantes.": "Très favorable",
            "Dépense pour des actions préventives, sensibilisation, études.": "Favorable sous conditions",
            "Dépense n'ayant pas d'impact direct sur les espèces exotiques envahissantes.": "Neutre",
            "Dépense conduisant à une dégradation de la biodiversité due à l'introduction d'espèces exotiques envahissantes.": "Défavorable",
            "Dépense ne pouvant être classée en raison d'un manque d'information.": "À approfondir"
        }
    }
}

# Initialisation des résultats dans la session
if "resultats" not in st.session_state:
    st.session_state.resultats = {}

# Parcours des rubriques
for rubrique, details in rubriques.items():
    #st.subheader(f"{rubrique}")
    question = details["question"]
    options = list(details["options"].keys())

    # Sélection de l'utilisateur
    choix = st.selectbox(
        question,
        options,
        key=f"select_{rubrique}"
    )

    # Classement pour cette rubrique
    classement = details["options"][choix]
    st.session_state.resultats[rubrique] = {
        "choix": choix,
        "classement": classement
    }


# Récapitulatif global
st.markdown(" ")
st.subheader("📊 Cotation global")
st.write("**Résumé des impacts par facteur :**")
impacts = []
for rubrique, resultat in st.session_state.resultats.items():
    st.write(f"- **{rubrique}** : {resultat['classement']}")
    impacts.append(resultat["classement"])

# Logique pour déterminer l'impact global
def determiner_impact_global(impacts):
    # Vérifie si tous les impacts sont "Très favorable" ou "Favorable sous conditions" ou "Neutre"
    if all(impact in ["Très favorable", "Favorable sous conditions", "Neutre"] for impact in impacts):
        if any(impact in ["Favorable sous conditions"] for impact in impacts):
            return "Favorable sous conditions"
        elif any(impact in ["Très favorable"] for impact in impacts):
            return "Favorable"
        else:
            return "Neutre"
    # Vérifie si tous les impacts sont "Défavorable" ou "Neutre"
    elif all(impact in ["Défavorable", "Neutre"] for impact in impacts):
        if any(impact == "Défavorable" for impact in impacts):
            return "Défavorable"
        else:
            return "Neutre"
    # Vérifie si les impacts sont mixtes (au moins un "Très favorable" ou "Favorable sous conditions" ET au moins un "Défavorable")
    elif any(impact in ["Très favorable", "Favorable sous conditions"] for impact in impacts) and any(impact == "Défavorable" for impact in impacts):
        return "Mixte"
    # Si tous les impacts sont "Neutre"
    elif all(impact == "Neutre" for impact in impacts):
        return "Neutre"
    # Cas par défaut (si des impacts sont "À approfondir", on ne peut pas trancher)
    else:
        return "à approfondir"

impact_global = determiner_impact_global(impacts)

# Affichage de l'impact global
if impact_global == "Favorable":
    st.success("✅ Impact global **Favorable** : Cette dépense a un impact positif sur la biodiversité.")
elif impact_global == "Favorable sous conditions":
    st.success("⚠️ Impact global **Favorable sous conditions** : Cette dépense a un impact positif sur la biodiversité, mais sous certaines conditions.")
elif impact_global == "Défavorable":
    st.error("❌ Impact global **Défavorable** : Cette dépense a un impact négatif sur la biodiversité.")
elif impact_global == "Mixte":
    st.warning("⚠️ Impact global **Mixte** : Cette dépense a des impacts à la fois positifs et négatifs sur la biodiversité.")
elif impact_global == "Neutre":
    st.info("ℹ️ Impact global **Neutre** : Cette dépense n'a pas d'effet significatif sur la biodiversité.")
else:
    st.warning("🔍 Impact global **À approfondir** : Une analyse complémentaire est nécessaire.")
st.markdown(" ")
st.subheader("Tableau synthèse")
# Afficher image illustrative
BASE_DIR = Path(__file__).resolve().parent
image_path = BASE_DIR / "images" / "biodiversite.png"

st.image(image_path)
