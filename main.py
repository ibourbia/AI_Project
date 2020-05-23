from project import ResultValues
from moteur_id3.noeud_de_decision import NoeudDeDecision
from statistics import mean
from moteur_id3.id3_advance import ID3Advance
from moteur_id3.noeud_de_decision_advance import NoeudDeDecisionAdvance

test = ResultValues()
print(test.arbre)
# print("Profondeur maximale = ", max(NoeudDeDecision.niveaux))
# print("Profondeur moyenne = ", mean(NoeudDeDecision.niveaux))
# print("Nombre d'enfants moyen", mean(NoeudDeDecision.nb_enfant))
# print("Precision rate of the classification tree is : ", test.precision_rate, "%")
# test.define_regles()
# #print("Regles", test.regles)
# #test.process_example(test.faits_initiaux[10])
# print(test.arbre.classifie(test.donnees_train[13][1]))
# print(test.affiche_ccl(["cp-1", "age-3", "chol-1", "ca-3", "sex-0"]))
# liste = test.diagnostique(["cp-1", "age-3", "chol-1", "ca-3", "sex-0"])
# print("Variables à modifier : ", liste)
# for fait in test.faits_initiaux:
#     print(test.diagnostique(fait))

print(test.arbre_advance)