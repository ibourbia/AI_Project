from moteur_id3.id3 import ID3
import csv


class ResultValues():

    def __init__(self):
        
        # Do computations here
        id3=ID3()
        self.filename = str(input("nom du fichier a ouvrir"))
        # Task 1
        self.arbre = id3.construit_arbre(self.get_datas())
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]

    def get_datas(self) :
        """
        Extrait les donnees du fichier csv

        :return: donnees, une liste avec une valeur de classe
                 et un dictionnaire associant attributs et valeurs

        """
        #the datas as a list of dictionnaries
        donnees=[]
        #open the file with encoding utf8-sig because of strange characters
        with open(self.filename , newline ='\n',encoding='utf-8-sig') as datas :
            #retrieves datas as a reader over dictionnaries
            dict_reader=csv.DictReader(datas,delimiter=',')
            #converts each row from OrderedDict to Dictionnary
            #Creates a list of datas
            for dct in map(dict,dict_reader):
                single_data=[]
                single_data.append(dct.pop("target"))
                single_data.append(dct)
                donnees.append(single_data)

        return donnees





