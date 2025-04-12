import numpy as np
from matplotlib import pyplot as plt
import os
import linecache

# Petit script pour avoir tous les graphes des données dans un dossier sour format pdf.
# Pour que ça marche bien :
# .txt pour les fichiers LTSpice (Pour une analyse fréquentielle à mon avis ça foire)
# .csv pour les fichiers scopy

# Titre du graphique : le nom du fichier avec les _ remplacés par des espaces
# Nom pour la légende : il faut aller rennomer le nom des colonnes dans le fichier où les données se trouvent par le nom voulu (sans enlever la virgule ou tab)

dir_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/"
)  # Dossier répertoire courant


def scopy_file(name):
    """Traite un fichier scopy

    Args:
        name (str): nom du fichier dans le dossier courant
    """
    file = dir_path + name
    labels = []
    first_line = linecache.getline(file, 8)
    labels = first_line.split(",")

    data_matrix = np.loadtxt(file, skiprows=8, delimiter=",", unpack=True)
    time = data_matrix[1]

    plt.figure()
    for i in range(2, len(data_matrix)):
        plt.plot(time, data_matrix[i], label=labels[i])

    title = name.replace(".csv", "")
    title = title.replace("_", " ")
    plt.title(title.capitalize())
    plt.xlabel("Time (S)")
    plt.legend()

    # Sauvegarde en pdf
    save_file = dir_path + name.replace(".csv", ".pdf")
    if os.path.isfile(save_file):
        os.remove(save_file)
    plt.savefig(save_file)


def LTSpice_file(name):
    """Traite un fichier de données LTSpice en .txt

    Args:
        name (str): nom du fichier dans le dossier courant

    Returns:
        Graphique des données en format .pdf
    """
    file = dir_path + name
    labels = []
    with open(file) as f:
        first_line = f.readline()
        labels = first_line.split("\t")
        labels = labels[1:]

    data_matrix = np.loadtxt(file, skiprows=1, delimiter="\t", unpack=True)
    time = data_matrix[0]

    plt.figure()

    for i in range(len(labels)):
        plt.plot(time, data_matrix[i + 1], label=labels[i])

    title = name.replace(".txt", "")
    title = title.replace("_", " ")
    plt.title(title.capitalize())
    plt.xlabel("Time (S)")
    plt.legend()

    # Sauvegarde en pdf
    save_file = file.replace(".txt", ".pdf")
    print("Save location" + save_file)
    if os.path.isfile(save_file):
        os.remove(save_file)
    plt.savefig(save_file)


file_list = os.listdir(dir_path)


# main
for name in file_list:
    if ".csv" in name:
        scopy_file(name)
    elif ".txt" in name:
        LTSpice_file(name)
    else:
        continue
    with open(dir_path + name) as f:
        first_line = f.readline()
        if "Scopy" in first_line:
            scopy_file(name)
        elif "time" in first_line:
            LTSpice_file(name)
