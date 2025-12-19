import streamlit as st
import pandas as pd
from pathlib import Path

# Configuration de la page
st.set_page_config(page_title="Outil de Classement I4CE")

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
            },
            "Entretien et maintenance de bâtiments et d'infrastructures": {
                "Opérations avec économie d'énergie ou décarbonation du mix énergétique prouvé": "100% Favorable sous conditions",
                "Opérations classiques": "100% Neutre"
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
            "Transports routiers non collectifs": {
                "Type d'investissement": {
                    "Achat de véhicules": {
                        "Type de véhicules": {
                            "Véhicules légers": {
                                "Motorisation": {
                                    "Moins de 50 gCO2/km": "100 % Très favorable",
                                    "Plus de 50 gCO2/km": "100 % Défavorable"
                                }
                            },
                            "Poids lourds": {
                                "Motorisation": {
                                    "Électrique/bioGNV/hydrogène décarboné": "100 % Très favorable",
                                    "Hybride/Gaz": "100 % Favorable sous conditions",
                                    "Diesel/essence": "100 % Défavorable"
                                }
                            },
                            "Deux roues": {
                                "Motorisation": {
                                    "Électrique ou actif": "100 % Très favorable",
                                    "Fossiles": "100 % Défavorable"
                                }
                            }
                        }
                    },
                    "Entretien de véhicules": {
                        "Type de véhicules": {
                            "Voiture": {
                                "Motorisation": {
                                    "Moins de 50 gCO2/km": "100 % Très favorable",
                                    "Plus de 50 gCO2/km": "100 % Neutre"
                                }
                            },
                            "Utilitaire/Camion": {
                                "Motorisation": {
                                    "Électrique/bioGNV/hydrogène décarboné/hybride": "100 % Très favorable",
                                    "Diesel/essence": "100 % Neutre"
                                }
                            },
                            "Deux roues": {
                                "Motorisation": {
                                    "Électrique ou actif": "100 % Très favorable",
                                    "Fossiles": "100 % Neutre"
                                }
                            }
                        }
                    }
                }
            },
            "Voirie": {
                "Type de travaux": {
                    "Construction": {
                        "Type de mobilités favorisées": {
                            "Piétons, vélos, transports en commun 100% décarbonnés": "100 % Très favorable",
                            "Transports en commun non décarbonnés": "100 % Favorable sous conditions",
                            "Voitures": "100 % Défavorable"
                        }
                    },
                    "Entretien/Requalification": {
                        "Type de mobilités favorisées": {
                            "Voies piétons, vélos, transports en commun 100% décarbonnés": "100 % Très favorable",
                            "Voies automobiles": "100 % Neutre"
                        }
                    },
                    "Exploitation": {
                        "Type de mobilités favorisées": {
                            "Voies piétons, vélos, transports en commun, mobilités bas carbone": "100 % Très favorable",
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
                    "Gaz renouvelable (biométhane)": "100 % Très favorable",
                    "Agrocarburants": "100 % À approfondir",
                    "Pétrole, charbon": "100 % Défavorable"
                }
            },
            "Infrastructures énergétiques": {
                "Type": {
                    "Infrastructures de production d'énergie (hors énergies renouvelables agricoles)": {
                        "Production d'électricité renouvelable": "100 % Très favorable",
                        "Production de gaz renouvelable": "100 % Très favorable",
                        "Agrocarburants": "100 % À approfondir",
                        "Pétrole, charbon": "100 % Défavorable"
                    },
                    "Réseaux de distribution d'énergie": {
                        "Transport et distribution d'électricité": {
                            "Électricité renouvelable": "100 % Très favorable",
                            "Électricité": "100 % Neutre"
                        },
                        "Transport et distribution de gaz": {
                            "Gaz renouvelable": "100 % Très favorable",
                            "Gaz": "100 % Neutre"
                        },
                        "Réseaux de chaleur/froid": {
                            "Proxy : part d'énergies renouvelables": "100 % Très favorable",
                            "Proxy : part d'énergies de co-génération": "100 % Favorable sous conditions",
                            "Proxy : part d'énergies fossiles": "100 % Défavorable"
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
                    "Encourageant la transition agroécologique (filières devant croître)": "100 % Très favorable",
                    "Encourageant la transition agroécologique (filières devant décroître)": "100 % Favorable sous conditions",
                    "N'entraînant pas de changement dans les pratiques agricoles": "100 % Défavorable"
                },
                "Actions d'efficacité énergétique des exploitations": {
                    "Économies d'énergie ou décarbonation du mixe prouvées": "100 % Favorable sous conditions",
                    "Serres chauffées, ou bâtiments d'élevage d'une exploitation sans pratiques de transition agroécologique": "100 % Défavorable"
                },
                "Construction/modernisation de bâtiments (hors efficacité énergétique)": {
                    "Facilitant la transition agroécologique (filières devant croître)": "100 % Très favorable",
                    "Facilitant la transition agroécologique (filières devant décroître)": "100 % Favorable sous conditions",
                    "Exploitations sans pratiques de transition agroécologique identifiées, et serres chauffées": "100 % Défavorable"
                },
                "Production d'énergies renouvelables agricoles": {
                    "Type d'énergies renouvelables": {
                        "Éolien": "100 % Très favorable",
                        "Solaire": {
                            "Solaire sur toiture (hors bâtiment d'élevage)": "100 % Très favorable",
                            "Solaire sur bâtiment d'élevage d'une exploitation avec pratiques de transition agroécologique": "100 % Favorable",
                            "Solaire sur terres non productives": "100 % Très favorable",
                            "Solaire sur bâtiment d'élevage d'une exploitation sans pratiques de transition agroécologique": "100 % Défavorable",
                            "Solaire au sol sans considération pour la productivité des terres": "100 % À approfondir"
                        },
                        "Méthanisation": {
                            "Couverture de fosses": "100 % Très favorable",
                            "Installation de torchères": "100 % Très favorable",
                            "Installation de méthaniseur": "100 % À approfondir"
                        }
                    },
                    "Facilitant la transition agroécologique (filières devant croître)": "100 % Très favorable",
                    "Facilitant la transition agroécologique (filières devant décroître)": "100 % Favorable sous conditions",
                    "Exploitations sans pratiques de transition agroécologique identifiées, et serres chauffées": "100 % Défavorable"
                }
            },
            "Circuits courts": {
                "Pratiques de production": {
                    "Transition agroécologique (filière devant croître)": "100 % Très favorable",
                    "Transition agroécologique (filière devant décroître)": "100 % Favorable sous conditions",
                    "Sans pratiques de transition agroécologique": "100 % Défavorable"
                }
            },
            "Forêt et bois": {
                "Pratiques d'exploitation": {
                    "Encourageant la gestion durable de la forêt (taxonomie européenne)": "100 % Très favorable",
                    "Exploitations forestières sans documentation de gestion durable": "100 % Neutre"
                }
            }
        }
    },
    "Activité économique": {
        "Sous-rubrique": {
            "Aides aux entreprises/organisations": "100 % À approfondir"
        }
    },
    "Alimentation": {
        "Sous-rubrique": {
            "Repas végétariens": "100 % Très favorable",
            "Autres repas": "100 % Neutre",
            "Viande de ruminants": "100 % Défavorable"
        }
    },
    "RH": {
        "Sous-rubrique": {
            "Formation professionnelle": {
                "Type de formations professionnelles et d'apprentissage": {
                    "Formations dans des secteurs couverts": "100 % Très favorable",
                    "Activité identifiée par les critères de classement": "100 % Très favorable"
                }
            },
            "Dépenses de personnel": "100 % À approfondir",
            "Frais de déplacements professionnels": {
                "Mode de déplacement": {
                    "Train": "100 % Très favorable",
                    "Transport en commun": "100 % Très favorable",
                    "Voiture électrique": "100 % Très favorable",
                    "Mobilités actives": "100 % Très favorable",
                    "Voitures GNV ou hybrides": "100 % Favorable sous conditions",
                    "Voitures fossiles sauf GNV/hybrides": "100 % Défavorable",
                    "Avion": "100 % Défavorable"
                }
            }
        }
    },
    "Espaces verts": {
        "Type d'espace": {
            "Développement ou entretien d'espaces arborés": "100 % Très favorable",
            "Développement ou entretien d'espaces verts sans spécificités arbres": "100 % Neutre"
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
    "Autres": {
        "Commande publique": "100 % À approfondir",
        "Compensation carbone": {
            "Dépense de compensation volontaire respectant les critères": "100 % Très favorable",
            "Selon les critères de classement": "100 % À approfondir"
        },
        "NTIC": {
            "Matériel": {
                "Achat respectant les critères méthodologiques": "100 % Favorable sous conditions",
                "Achat ne respectant pas les critères méthodologiques": "100 % Défavorable"
            },
            "Logiciels / Maintenance": "100 % Neutre",
            "Infrastructures": "100 % À approfondir"
        },
        "Paiement taxes": {
            "Paiement de taxes non incitatives": "100 % Neutre",
            "Paiement de taxes incitatives à réduire les émissions": "100 % Défavorable"
        },
        "Subventions": "100 % À approfondir"
    }
}



# Liste des titres connus dans l'arbre de décision
titres = ["Sous-rubrique", "Type", "Usage", "Partie concernée", "Motorisation", "Pratiques agricoles",
          "Performance énergie-carbone","Artificialisation des sols","Type de rénovation","Émissions"
          "Type de traitement","Type d'espace","Pratiques de production","Type d'énergie","Type de travaux",
          "Entretien", "Type d'investissement"]


def parcourir_arbre(noeud, chemin, titre_courant=None):

    # Cas final
    if isinstance(noeud, str):
        return noeud

    if isinstance(noeud, dict):

        # Si le noeud est un TITRE (clé connue)
        for titre in titres:
            if titre in noeud:
                return parcourir_arbre(
                    noeud[titre],
                    chemin,
                    titre_courant=titre
                )

        # Sinon : afficher le selectbox avec le TITRE COURANT
        options = list(noeud.keys())

        label = titre_courant if titre_courant else "Choisissez"

        choix = st.selectbox(
            label,
            options,
            key=" → ".join(chemin + [label])
        )

        chemin.append(choix)

        return parcourir_arbre(noeud[choix], chemin, titre_courant=None)




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
        if "Très favorable" in st.session_state.classement:
            st.success("✅ **Impact positif fort** : Cette dépense réduit significativement les émissions de GES.")
        elif "Favorable sous conditions" in st.session_state.classement:
            st.success("⚠️ **Impact positif limité** : Cette dépense améliore la performance, mais sous conditions.")
        elif "Défavorable" in st.session_state.classement:
            st.error("❌ **Impact négatif** : Cette dépense augmente les émissions de GES.")
        elif "Neutre" in st.session_state.classement:
            st.info("ℹ️ **Impact neutre** : Cette dépense n'a pas d'effet significatif sur les émissions.")
        elif "Occasion manquée" in st.session_state.classement:
            st.warning("⚠️ **Opportunité non saisie** : Cette dépense aurait pu inclure des améliorations énergétiques.")
        elif ("Très favorable" or "Favorable") and "Défavorable" in st.session_state.classement: 
            st.warning("⚠️ **Impact mixte** : Cette dépense a des impacts positifs et négatifs.")
        else:
            st.write("🔍 **À approfondir** : Analyse complémentaire nécessaire.")

    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")


### Associer image à Rubrique / sous-rubrique

# Récupérer les étapes du chemin de décision pour extraire les rubriques et sous-rubriques
chemin = st.session_state.etapes
rubrique = chemin[0]
sous_rubrique = chemin[1] if len(chemin) > 1 else None

# Dictionnaire d'images pour chaque rubrique et sous-rubrique
IMAGES_PAR_CHEMIN = {
    ("Bâtiment", "Construction de nouveaux bâtiments"): "images/batiment_construction.png",
    ("Bâtiment", "Rénovation des bâtiments"): "images/batiment_renovation.png",
    ("Bâtiment", "Entretien et maintenance de bâtiments et d'infrastructures"): "images/batiment_entretien.png",

    ("Transports et infrastructures", "Transports ferroviaires (tramway, train)"): "images/transport_ferroviaire.png",
    ("Transports et infrastructures", "Transports collectifs routiers (bus)"): "images/transport_collectif.png",
    ("Transports et infrastructures", "Achat de véhicule"): "images/transport_achat.png",
    ("Transports et infrastructures", "Entretien de véhicule"): "images/transport_entretien.png",
    ("Transports et infrastructures", "Voirie"): "images/transport_voirie.png",

    ("Énergie", "Achats d'énergie"): "images/energie_achats.png",
    ("Énergie", "Infrastructures de production d'énergie"): "images/energie_infra_production.png",
    ("Énergie", "Infrastructures de distribution d'énergie"): "images/energie_infra_distribution.png",

    ("Agriculture", "Pratiques agricoles"): "images/agriculture_aide_exploitation.png",
    ("Agriculture", "Construction/modernisation de bâtiments (hors efficacité énergétique)"): "images/agriculture_batiment_contruction_reno.png",
    ("Agriculture", "Circuits courts"): "images/agriculture_circuit_court.png",
    ("Agriculture", "Actions d'efficacité énergétique des exploitations"): "images/agriculture_efficacite_nrj.png",
    ("Agriculture", "Production d'énergies renouvelables agricoles"): "images/agriculture_production_nrj.png",
    ("Agriculture", "Forêt et bois"): "images/agriculture_foret.png",

    ("Activité économique", "Aides aux entreprises/organisations"): "images/action_économique.png",

    ("RH", "Formation professionnelle"): "images/rh_formation_pro.png",
    ("RH", "Dépenses personnels"): "images/rh_depense_personnel.png",
    ("RH", "Frais de déplacement"): "images/rh_frais_deplacement.png",

    ("Espaces verts", None): "images/espaces_verts.png",

    ("Alimentation", None): "images/alimentation.png",

    ("Déchets", "Gestion des déchets"): "images/dechets_gestion.png",

    ("Autres", "Commande publique"): "images/autre_commande_public.png",
    ("Autres", "Compensation carbone"): "images/autre_compensation_carbone.png",
    ("Autres", "NTIC"): "images/autre_NTIC.png",
    ("Autres", "Paiement taxes"): "images/autre_paiement_taxe.png",
    ("Autres", "Subventions"): "images/autre_subvention.png",

}


# Sélection de l'image correspondant au chemin
image_a_afficher = IMAGES_PAR_CHEMIN.get((rubrique, sous_rubrique), None)

# Affichage en bas de la page
if image_a_afficher:
    base_path = Path(__file__).parent  # répertoire contenant le script
    chemin_image = base_path / image_a_afficher

    if chemin_image.exists():
        with open(chemin_image, "rb") as f:
            image_bytes = f.read()
        st.subheader("Illustration associée")
        st.image(image_bytes, use_column_width=True)
    else:
        st.error(f"Image non trouvée : {chemin_image}")
else:
    st.info("🔍 Pas d'image disponible pour cette rubrique / sous-rubrique.")

