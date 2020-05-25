from project import ResultValues
from moteur_id3.noeud_de_decision import NoeudDeDecision
from statistics import mean
from moteur_id3.id3_advance import ID3Advance
from moteur_id3.noeud_de_decision_advance import NoeudDeDecisionAdvance

test = ResultValues()
# print("Arbre ID3")
# print(test.arbre)
# print("Profondeur maximale = ", max(NoeudDeDecision.niveaux))
# print("Profondeur moyenne = ", mean(NoeudDeDecision.niveaux))
# print("Nombre d'enfants moyen", mean(NoeudDeDecision.nb_enfant))
# print("Precision rate of the classification tree is : ", test.precision_rate, "%")

i = 0
j = len(test.faits_initiaux)
m = 0
for fait in test.faits_initiaux:
    diag = test.diagnostic(fait)
    m = len(diag)
    for e in diag:
        if len(e) == 2 or len(e) == 1:
            i = i + 1
            break
print("On trouve ", i, " patients dont on peut modifier 1 ou 2 parametres parmi ", m, " patients malades et ", j
      , " patients au total")

print("Arbre ID3 Advance")
print(test.arbre_advance)
print("Profondeur maximale = ", max(NoeudDeDecisionAdvance.niveaux))
print("Profondeur moyenne = ", mean(NoeudDeDecisionAdvance.niveaux))
print("Nombre d'enfants moyen", mean(NoeudDeDecisionAdvance.nb_enfant))
print("Precision rate of the classification tree is : ", test.precision_rate_advance, "%")
