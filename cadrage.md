# Document de cadrage — Dashboard "L'heure de pointe du soir fait grimper le prix au mile"

## Message clé
**Les courses prises entre 16h et 19h coûtent en moyenne 20 % de plus au mile que les heures creuses, à cause du ralentissement du trafic — cette fenêtre horaire est la plus rentable pour y positionner davantage de chauffeurs.**

## Audience cible
Le·la **responsable des opérations (dispatch) d'une compagnie de taxis/VTC** à New York, qui décide comment répartir les chauffeurs dans le temps et l'espace pour maximiser le chiffre d'affaires par heure travaillée. Ce n'est pas un dashboard pour le grand public : il sert une décision de planification opérationnelle.

## KPIs retenus

| KPI | Vanity ou Actionable ? | Justification |
|---|---|---|
| **Prix moyen au mile par période** (heures creuses / pointe matin / pointe soir) | Actionable | Identifie directement la fenêtre horaire la plus rentable au mile parcouru, pour orienter le repositionnement des chauffeurs. |
| **Vitesse moyenne (min/mile) par période** | Actionable | Explique le mécanisme derrière le KPI précédent (trafic plus dense = plus cher au mile) et permet d'anticiper les zones à embouteillage. |
| **Part du chiffre d'affaires généré en heure de pointe soir** | Actionable | Mesure la concentration réelle de revenu sur ce créneau, pour dimensionner l'effort d'incitation (primes, bonus horaires). |

*(Le nombre total de courses enregistrées, plus flatteur à afficher, a été volontairement écarté : il ne dit rien sur la rentabilité par heure travaillée, contrairement au prix au mile.)*

## Structure prévue du dashboard

1. **Zone KPIs** (haut de page, 3 colonnes) : les trois indicateurs ci-dessus, recalculés selon les filtres actifs.
2. **Zone détail** (onglets) :
   - *Vue d'ensemble* : distance vs prix, coloré par période de la journée, pour visualiser l'effet horaire course par course.
   - *Pointe vs heures creuses* : barres comparant prix/mile et vitesse par période, et par arrondissement de prise en charge.
   - *Données détaillées* : table filtrable pour l'audit ligne à ligne.
3. **Zone filtres** (sidebar) : arrondissement de prise en charge, couleur du taxi (yellow/green), mode de paiement, période de la journée.

## Dataset utilisé
`taxis` (6 433 courses de taxi new-yorkaises, mars 2019 — colonnes : horodatage, distance, tarif, pourboire, arrondissement, mode de paiement). Dataset public de référence pour l'analyse exploratoire, réutilisé tel quel conformément à la consigne ("vous pouvez utiliser un autre dataset si l'analyse en est déjà faite").

**Point de vigilance méthodologique** : le pourboire n'est enregistré que pour les paiements par carte (0 systématique en cash), ce qui rend toute comparaison "pourboire par mode de paiement" trompeuse — c'est pourquoi ce dashboard n'utilise pas cette variable comme KPI, au profit du prix au mile qui, lui, est fiable quel que soit le mode de paiement.
