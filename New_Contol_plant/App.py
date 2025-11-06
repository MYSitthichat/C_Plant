import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from Controller.main_controller import MainController

try:
    from qt_material import apply_stylesheet
except ImportError:
    print("\n[Error] not found qt-material")
    print("error please run: pip install qt-material\n")
    sys.exit()
    
# def fake_complete_load():
#     # Get current mixer
#     mixer = main_app.load_work_queue.get_current_mixer()
#     order_id = main_app.load_work_queue.get_current_order_id()
#     if not mixer or not order_id:
#         print("❌ No work in progress")
#         QMessageBox.warning(
#             main_app.main_window,
#             "ไม่มีงาน",
#             "ไม่มีงานที่กำลังดำเนินการอยู่"
#         )
#         return
#     # Simulate fake loaded weights (just for testing)
#     mixer.rock1_total_weight = mixer.rock1_weight  # Set to target weight
#     mixer.sand_total_weight = mixer.sand_weight
#     mixer.rock2_total_weight = mixer.rock2_weight
#     mixer.cement_total_weight = mixer.cement_weight
#     mixer.fly_ash_total_weight = mixer.fly_ash_weight
#     mixer.water_total_weight = mixer.water_weight
#     mixer.chem1_total_weight = mixer.chem1_weight
#     mixer.chem2_total_weight = mixer.chem2_weight
#     # Call complete_current_work to update database
#     result = main_app.load_work_queue.complete_current_work()
#     if result:
#         print(f"✅ Database updated! Status_load=1")
#         print(f"✅ Record ID: {result['record_id']}")
#     else:
#         print(f"❌ Failed to update database")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_red.xml')
    main_app = MainController()
    main_app.Show_main()
    app.exec()

    # app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='dark_red.xml')
    # main_app = MainController()
    # # Connect the fake load complete function to the button
    # main_app.main_window.mix_start_load_pushButton.clicked.connect(fake_complete_load)
    # main_app.Show_main()
    # app.exec()

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
    
    

