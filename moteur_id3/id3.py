from math import log2
from .noeud_de_decision import NoeudDeDecision

class ID3:
    """ Algorithme ID3. """
    
    def construit_arbre(self, donnees):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        
        # Nous devons extraire les domaines de valeur des 
        # attributs, puisqu'ils sont nécessaires pour 
        # construire l'arbre.
        attributs = {}
        for donnee in donnees:
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add(valeur)
                   
        arbre = self.construit_arbre_recur(donnees, attributs)
        
        return arbre

    def construit_arbre_recur(self, donnees, attributs):
        """ Construit rédurcivement un arbre de décision à partir 
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        classes = list(set([d[0] for d in donnees]))
        entropies = [(a,self.h_C_A(donnees,a,attributs[a])) for a in attributs]

        if len(donnees) == 0 : 
            return
        elif len(classes)==1:
            return NoeudDeDecision(None,donnees)
        elif attributs == {}:
            return NoeudDeDecision(None, donnees)
        else :
            if entropies : 
                attribut_min = min(entropies, key=lambda x:x[1])[0]
                attributs_restant = attributs.copy()
                del attributs_restant[attribut_min]
            
                valeurs_min = attributs[attribut_min]
                partition = self.partitionne(donnees,attribut_min,valeurs_min)
            
                enfants = {}
                for v in valeurs_min :
                    enfants.update({v:self.construit_arbre_recur(partition[v],attributs_restant)})
                return NoeudDeDecision(attribut_min,donnees,enfants)

               

        

    def partitionne(self, donnees, attribut, valeurs):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j.
        """
        #data pour lesquelles a=aj
        data_lists = []
        for v in valeurs : 
            data = [d for d in donnees if d[1][attribut]==v]
            data_lists.append(data)
        
        partition = dict(zip(valeurs, data_lists))
        return partition

    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.            
            :return: p(a_j)
        """
        #nombre de fois ou aj apparait dans les donnees
        occurence_aj=0
        #nombre total de donnees
        total = len(donnees)

        if total == 0 :
            return 0.0
        
        for d in donnees : 
            #comptage du nombre de fois ou aj apparait
            if d[1][attribut]==valeur : 
                occurence_aj+=1
        
        return occurence_aj/total

    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """
        #nombre de donnes ou A = aj
        donnes_aj = [d for d in donnees if d[1][attribut]==valeur]
        total = len(donnes_aj)
        #nombre de cas ou C = ci et A=aj
        occurence=0

        if total==0 : 
            return 0.0
        
        for d in donnes_aj : 
            #comptage du nombre de fois ou ci apparait dans les donnes aj
            if d[0]==classe : 
                occurence += 1

        return occurence/total


    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """
        h_C_aj = 0
        #ajoute une seule fois chaque classe differente a la liste
        classes_differentes =list(set( [donnee[0] for donnee in donnees]))

        #calcul de l'entropie de la classe
        for c in classes_differentes : 
            p_ci_aj = self.p_ci_aj(donnees,attribut,valeur,c) 
            log2p = log2(p_ci_aj) if p_ci_aj!=0 else 0.0
            h_C_aj -= p_ci_aj* log2p
        
        return h_C_aj




    def h_C_A(self, donnees, attribut, valeurs):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.
            
            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """
        h_C_A=0
        for val in valeurs : 
            h_C_A += self.p_aj(donnees,attribut,val)*self.h_C_aj(donnees,attribut,val)

        return h_C_A
