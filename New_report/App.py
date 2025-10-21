import sys
import os
from PySide6.QtWidgets import QApplication

# --- ADD THIS ---
# Get the main project directory (where App.py is)
project_root = os.path.dirname(os.path.abspath(__file__))
# Add the 'New_report' folder to the Python path
new_report_path = os.path.join(project_root, "New_report")
sys.path.append(new_report_path)
# --- END ADD ---

# This import will now work
from Controller.main_controller import MainController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainController()
    main_app.Show_main()
    app.exec()