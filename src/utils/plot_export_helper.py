from matplotlib import pyplot as plt


# Function to create a new figure and replicate the contents of the original figure
def create_new_figure_from_existing(fig):
    """Create a new figure and copy the contents of the existing figure onto it."""
    new_fig, new_axs = plt.subplots(len(fig.axes), 1, sharex=True)

    # Handle case where there is only one subplot
    if len(fig.axes) == 1:
        new_axs = [new_axs]

    for i, ax in enumerate(fig.axes):
        # Copy the content (lines, labels, etc.) from the original axes to the new one
        new_handles = []  # List to hold new handles for the legend
        for line in ax.lines:
            # Create a new line in the new axis
            # Get the Line2D instance
            new_line = new_axs[i].plot(line.get_xdata(), line.get_ydata(), label=line.get_label(),
                                       color=line.get_color(), linestyle=line.get_linestyle(),
                                       linewidth=line.get_linewidth(), marker=line.get_marker(),
                                       markersize=line.get_markersize())[0]
            new_handles.append(new_line)

        new_axs[i].set_xlabel(ax.get_xlabel())
        new_axs[i].set_ylabel(ax.get_ylabel())
        new_axs[i].set_title(ax.get_title())

        # Copy the legend if it exists
        legend = ax.get_legend()
        if legend is not None:
            # Create a new legend in the new axis with the new handles
            new_axs[i].legend(handles=new_handles, labels=[line.get_label() for line in ax.lines],
                              loc='best')

    return new_fig


# Function to save a plot with optional customization
def save_plot_with_clone(fig, filename, width=None, height=None, dpi=None, x_label=None,
                         y_label=None, title=None):
    """Create a new figure from the original, apply changes to it, and save it as a PNG file."""
    cloned_fig = create_new_figure_from_existing(fig)  # Create a new independent figure

    # Apply optional customizations
    if width and height:
        cloned_fig.set_size_inches(width / dpi, height / dpi)
    if x_label or y_label or title:
        for ax in cloned_fig.axes:
            if x_label:
                ax.set_xlabel(x_label)
            if y_label:
                ax.set_ylabel(y_label)
            if title:
                ax.set_title(title)

    # Save the cloned figure as an image
    cloned_fig.savefig(filename, format='png', dpi=dpi)
    plt.close(cloned_fig)  # Close the cloned figure to free memory
