import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

R = 1000
Vd = 0.7


def arcsinus(v, v_max):
    return -v_max * np.arcsin(v / v_max)


def get_linear_interp(v: float, params: list[float], etages=range(4)):
    for i in range(len(etages) - 1):
        if v <= Vd * (etages[i + 1]):
            return -R * (
                sum((v - Vd * etages[j]) / params[j + 1] for j in range(i + 1))
            )
    if v <= params[0]:
        return -R * (
            sum((v - Vd * etages[j]) / params[j + 1] for j in range(len(etages)))
        )

    return 0


def optimize(crit="max", etages=range(4)):
    """
    Optimize the parameters for the arcsinus function.
    """

    def objective(params):
        v = np.linspace(0, params[0], 100)
        arcs = arcsinus(v, params[0])
        if crit == "max":
            return max(
                abs(get_linear_interp(v[i], params, etages) - arcs[i])
                for i in range(len(v))
            )
        elif crit == "abs":
            return np.sum(
                [
                    abs(get_linear_interp(v[i], params, etages) - arcs[i])
                    for i in range(len(v))
                ]
            )
        elif crit == "mean":
            return abs(
                np.mean(
                    [
                        (get_linear_interp(v[i], params, etages) - arcs[i])
                        for i in range(len(v))
                    ]
                )
            )
        elif crit == "lstsq":
            return (
                np.sum(
                    [
                        (get_linear_interp(v[i], params, etages) - arcs[i]) ** 2
                        for i in range(len(v))
                    ]
                )
                / params[0]
            )
        return 0

    params0 = np.ones(len(etages) + 1) * R
    params0[0] = (etages[-1] + 1) * Vd
    bounds = np.concatenate(
        (
            [(Vd * etages[-1], Vd * (etages[-1] + 2)), (500, 1500)],
            [(200, 30000) for _ in range(len(etages) - 1)],
        )
    )
    result = opt.minimize(objective, params0, bounds=bounds)
    return result.fun, result.x


def plot_results(etages):
    """
    Plot the results of the optimization.
    """
    plt.subplots(2, 2, figsize=(10, 8))
    i = 1
    file_name = "conformateur/" + "-".join(map(str, etages)) + ".txt"
    with open(file_name, "w") as f:

        for crit in ["max", "abs", "mean", "lstsq"]:
            plt.subplot(2, 2, i)
            i += 1
            quality, params_opt = optimize(crit=crit, etages=etages)
            v = np.linspace(0, params_opt[0], 1000)
            arcs = arcsinus(v, params_opt[0])
            f.write(
                f"Criterion: {crit}, Quality: {quality}, Params:\n"
                + ", ".join(map(str, params_opt))
                + "\n"
            )

            y = [get_linear_interp(v[i], params_opt, etages) for i in range(len(v))]
            plt.plot(v, arcs, label="Arcsin")
            plt.plot(v, y, label=f"Optimized {crit}")
            plt.legend()
            plt.title(f"Criterion: {crit}, Quality: {quality:.2f}")
            plt.grid()
    plt.savefig("conformateur/" + "-".join(map(str, etages)) + ".png")
    plt.show()


if __name__ == "__main__":
    test_etages = [0, 2, 3, 4]
    plot_results(test_etages)
