import sys
import os
from PySide6.QtWidgets import QApplication


project_root = os.path.dirname(os.path.abspath(__file__))
new_report_path = os.path.join(project_root, "New_report")
sys.path.append(new_report_path)

from Controller.main_controller import MainController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainController()
    main_app.Show_main()
    app.exec()