# Cette page permet d'ouvrir un fichier excel pour récuperer les
# données qui nous intéressent et les placer dans un fichier csv.
# Code : Luc Degrève


import xlrd                                                 # Permet la lecture d'un fichier excel
from xlwt import Workbook                                   # Permet l'écriture d'un fichier

enter_data='C:/Users/Luc/PycharmProjects/Données.xlsm'      # Fichier excel contenant les données.
exit_data='C:/Users/Luc/PycharmProjects/Datasortie.csv'     # Fichier de sortir.

document = xlrd.open_workbook(enter_data)                   # Overture du fichier excel
data = document.sheet_by_index(0)                           # Selection de la feuille contenant les données

nbrow=data.nrows                                            # Nombre de le ligne
nbcol=data.ncols                                            # Nombre de le colonne

book=Workbook()                                             # Mise en place du nouveau fichier
feuil1 = book.add_sheet('view_data')                        # Création de la feuille 1

for k in range(0,nbcol):                                    # Acquisition des données
    for i in range(0,nbrow-1):
        feuil1.write(i, k,data.cell_value(rowx=(i+1), colx=k))

book.save(exit_data)                                        # Création du nouveau fichier