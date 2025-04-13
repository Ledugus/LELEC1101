"""Dimensionnement du circuit complet"""

# Importer les bibliothèques nécessaires
import tkinter as tk
from tkinter import ttk

import numpy as np

from arcsin import optimize


# Imposer les spécifications
def impose_specs():
    specs = {
        "f": 1870,  # Fréquence de l'oscillateur
        "V_cc": 15,  # Alimentation
        "V_max": 13.46,  # Tension maximale
        "P_hp": 0.048,  # Puissance du haut-parleur
        "R_hp": 32,  # Résistance du haut-parleur
        "etages": [0, 2, 3, 4],  # Etages de l'oscillateur
    }
    return specs


# Calculer les valeurs dimensionnées
def calculate_emetteur(specs):
    f = specs["f"]
    V_cc = specs["V_cc"]
    V_max = specs["V_max"]
    p_hp = specs["P_hp"]
    r_hp = specs["R_hp"]
    etages = specs["etages"]

    r_hpsup = 200

    # Amplitude de sortie de l'oscillateur
    ampli_osc = np.sqrt(p_hp * r_hp) * (r_hpsup + r_hp) / (r_hp)
    # Valeur arbitraire
    dim = {}

    C = 10e-9
    R3 = 12e3

    # R2 / R3 * V_max = ampli_osc
    R2 = (ampli_osc * R3) / V_max
    # f = R3 / (4 * R2 * R1 *C)
    R1 = R3 / (4 * R2 * f * C)

    dim["R_hp"] = r_hpsup
    dim["R1"] = R1
    dim["R2"] = R2
    dim["R3"] = R3
    dim["C"] = C

    return dim


def calculate_recepteur(specs):
    f = specs["f"]
    V_cc = specs["V_cc"]
    V_max = specs["V_max"]
    R_M = 10e3
    C_M = 1e-6

    dim = {}
    dim["R_M"] = R_M
    dim["C_M"] = C_M

    # Filtre passe-bande

    # Soustracteur

    # Valeur absolue

    # Moyenne

    # Renormalisation

    # Arcsinus

    fun, delta_V, r_opt = optimize(crit="lstsq", etages=specs["etages"])

    dim["DV"] = delta_V
    dim["R_arcsin"] = 1000
    for i, indx in enumerate(specs["etages"]):
        dim[f"R_arcsin_{indx}"] = r_opt[i]

    return dim


def stringify_float(size):
    if abs(size) >= 1:
        if abs(size) > 1e31:
            return "{:.3e}".format(size)
        else:
            for x in [" ", "K", "M"]:
                if abs(size) < 1000.0:
                    y = "%.2f %s" % (size, x)
                    return y
                size /= 1000.0
    if abs(size) < 1:
        if abs(size) < 1e-31:
            return "{:.3e}".format(size)
        elif abs(size) > 0.001:
            return "%3.3f" % size
        else:
            for x in [" ", "m", "u", "n", "p"]:
                if abs(size) > 1:
                    y = "%.2f %s" % (size, x)
                    return y

                size /= 0.001


def show_results(root, new_specs):
    # Create new window
    results_window = tk.Toplevel(root)

    specs = {}
    for key, value in new_specs.items():
        try:
            specs[key] = float(value.get())
        except ValueError:
            specs[key] = value.get()
    specs["etages"] = [int(x) for x in new_specs["etages"].get().split(",")]
    emetteur = calculate_emetteur(specs)
    recepteur = calculate_recepteur(specs)

    tree = ttk.Treeview(results_window)
    tree["columns"] = ("Value", "Unit")
    tree.heading("#0", text="Component")
    tree.heading("Value", text="Value")
    tree.heading("Unit", text="Unit")
    tree.pack()
    for key, value in emetteur.items():
        unit = "Ω" if "R" in key else "F" if "C" in key else ""
        tree.insert("", tk.END, text=key, values=(stringify_float(value), unit))
    for key, value in recepteur.items():
        unit = "Ω" if "R" in key else "F" if "C" in key else "V" if "V" in key else ""
        tree.insert("", tk.END, text=key, values=(stringify_float(value), unit))
    tree.pack()


# Afficher les résultats
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dimensionnement du circuit complet")

    # Get specs from the user
    specs = impose_specs()
    # Get the user input for the specs

    frame = tk.Frame(root)
    new_specs = {}
    for i, (key, value) in enumerate(specs.items()):
        # create variable to hold the value
        if isinstance(value, list):
            value = ", ".join(map(str, value))
        elif isinstance(value, float):
            value = "{:.2f}".format(value)
        new_specs[key] = tk.StringVar(value=value)

        label = tk.Label(frame, text=key)
        label.grid(row=i, column=0)
        entry = tk.Entry(frame, textvariable=new_specs[key])
        entry.grid(row=i, column=1)

    frame.pack()

    # Create a button to calculate the results
    button = tk.Button(
        root, text="Calculate", command=lambda: show_results(root, new_specs)
    )
    button.pack()

    root.mainloop()
