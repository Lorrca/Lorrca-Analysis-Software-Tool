import matplotlib.pyplot as plt
import numpy as np
from enum import Enum

from setup import load_data

from src.core.models.osmo_model import OsmoModel


class CurveType(Enum):
    BUMP = "bump"
    VALLEY = "valley"


data = load_data()

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

    filtered_o = model.o
    filtered_ei = model.ei

    # Plot original points
    ax.plot(filtered_o, filtered_ei, label='EI', linewidth=1)

    valley_upper_idx = find_breaking_point(ax, valley_idx, o_max_idx, 5,
                                           "Left")

    # Valley polynomial
    plot_polynomial(ax, peak_idx, valley_upper_idx, 2, CurveType.VALLEY)

    # Top part polynomial
    plot_polynomial(ax, valley_upper_idx, int(len(model.o) * 0.45), 4,
                    CurveType.BUMP)

    # Add title and labels
    ax.set_xlabel('Osmolality [mOsm/kg]')
    ax.set_ylabel('Elongation Index [EI]')
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.show()


def plot_polynomial(ax, lower_idx, upper_idx, degree: int,
                    curve_type: CurveType):
    """Main function to fit and plot the polynomial with manual adjustment type (bump or valley)."""
    relevant_o, relevant_ei = get_relevant_data(lower_idx, upper_idx + 1)
    polynomial = fit_polynomial(relevant_o, relevant_ei, degree)

    # Adjust polynomial based on the user-specified type: bump or valley
    adjusted_polynomial, o_fit, ei_adjusted_fit = adjust_polynomial(relevant_o,
                                                                    relevant_ei,
                                                                    polynomial,
                                                                    curve_type)

    # Plot the results
    plot_adjusted_polynomial(ax, o_fit, ei_adjusted_fit, degree)

    return adjusted_polynomial, o_fit, ei_adjusted_fit


def get_relevant_data(lower_idx, upper_idx):
    """Get the relevant 'o' and 'ei' data within the specified index range."""
    relevant_o = model.o[lower_idx:upper_idx]
    relevant_ei = model.ei[lower_idx:upper_idx]
    return relevant_o, relevant_ei


def fit_polynomial(relevant_o, relevant_ei, degree):
    """Fit a polynomial of the given degree to the relevant data."""
    coefficients = np.polyfit(relevant_o, relevant_ei, degree)
    return np.poly1d(coefficients)


def adjust_polynomial(relevant_o, relevant_ei, polynomial,
                      curve_type: CurveType):
    """Adjust the polynomial based on the user-defined adjustment type: bump or valley."""
    o_fit = np.linspace(min(relevant_o), max(relevant_o), 500)

    if curve_type == CurveType.BUMP:
        return adjust_for_bump(relevant_o, relevant_ei, polynomial, o_fit)
    elif curve_type == CurveType.VALLEY:
        return adjust_for_valley(relevant_o, relevant_ei, polynomial, o_fit)
    else:
        raise ValueError("Invalid adjust_type. Use 'bump' or 'valley'.")


def adjust_for_bump(relevant_o, relevant_ei, polynomial, o_fit):
    """Adjust the polynomial to fit the highest exceeding point (bump)."""
    exceeding_indices = np.nonzero(relevant_ei > polynomial(relevant_o))[0]
    max_exceeding_index = exceeding_indices[np.argmax(
        relevant_ei[exceeding_indices] - polynomial(
            relevant_o[exceeding_indices]))]
    max_exceeding_value = relevant_ei[max_exceeding_index] - polynomial(
        relevant_o[max_exceeding_index])

    adjusted_polynomial = polynomial + max_exceeding_value
    ei_adjusted_fit = adjusted_polynomial(o_fit)

    return adjusted_polynomial, o_fit, ei_adjusted_fit


def adjust_for_valley(relevant_o, relevant_ei, polynomial, o_fit):
    """Adjust the polynomial to fit the lowest exceeding point (valley)."""
    exceeding_indices = np.nonzero(relevant_ei < polynomial(relevant_o))[0]
    min_exceeding_index = exceeding_indices[np.argmin(
        relevant_ei[exceeding_indices] - polynomial(
            relevant_o[exceeding_indices]))]
    min_exceeding_value = relevant_ei[min_exceeding_index] - polynomial(
        relevant_o[min_exceeding_index])

    adjusted_polynomial = polynomial + min_exceeding_value
    ei_adjusted_fit = adjusted_polynomial(o_fit)

    return adjusted_polynomial, o_fit, ei_adjusted_fit


def plot_adjusted_polynomial(ax, o_fit, ei_adjusted_fit, degree):
    """Plot the adjusted polynomial curve."""
    ax.plot(o_fit, ei_adjusted_fit, label=f"Degree {degree} Fit")


def find_breaking_point(ax, start_index, end_index, degree: int, side: str):
    # Step 1: Select the portion of the data between valley_idx and o_max_idx
    o_segment = model.o[start_index:end_index]
    ei_segment = model.ei[start_index:end_index]

    # Step 2: Fit a polynomial to the selected segment
    coefficients = np.polyfit(o_segment, ei_segment, degree)
    polynomial = np.poly1d(coefficients)

    # Step 3: Generate a smooth range of O values for plotting and derivative calculations
    o_fit = np.linspace(min(o_segment), max(o_segment))

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
                color='red',
                label=f'{side}: Breaking Point ({model.o[original_index]}, {model.ei[original_index]})')

        return original_index  # Return the index based on the original array
    else:
        print(f"No breaking points found for {side}.")

    return None  # No breaking points found


if __name__ == "__main__":
    main()
