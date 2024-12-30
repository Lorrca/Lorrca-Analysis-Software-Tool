import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
from matplotlib import pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
import numpy as np


# Function to create a new figure and replicate the contents of the original figure
def create_new_figure_from_existing(fig):
    """Create a new figure and copy the contents of the existing figure onto it."""
    new_fig, new_axs = plt.subplots(len(fig.axes), 1, sharex=True)

    # Handle case where there is only one subplot
    if len(fig.axes) == 1:
        new_axs = [new_axs]

    for i, ax in enumerate(fig.axes):
        new_handles, new_labels = [], []

        # Copy lines, scatter, areas, and other elements
        copy_lines(ax, new_axs[i], new_handles, new_labels)
        copy_scatter_and_areas(ax, new_axs[i], new_handles, new_labels)
        copy_bar_plots(ax, new_axs[i], new_handles, new_labels)
        copy_annotations(ax, new_axs[i])

        # Set axis properties
        set_axis_properties(ax, new_axs[i])

        # Copy the legend if it exists
        copy_legend(ax, new_axs[i], new_handles, new_labels)

    return new_fig


def copy_lines(ax, new_ax, new_handles, new_labels):
    """Copy lines from the original axes to the new axes."""
    for line in ax.lines:
        new_line = new_ax.plot(
            line.get_xdata(), line.get_ydata(),
            label=line.get_label(),
            color=line.get_color(),
            linestyle=line.get_linestyle(),
            linewidth=line.get_linewidth(),
            marker=line.get_marker(),
            markersize=line.get_markersize()
        )[0]
        new_handles.append(new_line)
        new_labels.append(line.get_label())


def copy_scatter_and_areas(ax, new_ax, new_handles, new_labels):
    """Copy scatter plots and area plots (fill_between) from the original axes."""
    for collection in ax.collections:
        if isinstance(collection, PolyCollection):
            copy_area(collection, new_ax, new_handles, new_labels)
        else:
            copy_scatter(collection, new_ax, new_handles, new_labels)


def copy_area(collection, new_ax, new_handles, new_labels):
    """Copy area plots (PolyCollection) to the new axis."""
    paths = collection.get_paths()
    for path in paths:
        x, y1, y2 = extract_area_data(path)
        label = collection.get_label() or "Area"
        new_ax.fill_between(x, y1, y2, color=collection.get_facecolor()[0],
                            alpha=collection.get_alpha(), label=label)

        # Create a Patch for the area plot for the legend
        patch = Patch(color=collection.get_facecolor()[0], alpha=collection.get_alpha(),
                      label=label)
        new_handles.append(patch)
        new_labels.append(label)


def extract_area_data(path):
    """Extract the data for area plots (x, y1, y2) from the path."""
    vertices = path.vertices
    x = vertices[:, 0]
    y1 = vertices[:, 1]
    y2 = np.zeros_like(y1)  # Default to zero for filled areas

    # Check if the path has a second set of vertices (upper/lower bounds)
    if len(vertices) > len(x):
        y2 = vertices[len(x):, 1]

    # Filter only valid finite data points
    valid_indices = np.isfinite(x) & np.isfinite(y1) & np.isfinite(y2)
    return x[valid_indices], y1[valid_indices], y2[valid_indices]


def copy_scatter(collection, new_ax, new_handles, new_labels):
    """Copy scatter plots to the new axis."""
    offsets = collection.get_offsets()
    sizes = collection.get_sizes() or [20]  # Default marker size if not set
    new_scatter = new_ax.scatter(
        offsets[:, 0], offsets[:, 1],
        label=collection.get_label(),
        color=collection.get_facecolor()[0],
        edgecolor=collection.get_edgecolor(),
        s=sizes,
        alpha=collection.get_alpha()
    )
    new_handles.append(new_scatter)
    new_labels.append(collection.get_label())


def copy_bar_plots(ax, new_ax, new_handles, new_labels):
    """Copy bar plots (patches) from the original axes."""
    for patch in ax.patches:
        new_patch = new_ax.add_patch(patch)
        new_handles.append(new_patch)
        new_labels.append(patch.get_label())


def copy_annotations(ax, new_ax):
    """Copy annotations (texts) from the original axes."""
    for text in ax.texts:
        new_ax.annotate(
            text.get_text(),
            xy=text.get_position(),
            xycoords=text.xycoords,
            fontsize=text.get_fontsize(),
            color=text.get_color()
        )


def set_axis_properties(ax, new_ax):
    """Set axis properties from the original axes to the new axes."""
    new_ax.set_xlabel(ax.get_xlabel())
    new_ax.set_ylabel(ax.get_ylabel())
    new_ax.set_title(ax.get_title())
    new_ax.set_xlim(ax.get_xlim())
    new_ax.set_ylim(ax.get_ylim())


def copy_legend(ax, new_ax, new_handles, new_labels):
    """Copy the legend if it exists from the original axes to the new axes."""
    legend = ax.get_legend()
    if legend is not None:
        new_ax.legend(
            handles=new_handles,
            labels=new_labels,  # Use the new_labels list to match handles
            loc='best'
        )

# Function to save a plot with optional customization
def save_plot_with_clone(fig, filename, width=None, height=None, dpi=None, x_label=None,
                         y_label=None, title=None):
    """Create a new figure from the original, apply changes to it, and save it as a PNG file."""
    cloned_fig = create_new_figure_from_existing(fig)  # Create a new independent figure

    # Apply optional customizations
    if width and height and dpi:
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
