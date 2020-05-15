from moteur_id3.id3 import ID3
import csv


class ResultValues():

    def __init__(self):
        # Do computations here
        id3 = ID3()
        self.filename = "train_bin.csv"  # str(input("nom du fichier a ouvrir"))
        # Task 1
        self.arbre = id3.construit_arbre(self.get_datas())
        # Task 2
        self.precision_rate = self.test_precision()
        # Task 3
        self.faits_initiaux = ["cp-2", "sex-1", "slope-0", "trestbps-1"]
        self.regles = self.define_regles(self.arbre)
        self.define_regles(self.arbre, [])
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

    def test_precision(self):
        """
        :param: no parameters
        :return: return the precision percentage
        """
        donnees_test = self.get_datas("test_public_bin.csv")
        total = len(donnees_test)
        # Extraction of class value for each subject
        results = [d[0] for d in donnees_test]
        # Prediction of each subject's class using the model
        results_test = [self.arbre.classifie(d[1]) for d in donnees_test]
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

    def define_regles(self, noeud=None, premisse=[]):
        """
        Extrait les regles de l'arbre. Methode recursive. Traite les noeuds de l'arbre en recuperant les premisses et
        en assemblant les regles
            :param:
            :return:

        """
        if noeud is None:
            noeud = self.arbre

        if noeud.terminal():
            # conclusion = str()
            # if noeud.classe()=='1':
            #     conclusion = "Risque de Maladie"
            # else :
            #     conclusion = 'Pas de risque de Maladie'
            regle = [[premisse, noeud.classe()]]
            return regle

        else:
            regles = []
            for val, enfant in noeud.enfants.items():
                r1 = []
                pre_copy = premisse.copy()
                pre_copy.append(str(noeud.attribut) + '-' + str(val))
                r1 = self.define_regles(enfant, pre_copy)
                regles.extend(r1)
            return regles

    def process_example(self):
        """
        :param: prend un ensemble de faits initiaux
        :return: retourne la règle qui a mené à la conclcusion si elle est rpésente dans l'ensemble de regles
        retourne une liste vide si aucune regle n'a ete trouvee
        """
        for regle in self.regles:
            if all(fait in regle[0] for fait in self.faits_initiaux):
                if regle[1] == '1':
                    print("Le patient a un risque de maladie car il rempli les conditions :", regle[0])
                    return regle
                if regle[1] == '0':
                    print("Le patient ne présente pas de risque de maladie car il rempli les conditions :", regle[0])
                    return regle
        print("Aucune conclusion ne peut être faite car on ne appliquer aucune de l'ensemble défini")
        return []