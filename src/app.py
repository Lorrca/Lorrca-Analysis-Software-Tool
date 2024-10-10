import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

from src.core.models.osmo_model import OsmoModel

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

o_max_idx = model.o_max_idx


def main():
    # console_output()
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

    # EI_max
    # ax.plot(model.o[o_max_idx], model.ei[o_max_idx], "o", color="yellow",
    #         label=f"Original EI_max ({ei_max})", markersize=4)

    # Mark the peak with the highest prominence
    # ax.plot(model.o[peak_idx], model.ei[peak_idx],
    #         "o", color="g", markersize=4,
    #         label=f"Highest Prominence Peak ({round(model.o[peak_idx])}, {model.ei[peak_idx]})")
    #
    # ax.plot(model.o[valley_idx], model.ei[valley_idx], "o",
    #         label=f"Highest Prominence Valley ({round(model.o[valley_idx])}, {model.ei[valley_idx]})",
    #         color="r", markersize=4)

    # Plot points for EI_max and EI_hyper
    # ax.plot(o_max, ei_max, "o",
    #         label=f"EI_max {round(o_max), round(ei_max, 3)}", color="orange",
    #         markersize="4")
    # ax.plot(o_hyper, ei_hyper, "o",
    #         label=f"EI_Hyper {round(o_hyper), round(ei_hyper, 3)}",
    #         color="pink", markersize="4")

    # Plot vertical lines to o_hyper and o_max
    # ax.plot([o_hyper, o_hyper], [min(model.ei), ei_hyper], color='r',
    #         linestyle='--', linewidth=0.75)  # O_hyper vertical line
    # ax.plot([o_max, o_max], [min(model.ei), ei_max], color='r',
    #         linestyle='--', linewidth=0.75)  # O_max vertical line

    valley_upper_idx = find_breaking_point(ax, valley_idx, o_max_idx, 5, "Left")
    print(f"Peak Index: {model.o[peak_idx]}, {model.ei[peak_idx]}")
    print(f"Valley Upper Index: {model.o[valley_upper_idx]}, {model.ei[valley_upper_idx]}")

    # Valley polynomial
    plot_poly_chart_middle(ax, peak_idx, valley_upper_idx, 4)

    # Top part polynomial
    plot_poly_chart_middle(ax, valley_upper_idx, int(len(model.o) * 0.45), 4)
    print(f"Valley Upper Index: {model.o[valley_upper_idx]}, {model.ei[valley_upper_idx]}")
    print(f"Rigth Limit: {model.o[int(len(model.o) * 0.45)]}, {model.ei[int(len(model.o) * 0.45)]}")

    # find_breaking_point(ax, o_max_idx, len(model.o)-70, 5, "Right")

    # Add title and labels
    ax.set_xlabel('Osmolality [mOsm/kg]')
    ax.set_ylabel('Elongation Index [EI]')
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()


def plot_poly_chart_middle(ax, lower_idx, upper_idx, degree: int):
    o_middle = model.o[lower_idx:upper_idx]
    ei_middle = model.ei[lower_idx:upper_idx]

    coefficients = np.polyfit(o_middle, ei_middle, degree)
    polynomial = np.poly1d(coefficients)

    o_fit = np.linspace(min(o_middle), max(o_middle), 500)

    exceeding_indices = np.nonzero(ei_middle > polynomial(o_middle))[0]

    # Find the index of the maximum exceeding value
    max_exceeding_index = exceeding_indices[np.argmax(
        ei_middle[exceeding_indices] - polynomial(
            o_middle[exceeding_indices]))]

    # Get the maximum exceeding value and its corresponding O and EI values
    max_exceeding_value = ei_middle[max_exceeding_index] - polynomial(
        o_middle[max_exceeding_index])

    # Step 5: Shift the polynomial to be above the exceeding points
    adjusted_polynomial = polynomial + max_exceeding_value

    # Generate the adjusted polynomial curve
    ei_adjusted_fit = adjusted_polynomial(o_fit)

    # Use an optimization method to find the maximum
    # Provide an initial guess within the range of O_middle
    initial_guess = np.mean(o_middle)
    result = minimize(lambda O: -adjusted_polynomial(O), initial_guess,
                      bounds=[(min(o_middle), max(o_middle))])

    # Get the highest point for the adjusted polynomial
    highest_o = result.x[0]
    highest_ei = adjusted_polynomial(highest_o)

    # Plot the original fitted polynomial
    # ax.plot(o_fit, ei_fit, "r--", label='Original Fitted Polynomial', linewidth=1)
    # Plot the adjusted polynomial
    ax.plot(o_fit, ei_adjusted_fit, 'r', label='Adjusted Polynomial',
            linewidth=0.75)

    # Plot max exceeding point
    # ax.plot(o_middle[max_exceeding_index], ei_middle[max_exceeding_index], "x",
    #         color="yellow", markersize=6)

    # Polynomial max point
    # ax.plot(highest_o, highest_ei, "o", color="g", markersize=4,
    #         label=f"Polynomial EI_max({round(highest_ei, 3)})")

    # ax.scatter(o_middle[exceeding_indices], ei_middle[exceeding_indices],
    #            color='purple', label='Exceeding Points', s=50)


def find_breaking_point(ax, start_index, end_index, degree: int, side: str):
    # Step 1: Select the portion of the data between valley_idx and o_max_idx
    o_segment = model.o[start_index:end_index]
    ei_segment = model.ei[start_index:end_index]

    # Step 2: Fit a polynomial to the selected segment
    coefficients = np.polyfit(o_segment, ei_segment, degree)
    polynomial = np.poly1d(coefficients)

    # Step 3: Generate a smooth range of O values for plotting and derivative calculations
    o_fit = np.linspace(min(o_segment), max(o_segment))
    ei_fit = polynomial(o_fit)

    # Step 4: Calculate the first and second derivatives of the polynomial
    first_derivative = np.polyder(polynomial)
    second_derivative = np.polyder(first_derivative)

    # Step 5: Calculate the derivative values across the range of O values
    second_derivative_values = second_derivative(o_fit)

    # Step 6: Find breaking points where the second derivative changes sign
    breaking_points_indices = \
    np.nonzero(np.diff(np.sign(second_derivative_values)))[0]
    breaking_points_o = o_fit[breaking_points_indices]
    breaking_points_ei = polynomial(breaking_points_o)

    # Plot the polynomial fit
    # ax.plot(o_fit, ei_fit, 'b--', label='Polynomial Fit')
    #
    # ax.plot(breaking_points_o, breaking_points_ei, "x", color="orange", label='Breaking Points')
    # Step 7: Find the highest breaking point
    if len(breaking_points_ei) > 0:  # Check if there are any breaking points
        highest_breaking_index = np.argmax(breaking_points_ei)

        # Get the O value of the highest breaking point
        highest_breaking_o = breaking_points_o[highest_breaking_index]

        # Find the closest O value in the original data
        original_index = np.abs(model.o[
                                start_index:end_index] - highest_breaking_o).argmin() + start_index

        # Display the highest breaking point as a red cross
        ax.plot(model.o[original_index], model.ei[original_index], "x",
                color='red', label=f'{side}: Breaking Point')

        print(
            f"{side}: breaking point ({model.o[original_index]}, {model.ei[original_index]})")

        return int(
            original_index)  # Return the index based on the original array
    else:
        print(f"No breaking points found for {side}.")
        return None  # No breaking points found


if __name__ == "__main__":
    main()
