## Richesse du ménage
dic_aides_type_menage = {
  "tableauRevenus_ile_de_france": [
    {
      "nombrePersonnesComposantLeMenage": 1,
      "menagesAuxRevenusTresModestes": 23541,
      "menagesAuxRevenusModestes": 28657,
      "menagesAuxRevenusIntermediaires": 40018,
      "menagesAuxRevenusSuperieurs": "supérieur à 40 018 €"
    },
    {
      "nombrePersonnesComposantLeMenage": 2,
      "menagesAuxRevenusTresModestes": 34551,
      "menagesAuxRevenusModestes": 42058,
      "menagesAuxRevenusIntermediaires": 58827,
      "menagesAuxRevenusSuperieurs": "supérieur à 58 827 €"
    },
    {
      "nombrePersonnesComposantLeMenage": 3,
      "menagesAuxRevenusTresModestes": 41493,
      "menagesAuxRevenusModestes": 50513,
      "menagesAuxRevenusIntermediaires": 70382,
      "menagesAuxRevenusSuperieurs": "supérieur à 70 382 €"
    },
    {
      "nombrePersonnesComposantLeMenage": 4,
      "menagesAuxRevenusTresModestes": 48447,
      "menagesAuxRevenusModestes": 58981,
      "menagesAuxRevenusIntermediaires": 82839,
      "menagesAuxRevenusSuperieurs": "supérieur à 82 839 €"
    },
    {
      "nombrePersonnesComposantLeMenage": 5,
      "menagesAuxRevenusTresModestes": 55427,
      "menagesAuxRevenusModestes": 67473,
      "menagesAuxRevenusIntermediaires": 94844,
      "menagesAuxRevenusSuperieurs": "supérieur à 94 844 €"
    },
    {
      "nombrePersonnesComposantLeMenage": "par personne supplémentaire",
      "menagesAuxRevenusTresModestes": 6970,
      "menagesAuxRevenusModestes": 8486,
      "menagesAuxRevenusIntermediaires": 12006,
      "menagesAuxRevenusSuperieurs": 12006
    }
  ],
  "tableauRevenus_hors_ile_de_france": [
    {
      "nombrePersonnesComposantLeMenage": 1,
      "menagesAuxRevenusTresModestes": 17009,
      "menagesAuxRevenusModestes": 21805,
      "menagesAuxRevenusIntermediaires": 30549,
      "menagesAuxRevenusSuperieurs": "supérieur à 30 549 €"
    },
    {
      "nombrePersonnesComposantLeMenage": 2,
      "menagesAuxRevenusTresModestes": 24875,
      "menagesAuxRevenusModestes": 31889,
      "menagesAuxRevenusIntermediaires": 44907,
      "menagesAuxRevenusSuperieurs": "supérieur à 44 907 €"
    },
    {
      "nombrePersonnesComposantLeMenage": 3,
      "menagesAuxRevenusTresModestes": 29917,
      "menagesAuxRevenusModestes": 38349,
      "menagesAuxRevenusIntermediaires": 54071,
      "menagesAuxRevenusSuperieurs": "supérieur à 54 071 €"
    },
    {
      "nombrePersonnesComposantLeMenage": 4,
      "menagesAuxRevenusTresModestes": 34948,
      "menagesAuxRevenusModestes": 44802,
      "menagesAuxRevenusIntermediaires": 63235,
      "menagesAuxRevenusSuperieurs": "supérieur à 63 235 €"
    },
    {
      "nombrePersonnesComposantLeMenage": 5,
      "menagesAuxRevenusTresModestes": 40002,
      "menagesAuxRevenusModestes": 51281,
      "menagesAuxRevenusIntermediaires": 72400,
      "menagesAuxRevenusSuperieurs": "supérieur à 72 400 €"
    },
    {
      "nombrePersonnesComposantLeMenage": "par personne supplémentaire",
      "menagesAuxRevenusTresModestes": 5045,
      "menagesAuxRevenusModestes": 6462,
      "menagesAuxRevenusIntermediaires": 9165,
      "menagesAuxRevenusSuperieurs": 9165
    }
  ]
}

subventionsMPR = {
    'Raccordement à un réseau de chaleur et/ou de froid': [1200, 800, 400, 0],
    'Chauffe-eau thermodynamique': [1200, 800, 400, 0],
    'Pompe à chaleur air/eau (dont PAC hybrides)': [5000, 4000, 3000, 0],
    'Pompe à chaleur géothermique ou solarothermique (dont PAC hybrides)': [11000, 9000, 6000, 0],
    'Chauffe-eau solaire individuel en Métropole (et dispositifs solaires pour le chauffage de l’eau)': [4000, 3000, 2000, 0],
    'Système solaire combiné (et dispositifs solaires pour le chauffage des locaux)': [10000, 8000, 4000, 0],
    'Partie thermique d’un équipement PVT eau (système hybride photovoltaïque et thermique)': [2500, 2000, 1000, 0],
    'Poêle à bûches et cuisinière à bûches': [2500, 2000, 1000, 0],
    'Poêle à granulés et cuisinière à granulés': [2500, 2000, 1500, 0],
    'Chaudière bois à alimentation manuelle (bûches)': [8000, 6500, 3000, 0],
    'Chaudière bois à alimentation automatique (granulés, plaquettes)': [10000, 8000, 4000, 0],
    'Foyer fermé et insert à bûches ou à granulés': [2500, 1500, 800, 0],
}

translateMPR = {
  'PAC air-eau':'Pompe à chaleur air/eau (dont PAC hybrides)',
  #'Pergola solaire':'Système solaire combiné (et dispositifs solaires pour le chauffage des locaux)',
  'Ballon thermodynamique':'Chauffe-eau thermodynamique'
  }

subventions_isolation = {
    "Isolation thermique des murs par l’extérieur (surface de murs limitée à 100 m2)": {"€/m²": [75, 60, 40, 0]},
    "Isolation thermique des murs par l’intérieur": {"€/m²": [25, 20, 15, 0]},
    "Isolation thermique des rampants de toiture ou des plafonds de combles": {"€/m²": [25, 20, 15, 0]},
    "Isolation thermique des toitures terrasses": {"€/m²": [75, 60, 40, 0]},
    "Isolation thermique des parois vitrées (fenêtres et portes-fenêtres) en remplacement de simple vitrage": {"€/équipement": [100, 80, 40, 0]},
    "Protection des parois vitrées ou opaques contre le rayonnement solaire (uniquement pour l’Outre-mer)": {"€/m²": [25, 20, 15, 0]},
    "Audit énergétique hors obligation réglementaire (conditionné à la réalisation d’un geste de travaux)": {"€": [500, 400, 300, 0]},
    "Dépose de cuve à fioul": {"€": [1200, 800, 400, 0]},
    "Ventilation double flux": {"€": [2500, 2000, 1500, 0]}
}

subCEE = {
  'menage_modeste_ou_tres_modeste': {
    'Chaudière biomasse': 4000, 
    'Pompe à chaleur air/eau': 4000, 
    'Chauffe-eau thermodynamique':84,
    'Pompe à chaleur eau/eau ou sol/eau': 5000, 
    'Système solaire combiné': 5000, 
    'Pompe à chaleur hybride': 4000
    },
  'menage_autre': {'Chaudière biomasse': 2500,'Chauffe-eau thermodynamique':84, 'Pompe à chaleur air/eau': 2500, 'Pompe à chaleur eau/eau ou sol/eau': 5000, 'Système solaire combiné': 5000, 'Pompe à chaleur hybride': 2500}
}

translateCEE = {
  'PAC air-eau':'Pompe à chaleur air/eau',
  #'PAC air-air Quadri':'Pompe à chaleur hybride',
  #'Pergola solaire':'Système solaire combiné',
  'Ballon thermodynamique':'Chauffe-eau thermodynamique'
}

