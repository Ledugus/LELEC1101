import numpy as np
import matplotlib.pyplot as plt

# Charger les données depuis le fichier texte
# Assurez-vous que le fichier 'data.txt' est dans le même dossier que votre script ou spécifiez le chemin complet
data = np.loadtxt("Labo7\oscillateurLT.txt", delimiter="\t", skiprows=1)

# Séparer les colonnes
time = data[:, 0]
# Vin = data[:, 1]
Vout = data[:, 1]

# Créer le graphique
plt.figure(figsize=(10, 6))
# plt.plot(time, Vin, label="Vin", color='blue')
plt.plot(time, Vout, label="Vout", color="red")

# Ajouter des labels et un titre
plt.xlabel("Temps (s)")
plt.ylabel("Tension (V)")
plt.title("Evolution de la tension Vout en fonction du temps")
plt.legend()

# Afficher le graphique
plt.grid(True)
plt.show()
