from math import log
from moteur_id3.id3 import ID3
from .noeud_de_decision_advance import NoeudDeDecisionAdvance
class ID3Advance(ID3):
    """
    """
    def construit_arbre_recur(self,donnees,attributs,predominant_class):
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
            #1 : trouver l'attribut et sa valeur minimisant
            ia=1
        return
    
    def partitionne(self, donnees, attribut, valeurs,valeur_partitionnement):
        """ Partitionne les données sur les valeurs a_j de l'attribut A,
            en fonction d'une valeur de partition.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j selon le noeud de l'arbre binaire auquel appartient la donnee
        """
        partitions_droite = {valeur: [] for valeur in valeurs if int(valeur) >= int(valeur_partitionnement)}
        partitions_gauche = {valeur: [] for valeur in valeurs if int(valeur) < int(valeur_partitionnement)}
         
        for donnee in donnees : 
            if int(donnee[1][attribut])>=int(valeur_partitionnement):
                partition_droite=partitions_droite[donnee[1][attribut]]
                partition_droite.append(donnee)
            else : 
                partition_gauche=partitions_gauche[donnee[1][attribut]]
                partition_gauche.append(donnee)
        
        partitions = {"Droite":partitions_gauche,"Gauche":partitions_droite}
        return partitions

    def p_aj(self,partition):
        """
        Retourne p(aj), la probabilité que l'attribut prenne une valeur >= 
        a la valeur de partitionnement
            :param: donnnes : les donnees a partitionner
            :param: attribut : l'attribut dont on veut trouver la probabilite
            :param: partition : les donnnes
        """
        nombre_donnees_droite = len(partition["Droite"].values())
        nombre_donnees_gauche = len(partition["Gauche"].values())
        
        p_aj=0.0
        if nombre_donnees_droite == 0.0:
            return p_aj
        else: 
            p_aj=nombre_donnees_droite/(nombre_donnees_droite+nombre_donnees_gauche)
        
        return p_aj
    
    def p_ci_aj(self, donnees,attribut,valeurs,valeur_partitionnement,classe):
        """
        p(ci|aj) =  la probabilité que la classe soit ci sachant que aj>=valeur_partitionnement (droite)
        ou aj<valeur_partitionnement (gauche)
            :param:
        """
        partition = self.partitionne(donnees, attribut, valeurs,valeur_partitionnement)
        nombre_donnees_droite = len(partition["Droite"].values())
        nombre_donnees_gauche = len(partition["Gauche"].values())

        #calcul de la probabilité de ci en fonction du côté droit ou gauche
        nombre_ci_gauche = [donnee for donnee in partition["Gauche"].values()[0] if partition["Gauche"].values()[0]==classe]
        nombre_ci_droite = [donnee for donnee in partition["Droite"].values()[0] if partition["Gauche"].values()[0]==classe]
        #a droite
        p_ci_aj_droite= nombre_ci_droite/nombre_donnees_droite
        #a gauche
        p_ci_aj_gauche=nombre_ci_gauche/nombre_donnees_gauche

        probabilites={"Gauche":p_ci_aj_gauche,"Droite": p_ci_aj_droite}
        return probabilites

    def h_C_aj(self,donnees,attribut,valeurs,valeur_partitionnement):
        """
        H(C|aj) = l'entropie de la classe C selon si aj>= ou < a valeur_partitionnement
        """
        #calcule p(ci|aj) pour les classes 1 et 0, a droite et a gauche
        p_cis_aj_0 = [p for p in self.p_ci_aj(donnees,attribut,valeurs,valeur_partitionnement,'0').values()]
        p_cis_aj_1 = [p for p in self.p_ci_aj(donnees,attribut,valeurs,valeur_partitionnement,'1').values()]

        #calcul de l'entropie de la classe c a droite et a gauche
        h_c_aj_droite = -p_cis_aj_0["Droite"]*log(p_cis_aj_0["Droite"],2.0)-p_cis_aj_1["Droite"]*log(p_cis_aj_1["Droite"],2.0)
        h_c_aj_gauche = -p_cis_aj_0["Gauche"]*log(p_cis_aj_0["Gauche"],2.0)-p_cis_aj_1["Gauche"]*log(p_cis_aj_1["Gauche"],2.0)

        h_c_aj = {"Droite":h_c_aj_droite,"Gauche":h_c_aj_gauche}
        return h_c_aj
 
    def h_C_A(self,donnees,attribut,valeurs,valeur_partitionnement):
        """
        H(C|A)= l'entropie de la classe C

        """
        partition = self.partitionne(donnees, attribut, valeurs,valeur_partitionnement)

        h_c_aj=self.h_C_aj(donnees,attribut,valeurs,valeur_partitionnement)
        p_aj=self.p_aj(partition)
     
        h_c_a = -h_c_aj["Gauche"]*(1-p_aj) -h_c_aj["Droite"]*p_aj

        return h_c_a
