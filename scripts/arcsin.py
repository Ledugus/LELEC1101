import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

R = 1000
Vd = 0.7


def arcsinus(v, v_max):
    return -v_max * np.arcsin(v / v_max)


def get_linear_interp(v: float, v_max, r: list[float], etages=range(4), R=1000):
    for i in range(len(etages) - 1):
        if v <= Vd * (etages[i + 1]):
            return -R * (sum((v - Vd * etages[j]) / r[j] for j in range(i + 1)))
    if v <= v_max:
        return -R * (sum((v - Vd * etages[j]) / r[j] for j in range(len(etages))))

    return 0


def optimize(crit="lstsq", etages=range(4), R=1000, Vd=0.7):
    """
    Optimize the parameters for the arcsinus function.
    """

    def objective(params):
        v = np.linspace(0, params[0], 100)
        arcs = arcsinus(v, params[0])
        if crit == "max":
            return max(
                abs(
                    get_linear_interp(v[i], params[0], params[1:], etages=etages)
                    - arcs[i]
                )
                for i in range(len(v))
            )
        elif crit == "abs":
            return np.sum(
                [
                    abs(
                        get_linear_interp(v[i], params[0], params[1:], etages) - arcs[i]
                    )
                    for i in range(len(v))
                ]
            )
        elif crit == "mean":
            return abs(
                np.mean(
                    [
                        (
                            get_linear_interp(v[i], params[0], params[1:], etages)
                            - arcs[i]
                        )
                        for i in range(len(v))
                    ]
                )
            )
        elif crit == "lstsq":
            return (
                np.sum(
                    [
                        (
                            get_linear_interp(v[i], params[0], params[1:], etages)
                            - arcs[i]
                        )
                        ** 2
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
    return result.fun, result.x[0], result.x[1:]


def plot_optimization(etages):
    """
    Plot the results of the optimization.
    """
    plt.subplots(2, 2, figsize=(10, 8))
    i = 1
    file_name = "output/" + "-".join(map(str, etages)) + ".txt"
    with open(file_name, "w") as f:

        for crit in ["max", "abs", "mean", "lstsq"]:
            plt.subplot(2, 2, i)
            i += 1
            quality, v_max, r_opt = optimize(crit=crit, etages=etages)
            print(
                f"Criterion: {crit}, Quality: {quality:.2f}, Params: {v_max}, {r_opt}"
            )
            v = np.linspace(0, v_max, 1000)
            arcs = arcsinus(v, v_max)
            f.write(
                f"Criterion: {crit}, Quality: {quality}, Params:\n"
                + str(v_max)
                + ", "
                + ", ".join(map(str, r_opt))
                + "\n"
            )

            y = [get_linear_interp(v[i], v_max, r_opt, etages) for i in range(len(v))]
            plt.plot(v, arcs, label="Arcsin")
            plt.plot(v, y, label=f"Optimized {crit}")
            plt.legend()
            plt.title(f"Criterion: {crit}, Quality: {quality:.2f}")
            plt.grid()
    plt.savefig("output/plots/" + "-".join(map(str, etages)) + ".png")
    plt.show()


def plot_solution(DV, r_opt, etages, R=1000):
    v = np.linspace(0, DV, 1000)
    arcs = arcsinus(v, DV)
    y = [get_linear_interp(v[i], DV, r_opt, etages, R=R) for i in range(len(v))]

    plt.plot(v, arcs, label="Arcsin")
    plt.plot(v, y, label="Optimized")
    plt.title(f"R0={R}, r_opt={r_opt}, DV={DV}")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    r_opt = [5600, 56000, 10000, 1500]
    etages = [0, 1, 2, 3]
    R = 5600
    test_etages = [0, 1, 2, 3]
    DV = 2.3
    plot_solution(DV, r_opt, etages, R=R)
    # plot_optimization(test_etages)
