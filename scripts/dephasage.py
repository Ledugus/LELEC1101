"""Génération des images pour la section "Méthode de calcul de l'angle" du rapport intermédiaire et final."""

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 14})


def square(t, a, deph):
    """Retourne le signal carré de période 1, d'amplitude a et de déphasage deph."""
    return a * (np.sign(np.sin(np.pi * (t - deph))))


def graph_deph(path="output/plots/aires.pdf"):
    """Trace les graphes de u(t) et u(t+deph) pour deph=0, 0.25, 0.5 et 0.75."""
    t = np.linspace(0, 2, 1000)

    fig = plt.figure(figsize=(12, 8))
    for i, deph in enumerate([0, 0.25, 0.5, 0.75]):
        a = plt.subplot(2, 2, i + 1)
        plt.title(f"$\phi={deph}*\pi$")
        plt.plot(t, square(t, 1, 0), label=r"$u_1$", linewidth=2)
        plt.plot(t, square(t, 1, deph), label=r"$u_2$", linewidth=2)
        diff = (square(t, 1, 0) - square(t, 1, deph)) / 2
        plt.plot(t, diff, label=f"diff", linewidth=2)
        plt.fill_between(t, diff, color="green", alpha=0.3)

        a.set_yticks(
            [-1, 0, 1],
            labels=[r"-$V_{cc}$", r"0", r"$V_{cc}$"],
            minor=False,
        )
        plt.xlabel("$t$")
        plt.ylabel("$u(t)$")
        plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(path)


if __name__ == "__main__":
    graph_deph()
