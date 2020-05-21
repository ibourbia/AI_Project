from moteur_id3.id3 import ID3
import csv


def abduction_element(liste, abduct):
    """
    :param liste: liste à traiter
    :param abduct: liste d'element à retirer de :liste:
    :return: liste abductée des éléments de :abduct:
    """
    update = []
    for e in liste:
        flag = False
        for a in abduct:
            if a in e:
                flag = True
                # print("abduct", e)
                break
        if not flag:
            update.append(e)
    return update


class ResultValues():

    def __init__(self):
        # Do computations here
        id3 = ID3()
        self.filename = "train_bin.csv"  # str(input("nom du fichier a ouvrir"))
        # Task 1
        self.arbre = id3.construit_arbre(self.get_datas())
        # Task 2
        self.donnees_train = self.get_datas("train_bin.csv")
        self.donnees_test = self.get_datas("test_public_bin.csv")
        self.precision_rate = self.test_precision()
        # Task 3
        self.faits_initiaux = self.define_faits_initiaux()
        self.regles = self.define_regles(self.arbre)
        self.define_regles(self.arbre, [])
        self.attributs = self.get_attributs()
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]

    def get_datas(self, filename=None):
        """
        Extrait les donnees du fichier csv

        :return: donnees, une liste avec une valeur de classe
                 et un dictionnaire associant attributs et valeurs

        """
        if filename is None:
            filename = self.filename
        # the datas as a list of dictionnaries
        donnees = []
        # open the file with encoding utf8-sig because of strange characters
        with open(filename, newline='\n', encoding='utf-8-sig') as datas:
            # retrieves datas as a reader over dictionnaries
            dict_reader = csv.DictReader(datas, delimiter=',')
            # converts each row from OrderedDict to Dictionnary
            # Creates a list of datas
            for dct in map(dict, dict_reader):
                single_data = []
                single_data.append(dct.pop("target"))
                single_data.append(dct)
                donnees.append(single_data)

        return donnees

    def get_attributs(self):
        attributs = []
        for k in self.donnees_train[0][1].keys():
            attributs.append(k)
        return attributs

    def test_precision(self):
        """
        :param: no parameters
        :return: return the precision percentage
        """
        total = len(self.donnees_test)
        # Extraction of class value for each subject
        results = [d[0] for d in self.donnees_test]
        # Prediction of each subject's class using the model
        results_test = [self.arbre.classifie(d[1]) for d in self.donnees_test]
        # Precision calculation
        precision = 0
        if len(results) == len(results_test):
            for i, j in zip(results, results_test):
                # on a besoin seulement du dernier element de j
                if str(i) == j[-1]:
                    precision = precision + 1
            return (precision / total) * 100
        else:
            raise NameError("Error: number of results != number of predictions")

    def define_faits_initiaux(self):
        """
        Creer une liste des faits initiaux a partir des donnees de train
        """
        donnees = [d[1] for d in self.donnees_train]
        faits_initiaux = []
        for d in donnees:
            fait = []
            for key, val in d.items():
                fait.append(str(key) + "-" + str(val))
            faits_initiaux.append(fait)
        print(faits_initiaux)
        return faits_initiaux

    def define_regles(self, noeud=None, premisse=[]):
        """
        Extrait les regles de l'arbre. Methode recursive. Traite les noeuds de l'arbre en recuperant les premisses et
        en assemblant les regles
            :param: noeud : la racine de l'arbre/la branche de l'arbre qu'on parcourt
                    premisse : les attributs parents de noeud
            :return: regles : les regles 

        """
        # au cas ou
        if noeud is None:
            noeud = self.arbre

        if noeud.terminal():
            # une regle unique instanciée lorsqu'on arrive au bout de la branche
            regle = [[premisse, noeud.classe()]]
            return regle

        else:
            regles = []
            # recursion
            for val, enfant in noeud.enfants.items():
                # Nouvelle regle
                r1 = []
                # on fait une copie pour eviter les listes de liste de liste etc...
                pre_copy = premisse.copy()
                pre_copy.append(str(noeud.attribut) + '-' + str(val))
                r1 = self.define_regles(enfant, pre_copy)
                # toutes les regles
                regles.extend(r1)
            return regles

    def process_example(self, example=None):
        """
        :param: prend un ensemble de faits initiaux
        :return: retourne la règle qui a mené à la conclcusion si elle est présente dans l'ensemble de regles
        retourne une liste vide si aucune regle n'a ete trouvee
        """
        if example is None:
            return []
        else:
            for regle in self.regles:
                # all() :  retourne true si toutes les propositions sont vraies
                # verifie si les conditions/premisses d'une regle sont presentes dans un fait
                if all(r in example for r in regle[0]):
                    # print('1')
                    return regle
            # print('0')
            return []

    def affiche_ccl(self, example=None):
        """
        Méthode affichant la conclusion de l'exemple traité
        :param: prend une liste d'attribut correspondant à l'état d'un patient
        :return: affiche la conclusion et retourne la règle responsable / retourne une liste vide si aucun exemple n'est fourni
        ou qu'aucune règle n'a pu etre trouvée
        """
        if example is None:
            print("Aucun exemple fourni")
            return []
        conclusion = self.process_example(example)
        if len(conclusion) == 0:
            print("Aucune conclusion ne peut être faite car on ne appliquer aucune de l'ensemble défini")
            return []
        elif conclusion[1] == '1':
            print("Le patient a un risque de maladie car il rempli les conditions :", conclusion[0])
            return conclusion[0]
        elif conclusion[1] == '0':
            print("Le patient ne présente pas de risque de maladie car il rempli les conditions :", conclusion[0])
            return conclusion[0]

    def diagnostique(self, example=None):
        """
        :param example: une liste correspondant aux caractéristiques d'un patient
        :return: retourne une liste  de listes de tuples comprenant (attribut-valeur, attribut-nouvelle_valeur).
        Chaque sous liste correspond aux changements qu'il faudrait faire pour correspondre à une règle ayant la conclusion '0'
        """
        # Construction de l'ensemble de premisse qui mène à la conclusion '0'
        non_P = [r[0] for r in self.regles if r[1] == '0']

        if example is None:
            print("Aucun exemple fourni")
            return []
        # On obtient la regle qui mene qui traite l'exemple
        regle = self.process_example(example)
        if len(regle) == 0:
            return []
        else:
            premisses = regle[0]
            conclusion = regle[1]
            age = None
            sex = None
            for element in example:
                if 'age' in element:
                    age = element
                if 'sex' in element:
                    sex = element
            if conclusion == '1':
                # Isolation des regles avec une conclusion '1' les plus proches des premisses de l'exemple
                predicats_positif = []
                pre = premisses.copy()
                pre.pop()
                for p in non_P:
                    q = p.copy()
                    while len(q) > 0:
                        q.pop()
                        if all(e in pre for e in q):
                            predicats_positif.append(p)
                # On retire tous les predicats comportant un changement de 'sex' ou de 'age'
                predicats = []
                if age is not None and sex is not None:
                    for p in predicats_positif:
                        if all('age' not in e for e in p) and all('sex' not in e for e in p):
                            predicats.append(p)
                        if age in p and sex in p:
                            predicats.append(p)
                        if age in p and all('sex' not in e for e in p):
                            predicats.append(p)
                        if sex in p and all('age' not in e for e in p):
                            predicats.append(p)
                # Construction d'une liste stockant tous les changements possibles
                variables = []
                for p in predicats:
                    l = []
                    for att in self.attributs:
                        if att == 'sex' or att == 'age':
                            pass
                        else:
                            for pre in example:
                                for el in p:
                                    if att in el and att in pre:
                                        if el != pre:
                                            l.append((pre, el))
                    if len(l) > 0:
                        variables.append(l)

                #print("Patient : ", premisses, example)
                #print("VAR : ", variables)
                #print("Liste des modifications")
                return variables
            elif conclusion == '0':
                print("La prédiction ne mène à aucune maladie")
                return []
