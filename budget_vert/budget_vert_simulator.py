import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Outil de Classement I4CE", layout="wide")

# Titre et description
st.title("🌱 Outil de catégorisation des dépenses - Axe 1 Budget Vert (I4CE)")
st.markdown("""
Cet outil utilise un **arbre de décision complet** basé sur le **tableau de synthèse des critères de classement par rubriques** (page 18 du guide I4CE).
**Instructions** : Sélectionnez une rubrique et répondez aux questions pour obtenir le classement de votre dépense.
""")

# Arbre de décision complet (basé sur le tableau de synthèse I4CE)
arbre_decision = {
    "Bâtiment": {
        "Sous-rubrique": {
            "Construction de nouveaux bâtiments": {
                "Performance énergie-carbone": {
                    "Supérieure aux normes (RE2020) ou niveau C1 (E+C-)": {
                        "Artificialisation des sols": {
                            "Pas d'artificialisation": "100 % Très favorable (dépassement des normes)",
                            "Artificialisation supplémentaire": "Partie dépassement des normes : Très favorable | Reste : Défavorable (artificialisation)"
                        }
                    },
                    "Conforme aux normes (RE2020/RT2012)": {
                        "Artificialisation des sols": {
                            "Pas d'artificialisation": "100 % Favorable sous conditions",
                            "Artificialisation supplémentaire": "100 % Défavorable"
                        }
                    },
                    "Inférieure aux normes": "100 % Défavorable"
                }
            },
            "Rénovation des bâtiments": {
                "Type de rénovation": {
                    "Performance énergétique (classe A/B DPE)": "100 % Très favorable",
                    "Amélioration partielle (saut de classe ou -30% consommation)": "100 % Favorable sous conditions",
                    "Sans amélioration énergétique": {
                        "Bâtiment déjà performant (classe A/B)": "100 % Neutre",
                        "Bâtiment non performant": "100 % Occasion manquée"
                    }
                }
            }
        }
    },
    "Transports et infrastructures": {
        "Sous-rubrique": {
            "Transports ferroviaires (tramway, train)": {
                "Type d'investissement": {
                    "Matériel roulant": {
                        "Motorisation": {
                            "Électrique/bioGNV/hydrogène décarboné": "100 % Très favorable",
                            "Hybride/GNV/bi-mode": "100 % Favorable sous conditions",
                            "Diesel/essence": "100 % Défavorable"
                        }
                    },
                    "Infrastructures": {
                        "Type": {
                            "Électrification": "100 % Très favorable",
                            "Non-électrique (modernisation)": "100 % Favorable sous conditions"
                        }
                    }
                }
            },
            "Transports collectifs routiers (bus)": {
                "Type d'investissement": {
                    "Matériel roulant": {
                        "Motorisation": {
                            "Électrique/bioGNV/hydrogène décarboné": "100 % Très favorable",
                            "Hybride/GNV": "100 % Favorable sous conditions",
                            "Diesel/essence": "100 % Défavorable"
                        }
                    }
                }
            },
            "Voirie": {
                "Type de travaux": {
                    "Construction": {
                        "Usage": {
                            "Mobilités douces (piste cyclable, trottoir)": "100 % Très favorable",
                            "Voie automobile": "100 % Défavorable",
                            "Mixte": "À répartir au prorata des surfaces (Très favorable pour mobilités douces | Défavorable pour voies automobiles)"
                        }
                    },
                    "Entretien": {
                        "Partie concernée": {
                            "Mobilités douces": "100 % Très favorable",
                            "Voies automobiles": "100 % Neutre"
                        }
                    }
                }
            }
        }
    },
    "Énergie": {
        "Sous-rubrique": {
            "Achats d'énergie": {
                "Type d'énergie": {
                    "Électricité (garantie d'origine renouvelable)": "100 % Très favorable",
                    "Électricité (standard)": "100 % Neutre",
                    "Gaz naturel fossile": "100 % Défavorable",
                    "Gaz renouvelable (biométhane)": "100 % Très favorable"
                }
            },
            "Infrastructures énergétiques": {
                "Type": {
                    "Production d'électricité renouvelable": "100 % Très favorable",
                    "Production de gaz renouvelable": "100 % Très favorable",
                    "Réseaux (électricité/gaz)": {
                        "Usage": {
                            "Raccordement EnR": "100 % Très favorable",
                            "Standard": "100 % Neutre"
                        }
                    }
                }
            }
        }
    },
    "Agriculture": {
        "Sous-rubrique": {
            "Aides aux exploitations": {
                "Pratiques agricoles": {
                    "Transition agroécologique (ex. : AB)": "100 % Très favorable",
                    "HVE ou pratiques partielles": "100 % Favorable sous conditions",
                    "Pas de transition": "100 % Défavorable"
                }
            },
            "Circuits courts": {
                "Pratiques de production": {
                    "Transition agroécologique (filière en croissance)": "100 % Très favorable",
                    "Transition agroécologique (filière en déclin)": "100 % Favorable sous conditions",
                    "Pas de transition": "100 % Défavorable"
                }
            }
        }
    },
    "Espaces verts": {
        "Sous-rubrique": {
            "Investissement/entretien": {
                "Type d'espace": {
                    "Espaces arborés": "100 % Très favorable",
                    "Autres espaces verts": "100 % Neutre"
                }
            }
        }
    },
    "Déchets": {
        "Sous-rubrique": {
            "Gestion des déchets": {
                "Type de traitement": {
                    "Prévention/réemploi/valorisation matière": "100 % Très favorable",
                    "Valorisation énergétique": "100 % Favorable sous conditions",
                    "Enfouissement/incinération": "100 % Défavorable"
                }
            }
        }
    },
    "Achats et entretien de véhicules": {
        "Sous-rubrique": {
            "Véhicules légers (voitures, VUL)": {
                "Émissions": {
                    "< 50 gCO₂/km": "100 % Très favorable",
                    "> 50 gCO₂/km": "100 % Défavorable"
                }
            },
            "Poids lourds": {
                "Motorisation": {
                    "Électrique": "100 % Très favorable",
                    "Gaz/hybride": "100 % Favorable sous conditions",
                    "Diesel/essence": "100 % Défavorable"
                }
            }
        }
    }
}

titres = ["Sous-rubrique", "Type", "Usage", "Partie concernée", "Motorisation", "Pratiques agricoles",
          "Performance énergie-carbone","Artificialisation des sols","Type de rénovation","Émissions"
          "Type de traitement","Type d'espace","Pratiques de production","Type d'énergie","Type de travaux",
          "Entretien", "Type d'investissement"]


def parcourir_arbre(noeud, chemin):
    # Si le noeud est une chaîne, c'est la fin
    if isinstance(noeud, str):
        return noeud

    # Si le noeud est un dictionnaire
    if isinstance(noeud, dict):
        # Filtrer les clés "titre" pour descendre directement
        for titre in titres:
            if titre in noeud:
                return parcourir_arbre(noeud[titre], chemin)

        # Sinon, proposer les clés comme options
        options = list(noeud.keys())
        question = st.selectbox("Choisissez :", options)
        chemin.append(question)
        return parcourir_arbre(noeud[question], chemin)




# Initialisation de la session
if "etapes" not in st.session_state:
    st.session_state.etapes = []
if "classement" not in st.session_state:
    st.session_state.classement = None

# Sélection de la rubrique principale
st.subheader("1. Sélectionnez la rubrique principale")
rubrique = st.selectbox("Rubrique", list(arbre_decision.keys()))

# Parcours de l'arbre
if rubrique in arbre_decision:
    st.session_state.etapes = [rubrique]
    try:
        classement = parcourir_arbre(arbre_decision[rubrique], st.session_state.etapes)
        st.session_state.classement = classement

        # Affichage du résultat
        st.subheader("2. Résultat du classement")
        st.write(f"**Classement :** {st.session_state.classement}")
        st.write(f"**Chemin de décision :** {' → '.join(st.session_state.etapes)}")

        # Explications supplémentaires
        if("Très favorable" or "Favorable") and "Défavorable" in st.session_state.classement: 
            st.warning("⚠️ **Impact mixte** : Cette dépense a des impacts positifs et négatifs.")
        elif "Très favorable" in st.session_state.classement:
            st.success("✅ **Impact positif fort** : Cette dépense réduit significativement les émissions de GES.")
        elif "Favorable sous conditions" in st.session_state.classement:
            st.success("⚠️ **Impact positif limité** : Cette dépense améliore la performance, mais sous conditions.")
        elif "Défavorable" in st.session_state.classement:
            st.error("❌ **Impact négatif** : Cette dépense augmente les émissions de GES.")
        elif "Neutre" in st.session_state.classement:
            st.info("ℹ️ **Impact neutre** : Cette dépense n'a pas d'effet significatif sur les émissions.")
        elif "Occasion manquée" in st.session_state.classement:
            st.warning("⚠️ **Opportunité non saisie** : Cette dépense aurait pu inclure des améliorations énergétiques.")

        else:
            st.write("🔍 **À approfondir** : Analyse complémentaire nécessaire.")

    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")