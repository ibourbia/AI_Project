from project import ResultValues
from moteur_id3.noeud_de_decision import NoeudDeDecision
from statistics import mean

test=ResultValues()
print(test.arbre)
print("Profondeur maximale = ",max(NoeudDeDecision.niveaux))
print("Profondeur moyenne = ", mean(NoeudDeDecision.niveaux))