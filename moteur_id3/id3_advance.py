from math import log
from moteur_id3.id3 import ID3
from .noeud_de_decision_advance import NoeudDeDecisionAdvance
class ID3Advance:
    """
    """
    def construit_arbre_advance(self,donnees) : 
        attributs = self.attributs(donnees)
        # Find the predominant class
        classes = set([row[0] for row in donnees])
        # print(classes)
        predominant_class_counter = -1
        for c in classes:
            # print([row[0] for row in donnees].count(c))
            if [row[0] for row in donnees].count(c) >= predominant_class_counter:
                predominant_class_counter = [row[0] for row in donnees].count(c)
                predominant_class = c
        self.construit_arbre_advance_recur(donnees,attributs,predominant_class)
        return
    
    def construit_arbre_advance_recur(self,donnees,attributs,predominant_class):
        def classe_unique(donnees):
            """ Vérifie que toutes les données appartiennent à la même classe. """
            
            if len(donnees) == 0:
                return True 
            premiere_classe = donnees[0][0]
            for donnee in donnees:
                if donnee[0] != premiere_classe:
                    return False 
            return True

        if classe_unique(donnees):
            return NoeudDeDecisionAdvance(None, donnees, str(predominant_class))
        elif donnees ==[]:
            return NoeudDeDecisionAdvance(None, [str(predominant_class), dict()], str(predominant_class))
        else : 
            # Sélectionne l'attribut qui réduit au maximum l'entropie : 
            h_C_As_attribs = [(self.h_C_A(donnees, attribut, attributs[attribut]), 
                               attribut) for attribut in attributs]
            attribut = min(h_C_As_attribs, key=lambda h_a: h_a[0])[1]
            
            #maximisation du gain : 
            h_c_attrib =[]
            for sets in attributs[attribut]: 
                set_iterator = iter(sets)
                h_c_attrib.append( (next(set_iterator),self.h_C(donnees,next(set_iterator))))
            
            attribut_max=


        return
    
    def attributs(self,donnees):
        # Nous devons extraire les domaines de valeur des 
        # attributs et leur classe, puisqu'ils sont nécessaires pour 
        # construire l'arbre.
        attributs = {}
        for donnee in donnees:
            classe = donnee[0]
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add((valeur,classe))
        print("ATTRIBUTS ID3", attributs)
        return attributs

    
    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.            
            :return: p(a_j)
        """
        # Nombre de données.
        nombre_donnees = len(donnees)
        
        # Permet d'éviter les divisions par 0.
        if nombre_donnees == 0:
            return 0.0
        
        # Nombre d'occurrences de la valeur a_j parmi les données.
        nombre_aj = 0
        for donnee in donnees:
            if donnee[1][attribut] == valeur:
                nombre_aj += 1

        # p(a_j) = nombre d'occurrences de la valeur a_j parmi les données / 
        #          nombre de données.
        return nombre_aj / nombre_donnees

    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """
        # Nombre d'occurrences de la valeur a_j parmi les données.
        donnees_aj = [donnee for donnee in donnees if donnee[1][attribut] == valeur]
        nombre_aj = len(donnees_aj)
        
        # Permet d'éviter les divisions par 0.
        if nombre_aj == 0:
            return 0
        
        # Nombre d'occurrences de la classe c_i parmi les données pour lesquelles 
        # A vaut a_j.
        donnees_ci = [donnee for donnee in donnees_aj if donnee[0] == classe]
        nombre_ci = len(donnees_ci)

        # p(c_i|a_j) = nombre d'occurrences de la classe c_i parmi les données 
        #              pour lesquelles A vaut a_j /
        #              nombre d'occurrences de la valeur a_j parmi les données.
        return nombre_ci / nombre_aj

    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """
        # Les classes attestées dans les exemples.
        classes = list(set([donnee[0] for donnee in donnees]))
        
        # Calcule p(c_i|a_j) pour chaque classe c_i.
        p_ci_ajs = [self.p_ci_aj(donnees, attribut, valeur, classe) 
                    for classe in classes]

        # Si p vaut 0 -> plog(p) vaut 0.
        return -sum([p_ci_aj * log(p_ci_aj, 2.0) 
                    for p_ci_aj in p_ci_ajs 
                    if p_ci_aj != 0])

    def h_C_A(self, donnees, attribut, valeurs):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.
            
            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """
        # Calcule P(a_j) pour chaque valeur a_j de l'attribut A.
        p_ajs = [self.p_aj(donnees, attribut, valeur) for valeur in valeurs]

        # Calcule H_C_aj pour chaque valeur a_j de l'attribut A.
        h_c_ajs = [self.h_C_aj(donnees, attribut, valeur) 
                   for valeur in valeurs]

        return sum([p_aj * h_c_aj for p_aj, h_c_aj in zip(p_ajs, h_c_ajs)])

    def h_C(self,donnees,classe):
        """
        p(ci) =  la probabilité que la classe C ait la valeur ci parmis les données

            :param donnees : les donnnees d'apprentissage
            :param classe :  la valeur ci de la classe
            :return: p(ci)
        """
        nombre_donnees = len(donnees)
        donnees_ci = [donnee for donnee in donnees if donnee[0]==classe]
        nombre_ci = len(donnees_ci)
        p_ci = nombre_ci/nombre_donnees
        return -(p_ci * log(p_ci,2.0))
