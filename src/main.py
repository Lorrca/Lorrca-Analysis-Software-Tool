from src.core.controllers.osmo_controller import OsmoController
from src.utils.osmo_data_loader import OsmoDataLoader


def main():
    # Initialize DataLoader and OsmoController
    data_loader = OsmoDataLoader(
        r"C:\Users\andrii.kernytskyi\Downloads\Archive 2\data_dir\OSMO1-AGIOS-002-SS-Day56_2023-09-19_0.CSV")
    controller = OsmoController(data_loader)

    # Load data
    controller.load_data()

    # Visualize results
    controller.visualize_results()


if __name__ == "__main__":
    main()
