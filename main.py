from project import ResultValues
from moteur_id3.noeud_de_decision import NoeudDeDecision
from statistics import mean
from moteur_id3.id3_advance import ID3Advance
from moteur_id3.noeud_de_decision_advance import NoeudDeDecisionAdvance

test = ResultValues()
print("Arbre ID3")
print(test.arbre)
print("Profondeur maximale = ", max(NoeudDeDecision.niveaux))
print("Profondeur moyenne = ", mean(NoeudDeDecision.niveaux))
print("Nombre d'enfants moyen", mean(NoeudDeDecision.nb_enfant))
# print("Precision rate of the classification tree is : ", test.precision_rate, "%")
# test.define_regles()
# #print("Regles", test.regles)
# #test.process_example(test.faits_initiaux[10])
# print(test.arbre.classifie(test.donnees_train[13][1]))
# print(test.affiche_ccl(["cp-1", "age-3", "chol-1", "ca-3", "sex-0"]))
# liste = test.diagnostique(["cp-1", "age-3", "chol-1", "ca-3", "sex-0"])
# print("Variables à modifier : ", liste)
i = 0
j = len(test.faits_initiaux)
for fait in test.faits_initiaux:
    diag = test.diagnostique(fait)
    for e in diag:
        if len(e) == 2 or len(e) == 1:
            i = i + 1
            break
print("On trouve ", i," patients dont on peut modifier 1 ou 2 parametres parmi ", j, " patients")

print("Arbre ID3 Advance")
print(test.arbre_advance)
print("Profondeur maximale = ", max(NoeudDeDecisionAdvance.niveaux))
print("Profondeur moyenne = ", mean(NoeudDeDecisionAdvance.niveaux))
print("Nombre d'enfants moyen", mean(NoeudDeDecisionAdvance.nb_enfant))