from project import ResultValues
from moteur_id3.noeud_de_decision import NoeudDeDecision
from statistics import mean

test = ResultValues()
print(test.arbre)
print("Profondeur maximale = ", max(NoeudDeDecision.niveaux))
print("Profondeur moyenne = ", mean(NoeudDeDecision.niveaux))
print("Nombre d'enfants moyen", mean(NoeudDeDecision.nb_enfant))
print("Precision rate of the classification tree is : ", test.precision_rate, "%")
test.define_regles()
print("Regles", test.regles)
