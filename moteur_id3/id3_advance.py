from math import log
from moteur_id3.id3 import ID3
from .noeud_de_decision_advance import NoeudDeDecisionAdvance


class ID3Advance(ID3):
    """
    """

    def construit_arbre_recur(self, donnees, attributs, predominant_class, attribut_optimal_recur=None, ):
        def classe_unique(donnees):
            """ Vérifie que toutes les données appartiennent à la même classe. """

            if len(donnees) == 0:
                return True
            premiere_classe = donnees[0][0]
            for donnee in donnees:
                if donnee[0] != premiere_classe:
                    return False
            return True

        if len(donnees) == 0:
            return NoeudDeDecisionAdvance(None, None, [str(predominant_class), dict()], str(predominant_class))
        elif classe_unique(donnees):
            return NoeudDeDecisionAdvance(None, None, donnees, str(predominant_class))
        else:
            # 1 : trouver l'attribut et sa valeur minimisant l'entropie
            attribut_optimal = self.attribut_optimal(donnees, attributs)
            # if attribut_optimal == attribut_optimal_recur:
            #     return NoeudDeDecisionAdvance(None, None, donnees, str(predominant_class))

            partitions_dict = self.partitionne(donnees, attribut_optimal[0], attributs[attribut_optimal[0]],
                                               attribut_optimal[1])

            enfants = {}
            for side, partition in partitions_dict.items():
                if side == "Droite":
                    donnees_droite = self.donnees_partition(partition.values())
                    attributs_droite = self.attributs(donnees_droite)
                    enfants[side] = self.construit_arbre_recur(donnees_droite, attributs_droite, predominant_class,
                                                               attribut_optimal)
                elif side == "Gauche":
                    donnees_gauche = self.donnees_partition(partition.values())
                    attributs_gauche = self.attributs(donnees_gauche)
                    enfants[side] = self.construit_arbre_recur(donnees_gauche, attributs_gauche, predominant_class,
                                                               attribut_optimal)
            return NoeudDeDecisionAdvance(attribut_optimal[0], attribut_optimal[1], donnees, str(predominant_class),
                                          enfants)

    def valeur_max(self, donnees, attribut, attributs):
        """
        Cherche la valeur maximale pour un seul attribut
        """
        val_max = str()
        for value in attributs[attribut]:
            valeur_max = -100000.0
            valeur_courante = float(value)
            if valeur_courante > valeur_max:
                valeur_max = valeur_courante
                val_max = str(valeur_max)
        return val_max

    def attribut_optimal(self, donnees, attributs):
        """
        Cherche l'attribut et sa valeur qui minimisent l'entropie
        Retourne l'attribut et la valeur pour partitionner
            :param: donnees : les donnees d'apprentissage
            :param: attributs : tous les attributs et leur domaine de valeur
                                {attribut : {valeurs}}
            :return: attribut_optimal : un tuple (nom de l'attribut minimal, valeur minimale)
        """

        entropies_attributs = []

        for attribut, set_value in attributs.items():
            entropie_minimale = 10000
            valeur_partitionnement = str()
            for value in set_value:
                entropie = self.h_C_A(donnees, attribut, attributs[attribut], value)
                if entropie < entropie_minimale:
                    entropie_minimale = entropie
                    valeur_partitionnement = value
            entropies_attributs.append((entropie_minimale, (attribut, valeur_partitionnement)))
        attribut_optimal = min(entropies_attributs, key=lambda h_c_a: h_c_a[0])[1]

        return attribut_optimal

    def partitionne(self, donnees, attribut, valeurs, valeur_partitionnement):
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

        for donnee in donnees:
            if float(donnee[1][attribut]) >= float(valeur_partitionnement):
                partition_droite = partitions_droite[donnee[1][attribut]]
                partition_droite.extend([donnee])
            else:
                partition_gauche = partitions_gauche[donnee[1][attribut]]
                partition_gauche.extend([donnee])

        partitions = {"Droite": partitions_droite, "Gauche": partitions_gauche}
        return partitions

    def p_aj(self, partition):
        """
        Retourne p(aj), la probabilité que l'attribut prenne une valeur >= 
        a la valeur de partitionnement
            :param: donnnes : les donnees a partitionner
            :param: attribut : l'attribut dont on veut trouver la probabilite
            :param: partition : les donnnes
        """
        nombre_donnees_droite = len(partition["Droite"].values())
        nombre_donnees_gauche = len(partition["Gauche"].values())

        if nombre_donnees_droite == 0.0:
            return 0.0
        else:
            p_aj = nombre_donnees_droite / (nombre_donnees_droite + nombre_donnees_gauche)
        return p_aj

    def donnees_partition(self, partition):
        """
        Retourne les donnees d'une partition

        """
        donnees_part = [donnees_liste for donnees_liste in partition]
        donnees_partition = list()
        for donnees in donnees_part:
            for d in donnees:
                donnees_partition.extend([d])

        return donnees_partition

    def p_ci_aj(self, donnees, attribut, valeurs, valeur_partitionnement, classe):
        """
        p(ci|aj) =  la probabilité que la classe soit ci sachant que aj>=valeur_partitionnement (droite)
        ou aj<valeur_partitionnement (gauche)
            :param:
        """
        partition = self.partitionne(donnees, attribut, valeurs, valeur_partitionnement)
        partition_droite = partition["Droite"].values()
        partition_gauche = partition["Gauche"].values()

        donnees_droite = self.donnees_partition(partition_droite)
        donnees_gauche = self.donnees_partition(partition_gauche)

        nombre_donnees_droite = len(donnees_droite)
        nombre_donnees_gauche = len(donnees_gauche)

        # calcul de la probabilité de ci en fonction du côté droit ou gauche
        donnees_ci_gauche = [donnee for donnee in donnees_gauche if donnee[0] == classe]
        donnees_ci_droite = [donnee for donnee in donnees_droite if donnee[0] == classe]

        nombre_ci_droite = len(donnees_ci_droite)
        nombre_ci_gauche = len(donnees_ci_gauche)

        # a droite
        p_ci_aj_droite = nombre_ci_droite / nombre_donnees_droite if nombre_donnees_droite != 0.0 else 0.0
        # a gauche
        p_ci_aj_gauche = nombre_ci_gauche / nombre_donnees_gauche if nombre_donnees_gauche != 0.0 else 0.0

        probabilites = {"Gauche": p_ci_aj_gauche, "Droite": p_ci_aj_droite}
        return probabilites

    def h_C_aj(self, donnees, attribut, valeurs, valeur_partitionnement):
        """
        H(C|aj) = l'entropie de la classe C selon si aj>= ou < a valeur_partitionnement
        """
        # calcule p(ci|aj) pour les classes 1 et 0, a droite et a gauche
        p_cis_aj_0 = self.p_ci_aj(donnees, attribut, valeurs, valeur_partitionnement, '0')
        p_cis_aj_1 = self.p_ci_aj(donnees, attribut, valeurs, valeur_partitionnement, '1')

        # calcul de l'entropie de la classe c a droite et a gauche
        h_c_aj_droite = -sum(
            p_ci_aj * log(p_ci_aj, 2.0) for p_ci_aj in (p_cis_aj_0["Droite"], p_cis_aj_1["Droite"]) if p_ci_aj != 0.0)
        h_c_aj_gauche = -sum(
            p_ci_aj * log(p_ci_aj, 2.0) for p_ci_aj in (p_cis_aj_0["Gauche"], p_cis_aj_1["Gauche"]) if p_ci_aj != 0.0)

        h_c_aj = {"Droite": h_c_aj_droite, "Gauche": h_c_aj_gauche}
        return h_c_aj

    def h_C_A(self, donnees, attribut, valeurs, valeur_partitionnement):
        """
        H(C|A)= l'entropie de la classe C

        """
        partition = self.partitionne(donnees, attribut, valeurs, valeur_partitionnement)

        h_c_aj = self.h_C_aj(donnees, attribut, valeurs, valeur_partitionnement)
        p_aj = self.p_aj(partition)

        h_c_a = h_c_aj["Gauche"] * (1 - p_aj) + h_c_aj["Droite"] * p_aj

        return h_c_a
