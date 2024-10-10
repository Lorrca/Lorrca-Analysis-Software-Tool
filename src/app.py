import matplotlib.pyplot as plt

from src.core.entities.osmo_model import OsmoModel

data = {
    "EI": [
        0.117, 0.118, 0.128, 0.115, 0.108, 0.11, 0.107, 0.13, 0.171, 0.209,
        0.236, 0.265, 0.261, 0.251, 0.241, 0.235, 0.231, 0.228, 0.228,
        0.232,
        0.236, 0.241, 0.249, 0.258, 0.269, 0.281, 0.293, 0.305, 0.317,
        0.329,
        0.341, 0.352, 0.363, 0.374, 0.386, 0.396, 0.405, 0.414, 0.422,
        0.43,
        0.438, 0.447, 0.453, 0.46, 0.466, 0.471, 0.475, 0.482, 0.486,
        0.489,
        0.494, 0.498, 0.501, 0.505, 0.51, 0.512, 0.515, 0.516, 0.516,
        0.516,
        0.515, 0.516, 0.517, 0.515, 0.514, 0.514, 0.511, 0.507, 0.507,
        0.506,
        0.501, 0.5, 0.5, 0.497, 0.496, 0.498, 0.497, 0.496, 0.496, 0.495,
        0.494, 0.492, 0.488, 0.486, 0.482, 0.479, 0.477, 0.474, 0.469,
        0.467,
        0.465, 0.46, 0.457, 0.455, 0.451, 0.446, 0.444, 0.442, 0.439,
        0.437,
        0.435, 0.432, 0.428, 0.424, 0.418, 0.411, 0.405, 0.399, 0.392,
        0.387,
        0.381, 0.373, 0.364, 0.355, 0.344, 0.333, 0.323, 0.313, 0.304,
        0.293,
        0.281, 0.269, 0.257, 0.245, 0.234, 0.224, 0.214, 0.203, 0.193,
        0.184,
        0.174, 0.166, 0.158, 0.149, 0.14, 0.131, 0.122, 0.114, 0.106,
        0.098,
        0.09, 0.083, 0.076, 0.069, 0.063, 0.056, 0.048, 0.041, 0.035,
        0.027,
        0.021, 0.016, 0.01, 0.005, -0.001, -0.007, -0.013, -0.018, -0.024,
        -0.028,
        -0.033, -0.037, -0.041, -0.044, -0.047, -0.051, -0.054, -0.058,
        -0.062, -0.066,
        -0.069, -0.073, -0.076, -0.079, -0.083, -0.085, -0.088, -0.091,
        -0.093, -0.095,
        -0.097, -0.098, -0.1, -0.105, -0.106, -0.108, -0.11, -0.111,
        -0.112, -0.113,
        -0.111, -0.11, -0.111, -0.111, -0.111, -0.114, -0.116, -0.117,
        -0.118, -0.118,
        -0.118, -0.119, -0.119, -0.119, -0.119, -0.117, -0.116, -0.116,
        -0.115, -0.112,
        -0.111, -0.108, -0.106, -0.104, -0.103, -0.102, -0.101, -0.1, -0.1,
        -0.099,
        -0.098, -0.096, -0.094, -0.092, -0.089, -0.086, -0.084, -0.082,
        -0.079, -0.078,
        -0.076, -0.075, -0.073
    ],
    "O.": [
        66.75, 73.2, 75.76, 77.6, 79.24, 83.62, 85.99, 88.57, 91.07, 93.49,
        95.86, 98.16, 100.45, 102.83, 105.12, 107.29, 109.5, 111.75,
        113.88, 115.97,
        118.02, 120.11, 122.11, 124.16, 126.21, 128.21, 130.22, 132.15,
        134.07, 136.08,
        138.12, 140.17, 142.14, 144.1, 146.23, 148.32, 150.29, 152.46,
        154.67, 156.67,
        158.8, 161.1, 163.47, 165.77, 168.18, 170.6, 173.01, 175.39,
        177.85, 180.3,
        182.8, 185.3, 187.92, 190.42, 192.92, 195.37, 197.91, 200.45,
        202.91, 205.36,
        207.9, 210.36, 212.82, 215.44, 217.98, 220.47, 223.05, 225.51,
        228.01, 230.43,
        232.92, 235.26, 237.8, 240.21, 242.59, 244.96, 247.46, 249.92,
        252.42, 254.83,
        257.33, 259.7, 262.28, 264.86, 267.49, 270.15, 272.73, 275.14,
        277.52, 279.93,
        282.35, 284.81, 287.39, 290.01, 292.59, 295.09, 297.75, 300.29,
        302.78, 305.36,
        307.9, 310.32, 312.98, 315.68, 318.18, 320.93, 323.5, 326.0,
        328.54, 331.24,
        333.78, 336.61, 339.19, 341.77, 344.47, 346.85, 349.39, 351.97,
        354.67, 357.08,
        359.87, 362.28, 364.74, 367.28, 369.82, 372.15, 374.61, 377.19,
        379.44, 381.9,
        384.44, 386.81, 389.15, 391.56, 394.1, 396.48, 399.18, 401.6,
        404.38, 406.84,
        409.54, 412.0, 414.54, 416.91, 419.45, 421.66, 424.16, 426.58,
        428.99, 431.53,
        434.19, 436.69, 439.39, 442.06, 444.64, 447.34, 449.92, 452.29,
        454.67, 457.12,
        459.5, 461.96, 464.29, 466.67, 469.04, 471.33, 473.63, 476.08,
        478.5, 481.04,
        483.54, 486.08, 488.62, 491.28, 493.69, 496.4, 499.06, 501.47,
        503.77, 506.02,
        508.19, 510.28, 512.65, 514.95, 517.24, 519.33, 521.58, 523.87,
        526.21, 528.46,
        530.75, 533.01, 535.3, 537.26, 539.6, 542.01, 544.43, 546.56,
        549.18, 551.6,
        553.85, 556.14, 558.72, 560.85, 563.14, 565.19, 567.65, 569.53,
        571.91, 573.83,
        575.84, 577.31, 579.28, 581.04, 583.01, 584.97, 586.9, 588.78,
        590.42, 592.06,
        593.94, 595.62, 597.13, 598.93, 600.65, 602.05, 603.81, 605.12,
        606.67, 608.11,
        609.46, 610.85, 612.37
    ]
}

model = OsmoModel(data)

# (EI) Elongation Index values
ei_max = model.ei_max
ei_hyper = model.ei_hyper

# (O) Osmolality values
o_max = model.o_max
o_hyper = model.o_hyper

valley_idx = model.valley_idx
peak_idx = model.first_peak_idx


def main():
    console_output()
    plot_chart()


def console_output():
    print(f"EI_max = '{ei_max}'")
    print(f"EI_hyper = '{ei_hyper}'")
    print(f"O_max '{o_max}'")
    print(f"O_hyper '{o_hyper}'")


def plot_chart():
    _fig, ax = plt.subplots(figsize=(16, 9))

    # Plot original points and the polynomial curve
    ax.plot(model.o, model.ei, label='EI', linewidth=1)

    # Mark the peak with the highest prominence
    ax.plot(model.o[peak_idx], model.ei[peak_idx],
            "o", color='g', markersize=4,
             label='Highest Prominence Peak')

    ax.plot(model.o[valley_idx], model.ei[valley_idx], "o",
             label="Highest Prominence Valley", color="r", markersize=4)

    # Plot vertical lines to o_hyper and o_max
    ax.plot([o_hyper, o_hyper], [min(model.ei), ei_hyper], color='r',
            linestyle='--', linewidth=0.75)  # O_hyper vertical line
    ax.plot([o_max, o_max], [min(model.ei), ei_max], color='r',
            linestyle='--', linewidth=0.75)  # O_max vertical line

    ei_margin = 0.01 * (max(model.ei) - min(model.ei))
    o_margin = 0.01 * (max(model.o) - min(model.o))

    # Set limits with margins
    ax.set_ylim(bottom=min(model.ei) - ei_margin,
                top=max(model.ei) + ei_margin)
    ax.set_xlim(left=min(model.o) - o_margin, right=max(model.o) + o_margin)

    # Add title and labels
    ax.set_xlabel('Osmolality [mOsm/kg]')
    ax.set_ylabel('Elongation Index [EI]')
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
