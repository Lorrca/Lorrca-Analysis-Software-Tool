from typing import Optional

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget


class MainWindow(QMainWindow):
	def __init__(self, presenter):
		super().__init__()
		self.selected_folders_label = None
		self.select_hc_data_button = None
		self.select_data_button = None
		self.select_results_button = None
		self.presenter = presenter
		self.init_ui()

		# Initialize folder paths with None
		self.selected_folders: dict[str, Optional[str]] = {
			"data": None,
			"HCdata": None,
			"results": None
		}

	def init_ui(self):
		self.setWindowTitle("Folder Selection Example")
		layout = QVBoxLayout()
	
		# Buttons to select folders independently
		self.select_data_button = QPushButton("Select Data Folder", self)
		self.select_data_button.clicked.connect(self.presenter.on_select_data_folder)
		layout.addWidget(self.select_data_button)
	
		self.select_hc_data_button = QPushButton("Select HCData Folder", self)
		self.select_hc_data_button.clicked.connect(self.presenter.on_select_hc_data_folder)
		layout.addWidget(self.select_hc_data_button)
	
		self.select_results_button = QPushButton("Select Results Folder", self)
		self.select_results_button.clicked.connect(self.presenter.on_select_results_folder)
		layout.addWidget(self.select_results_button)
	
		# Label to display selected folders
		self.selected_folders_label = QLabel("Selected Folders: None", self)
		layout.addWidget(self.selected_folders_label)
	
		# Central widget setup
		container = QWidget()
		container.setLayout(layout)
		self.setCentralWidget(container)

	# Methods to update the UI from the presenter
	def set_data_folder(self, folder: str):
		self.selected_folders["data"] = folder
		self.update_ui_with_selected_folders()
	
	def set_hc_data_folder(self, folder: str):
		self.selected_folders["HCdata"] = folder
		self.update_ui_with_selected_folders()
	
	def set_results_folder(self, folder: str):
		self.selected_folders["results"] = folder
		self.update_ui_with_selected_folders()
	
	def update_ui_with_selected_folders(self):
		folders_text = "\n".join([f"{key}: {path}" for key, path in self.selected_folders.items() if path])
		self.selected_folders_label.setText(f"Selected Folders:\n{folders_text}" if folders_text else "No folders selected")
	
	def display_error(self, error_message: str):
		self.selected_folders_label.setText(f"Error: {error_message}")
