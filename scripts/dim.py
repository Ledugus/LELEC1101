"""Dimensionnement du circuit complet"""

# Importer les bibliothèques nécessaires
import tkinter as tk
from tkinter import ttk

import numpy as np

from arcsin import optimize


# Imposer les spécifications
def impose_specs():
    specs = {
        "f": 1380,  # Fréquence de l'oscillateur
        "V_cc": 15,  # Alimentation
        "V_sat": 13.56,  # Tension maximale
        "V_moy_max": 12,
        "V_moy_min": 0.6,
        "P_hp": 0.05,  # Puissance du haut-parleur
        "R_hp": 32,  # Résistance du haut-parleur
        "etages": [0, 1, 2, 3],  # Etages de l'oscillateur
        "f_coupure_moyenne": 80,  # Fréquence de coupure
        "Q": 3.15,  # Facteur de qualité
        "H": 13,  # Gain du filtre
    }
    return specs


# Calculer les valeurs dimensionnées
def calculate_emetteur(specs):
    f = specs["f"]
    V_cc = specs["V_cc"]
    V_sat = specs["V_sat"]
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

    # R2 / R3 * V_sat = ampli_osc
    R2 = (ampli_osc * R3) / V_sat
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
    V_sat = specs["V_sat"]
    V_moy_max = specs["V_moy_max"]
    V_moy_min = specs["V_moy_min"]
    dim = {}

    # Micros

    R_M = 10e3
    C_M = 1e-6

    dim["R_M"] = R_M
    dim["C_M"] = C_M

    # Filtre passe-bande

    C_PB1 = 10e-9
    C_PB2 = 10e-9

    Q = specs["Q"]
    H = specs["H"]
    w0 = f * 2 * np.pi
    C = 10e-9
    R_PB1 = Q / (w0 * H * C)
    R_PB2 = (Q / w0) * ((2 * C) / (C * C))
    R_PB3 = 1 / ((Q * w0 * (2 * C)) - ((w0 * H * C) / Q))

    dim["R_PB1"] = R_PB1
    dim["R_PB2"] = R_PB2
    dim["R_PB3"] = R_PB3
    dim["C_PB1"] = C_PB1
    dim["C_PB2"] = C_PB2

    # Soustracteur

    A1 = 1
    A2 = 1
    R_S1 = 10000
    R_S2 = 10000
    R_S3 = 10000
    R_S4 = 10000
    dim["R_S1"] = R_S1
    dim["R_S2"] = R_S2
    dim["R_S3"] = R_S3
    dim["R_S4"] = R_S4

    # Valeur absolue

    # Moyenne
    f_coup = specs["f_coupure_moyenne"]
    C_MOY1 = 100e-9
    C_MOY2 = 100e-9
    R_MOY1 = 1 / (2 * np.pi * f_coup * C_MOY1)
    R_MOY2 = 2 * R_MOY1

    dim["R_MOY1"] = R_MOY1
    dim["R_MOY2"] = R_MOY2

    # Arcsinus

    fun, delta_V, r_opt = optimize(crit="lstsq", etages=specs["etages"])

    dim["DV"] = delta_V
    dim["R_arcsin"] = 1000
    for i, indx in enumerate(specs["etages"]):
        dim[f"R_arcsin_{indx}"] = r_opt[i]

    # Renormalisation
    # R4(R1+R2)/R1(R3+R4) = 2 * DV / (V_moy_max - V_moy_min)
    # R2/R1 = (DV) / V_CC
    R2 = 1200
    R4 = 1200
    R1 = R2 * V_cc / delta_V
    R3 = R4 * (R1 + R2) * (V_moy_max - V_moy_min) / (R1 * (2 * delta_V)) - R4
    dim["R_NORM1"] = R1
    dim["R_NORM2"] = R2
    dim["R_NORM3"] = R3
    dim["R_NORM4"] = R4

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
