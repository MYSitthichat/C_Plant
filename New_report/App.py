import sys
import os
from PySide6.QtWidgets import QApplication


project_root = os.path.dirname(os.path.abspath(__file__))
new_report_path = os.path.join(project_root, "New_report")
sys.path.append(new_report_path)

from Controller.main_controller import MainController
try:
    from qt_material import apply_stylesheet
except ImportError:
    print("\n[Error] not found qt-material")
    print("error please run: pip install qt-material\n")
    sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_red.xml')
    main_app = MainController()
    main_app.Show_main()
    app.exec()