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
                print("LES CLASSES DES DONNEES",donnee[0])
                if donnee[0] != premiere_classe:
                    return False 
            return True
        if classe_unique(donnees):
            print("UNIQUEEEEEEE")
            return NoeudDeDecisionAdvance(None, donnees, str(predominant_class))
        elif len(donnees)==0:
            print("TRUEEEEEEEEEEEEEE")
            return NoeudDeDecisionAdvance(None, [str(predominant_class), dict()], str(predominant_class))
        else : 
            #1 : trouver l'attribut et sa valeur minimisant l'entropie
            attribut_optimal = self.attribut_optimal(donnees,attributs)
            attributs_valeurs_restantes = attributs.copy()
            attributs_valeurs_restantes[attribut_optimal[0]].remove(attribut_optimal[1])
            print("ATTRIBUT OPTIMAL",attribut_optimal)
            print("ATTRIBUTS RESTANTS",attributs_valeurs_restantes)
            
            partitions_dict=self.partitionne(donnees,attribut_optimal[0],attributs_valeurs_restantes[attribut_optimal[0]], attribut_optimal[1])
            partitions= [partitions_dict["Droite"],partitions_dict["Gauche"]]

            enfants = {}
            for partition in partitions : 
                for valeur, partition in partition.items():
                    print("NIQUE SA RACEEEEEEEEEEEEEEEEE",partition)
                    enfants[valeur] = self.construit_arbre_recur(partition,
                                                             attributs_valeurs_restantes,
                                                             predominant_class)

                return NoeudDeDecisionAdvance(attribut_optimal[0], donnees, str(predominant_class), enfants)

    
    
    def attribut_optimal(self,donnees,attributs):
        """
        Cherche l'attribut et sa valeur qui minimisent l'entropie
        Retourne l'attribut et la valeur pour partitionner
            :param: donnees : les donnees d'apprentissage
            :param: attributs : tous les attributs et leur domaine de valeur
                                {attribut : {valeurs}}
            :return: attribut_optimal : un tuple (nom de l'attribut minimal, valeur minimale)
        """

        entropies_attributs=[]

        for attribut,set_value in attributs.items():
            entropie_minimale = 10000
            valeur_partitionnement = str()
            for value in set_value : 
                entropie = self.h_C_A(donnees,attribut,attributs[attribut],value)
                if entropie<entropie_minimale:
                    entropie_minimale=entropie
                    valeur_partitionnement=value
            entropies_attributs.append((entropie_minimale,(attribut,valeur_partitionnement)))
        
        attribut_optimal=min(entropies_attributs, key=lambda h_c_a:h_c_a[0])[1]
        # print("ATTRIBUT OPTIMAL",attribut_optimal)
        
        return attribut_optimal
    
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
        partitions_droite = {valeur: [] for valeur in valeurs if float(valeur) >= float(valeur_partitionnement)}
        partitions_gauche = {valeur: [] for valeur in valeurs if float(valeur) < float(valeur_partitionnement)}
         
        for donnee in donnees : 
            if float(donnee[1][attribut])>=float(valeur_partitionnement):
                partition_droite=partitions_droite[donnee[1][attribut]]
                partition_droite.extend([donnee])
            else : 
                partition_gauche=partitions_gauche[donnee[1][attribut]]
                partition_gauche.extend([donnee])
        
        partitions = {"Droite":partitions_gauche,"Gauche":partitions_droite}
        # print("PARTITIONS ", partitions)
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
        # print("LEN DONNEES DROITES", nombre_donnees_droite )
        # print("LEN DONNEES GAUCHE", nombre_donnees_gauche)
        if nombre_donnees_droite == 0.0:
            return 0.0
        else: 
            p_aj=nombre_donnees_droite/(nombre_donnees_droite+nombre_donnees_gauche)
        
        return p_aj
    
    def p_ci_aj(self, donnees,attribut,valeurs,valeur_partitionnement,classe):
        """
        p(ci|aj) =  la probabilité que la classe soit ci sachant que aj>=valeur_partitionnement (droite)
        ou aj<valeur_partitionnement (gauche)
            :param:
        """
        donnees_droite=list()
        donnees_gauche=list()
        partition = self.partitionne(donnees, attribut, valeurs,valeur_partitionnement)
        partition_droite=partition["Droite"].values()
        partition_gauche=partition["Gauche"].values()

        
        donnees_droite=[donnees_liste for donnees_liste in partition_droite]
        donnees_gauche=[donnees_liste for donnees_liste in partition_gauche]
        donnee_droite=list()
        donnee_gauche=list()

        for donnees in donnees_droite:
            for d in donnees : 
                donnee_droite.extend([d])
        for donnees in donnees_gauche:
            for d in donnees:
                donnee_gauche.extend([d])
        # print("DONNEES DROITES", donnee_droite)
        # print("DONNEES GAUCHE", donnee_gauche)

        nombre_donnees_droite = len(donnee_droite)
        nombre_donnees_gauche = len(donnee_gauche)
        # print("NOMBRE DONNEES DROITE", nombre_donnees_droite)
        # print("NOMBRE DONNEES GAUCHE ", nombre_donnees_gauche)
        #calcul de la probabilité de ci en fonction du côté droit ou gauche
        donnees_ci_gauche = [donnee for donnee in donnee_droite if donnee[0]==classe]
        donnees_ci_droite = [donnee for donnee in donnee_gauche if donnee[0]==classe]
        
        nombre_ci_droite = len(donnees_ci_droite)
        nombre_ci_gauche = len(donnees_ci_gauche)
        # print("DONNEES DROITES CI", donnees_ci_droite)
        # print("NOMBRE DONNEES DROITES CI", nombre_ci_droite)

        #a droite
        p_ci_aj_droite= nombre_ci_droite/nombre_donnees_droite if nombre_donnees_droite!=0.0 else 0.0
        #a gauche
        p_ci_aj_gauche=nombre_ci_gauche/nombre_donnees_gauche if nombre_donnees_gauche!=0.0 else 0.0
        # print("PCIAJDROITE",p_ci_aj_droite)
        # print("PCIAJGAUCHE", p_ci_aj_gauche)

        probabilites={"Gauche":p_ci_aj_gauche,"Droite": p_ci_aj_droite}
        
        return probabilites

    def h_C_aj(self,donnees,attribut,valeurs,valeur_partitionnement):
        """
        H(C|aj) = l'entropie de la classe C selon si aj>= ou < a valeur_partitionnement
        """
        #calcule p(ci|aj) pour les classes 1 et 0, a droite et a gauche
        p_cis_aj_0 = self.p_ci_aj(donnees,attribut,valeurs,valeur_partitionnement,'0')
        p_cis_aj_1 = self.p_ci_aj(donnees,attribut,valeurs,valeur_partitionnement,'1')

        #calcul de l'entropie de la classe c a droite et a gauche
        h_c_aj_droite = -sum(p_ci_aj*log(p_ci_aj,2.0) for p_ci_aj in (p_cis_aj_0["Droite"],p_cis_aj_1["Droite"]) if p_ci_aj!=0.0)
        h_c_aj_gauche = -sum(p_ci_aj*log(p_ci_aj,2.0) for p_ci_aj in (p_cis_aj_0["Gauche"], p_cis_aj_1["Gauche"]) if p_ci_aj!=0.0)

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
