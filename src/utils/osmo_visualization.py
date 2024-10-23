import matplotlib.pyplot as plt

from src.core.models.osmo_model import OsmoModel


class OsmoVisualizer:
    def __init__(self, model: OsmoModel):
        self.id = model.id

        self.o = model.o
        self.ei = model.ei
        self.ei_max = model.ei_max
        self.o_max = model.o_max
        self.ei_hyper = model.ei_hyper
        self.o_hyper = model.o_hyper
        self.o_min, self.ei_min = model.min
        self.o_first_peak, self.ei_first_peak = model.first_peak
        self.area, self.o_segment, self.ei_segment = model.area

    def visualize_raw(self):
        _, ax = plt.subplots()

        # Plot Osmolality / Elongation raw curve
        ax.plot(self.o, self.ei,
                label='Raw Osmolality vs. Elongation', linewidth=0.75)

        # Plot EI / O. first peak

        ax.plot(self.o_first_peak, self.ei_first_peak, 'o',
                label=f'First peak ({self.o_first_peak}, {self.ei_first_peak})',
                markersize=3)

        # Plot EI / O. min
        ax.plot(self.o_min, self.ei_min, 'o',
                label=f'EI min ({round(self.o_min)}, {round(self.ei_min, 3)})',
                markersize=3)

        # Plot EI / O. max
        ax.plot(self.o_max, self.ei_max, 'o',
                label=f'EI max ({round(self.o_max)}, {self.ei_max})',
                markersize=3)

        # Plot EI / O. hyper
        ax.plot(self.o_hyper, self.ei_hyper, 'o',
                label=f'EI hyper ({round(self.o_hyper)}, {round(self.ei_hyper, 3)})',
                markersize=3)

        # Fill the area under the curve
        plt.fill_between(self.o_segment, self.ei_segment, color='goldenrod',
                         alpha=0.2, hatch='//', edgecolor='black',
                         label=f'Area = {round(self.area)}')

        # Set labels and title
        ax.set_xlabel("Osmolality (O.)")  # X-axis label
        ax.set_ylabel("Elongation Index (EI)")  # Y-axis label
        ax.set_title(f"{self.id}")
        ax.legend()
        ax.grid(True)  # Add grid for better readability

        plt.tight_layout()  # Adjust layout for better fit
        plt.show()
