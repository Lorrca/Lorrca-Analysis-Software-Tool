import matplotlib.pyplot as plt

class OsmoVisualizer:
    def __init__(self, results, data, osmo_metadata):
        self.results = results
        self.data = data
        self.metadata = osmo_metadata

    def visualize_raw(self):
        _, ax = plt.subplots()

        # Plot Osmolality / Elongation raw curve
        ax.plot(self.data['O.'], self.data['EI'],
                label='Raw Osmolality vs. Elongation', linewidth=0.75)

        # Plot EI / O. first peak
        o_first_peak = self.results.get('first_peak')[0] if self.results.get('first_peak') else None
        ei_first_peak = self.results.get('first_peak')[1] if self.results.get('first_peak') else None
        if o_first_peak is not None and ei_first_peak is not None:
            ax.plot(o_first_peak, ei_first_peak, 'o', label=f'First peak ({o_first_peak}, {ei_first_peak})',
                    markersize=3)

        # Plot EI / O. min
        o_min = self.results.get('valley')[0] if self.results.get('valley') else None
        ei_min = self.results.get('valley')[1] if self.results.get('valley') else None
        if o_min is not None and ei_min is not None:
            ax.plot(o_min, ei_min, 'o', label=f'EI min ({o_min}, {ei_min})',
                    markersize=3)

        # Plot EI / O. max
        o_max = self.results.get('o_max')
        ei_max = self.results.get('ei_max')
        if o_max is not None and ei_max is not None:
            ax.plot(o_max, ei_max, 'o', label=f'EI max ({o_max}, {ei_max})', markersize=3)

        # Plot EI / O. hyper
        o_hyper = self.results.get('o_hyper')
        ei_hyper = self.results.get('ei_hyper')
        if o_hyper is not None and ei_hyper is not None:
            ax.plot(o_hyper, ei_hyper, 'o', label=f'EI hyper ({o_hyper}, {ei_hyper})', markersize=3)

        # Set labels and title
        ax.set_xlabel("Osmolality (O.)")  # X-axis label
        ax.set_ylabel("Elongation Index (EI)")  # Y-axis label
        ax.set_title(f"{self.metadata.get('measurement_id')}")
        ax.legend()
        ax.grid(True)  # Add grid for better readability

        plt.tight_layout()  # Adjust layout for better fit
        plt.show()  # Display the plot
