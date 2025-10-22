import sys
from PySide6.QtWidgets import QApplication
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

# Available themes
# Light Themes:
    # 'light_blue.xml'
    # 'light_blue_500.xml'
    # 'light_cyan.xml'
    # 'light_orange.xml'
    # 'light_pink.xml'
    # 'light_purple.xml'
    # 'light_red.xml'
    # 'light_teal.xml'
    # 'light_yellow.xml'

# Dark Themes:
    # 'dark_blue.xml'
    # 'dark_cyan.xml'
    # 'dark_pink.xml'
    # 'dark_purple.xml'
    # 'dark_red.xml'
    # 'dark_teal.xml'
    # 'dark_yellow.xml'