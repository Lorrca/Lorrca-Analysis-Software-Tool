import matplotlib.pyplot as plt

from src.core.models.osmo_model import OsmoModel


class OsmoVisualizer:
    def __init__(self, model: OsmoModel):
        self.id = model.id
        self.info = model.info
        self.model = model

    def visualize_raw(self):
        _, ax = plt.subplots()

        # Plot Osmolality / Elongation raw curve
        ax.plot(self.model.o, self.model.ei,
                label='Raw Osmolality vs. Elongation', linewidth=0.75)

        # Plot EI / O. first peak
        ax.plot(self.model.o_first_peak, self.model.ei_first_peak, 'o',
                label=f'First peak ({self.model.o_first_peak}, {self.model.ei_first_peak})',
                markersize=3)

        # Plot EI / O. min

        o_min = self.model.min[0]
        ei_min = self.model.min[1]
        ax.plot(o_min, ei_min, 'o',
                label=f'EI min ({round(o_min)}, {round(ei_min, 3)})',
                markersize=3)

        # Plot EI / O. max
        ax.plot(self.model.o_max, self.model.ei_max, 'o',
                label=f'EI max ({round(self.model.o_max)}, {self.model.ei_max})',
                markersize=3)

        # Plot EI / O. hyper
        ax.plot(self.model.o_hyper, self.model.ei_hyper, 'o',
                label=f'EI hyper ({round(self.model.o_hyper)}, {round(self.model.ei_hyper, 3)})',
                markersize=3)

        # Fill the area under the curve
        area, o_segment, ei_segment = self.model.area
        plt.fill_between(o_segment, ei_segment, color='goldenrod',
                         alpha=0.2, hatch='//', edgecolor='black',
                         label=f'Area = {round(area)}')

        # Set labels and title
        ax.set_xlabel("Osmolality (O.)")  # X-axis label
        ax.set_ylabel("Elongation Index (EI)")  # Y-axis label
        ax.set_title(f"{self.info}, {self.id}")
        ax.legend()
        ax.grid(True)  # Add grid for better readability

        plt.tight_layout()  # Adjust layout for better fit
        plt.show()
