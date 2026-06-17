from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

class offset_tab(QObject):
    def __init__(self, main_window, db):
        super(offset_tab, self).__init__()
        self.main_window = main_window
        self.db = db

        self._connect_signals()
        self.load_offset_settings()
        self.set_offset_form_read_only(True)
        self.main_window.offset_save_pushButton.setEnabled(False)
        self.main_window.offset_edite_pushButton.setEnabled(True)
        self.main_window.offset_cancel_pushButton.setEnabled(False)

    def _connect_signals(self):
        self.main_window.offset_save_pushButton.clicked.connect(self.offset_save)
        self.main_window.offset_edite_pushButton.clicked.connect(self.offset_edite)
        self.main_window.offset_cancel_pushButton.clicked.connect(self.offset_cancel)

    def set_offset_form_read_only(self, is_read_only):
        """ตั้งค่าช่องกรอกข้อมูล Offset ทั้งหมดเป็น ReadOnly หรือ Editable"""
        self.main_window.offset_rock_1_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_sand_1_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_rock_2_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_sand_2_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_cement_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_fyash_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_water_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_chem_1_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_chem_2_lineEdit.setReadOnly(is_read_only)

        self.main_window.offset_converyer_silo_time_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_opan_cement_time_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_run_mixer_time_lineEdit.setReadOnly(is_read_only)
        self.main_window.offset_time_next_load_lineEdit.setReadOnly(is_read_only)

    def load_offset_settings(self):
        """โหลดค่าจาก DB มาแสดงในหน้า Offset"""
        data = self.db.read_offset_settings()
        if data:

            self.main_window.offset_rock_1_lineEdit.setText(str(data[1]))
            self.main_window.offset_sand_1_lineEdit.setText(str(data[2]))
            self.main_window.offset_rock_2_lineEdit.setText(str(data[3]))
            self.main_window.offset_sand_2_lineEdit.setText(str(data[4]))
            self.main_window.offset_cement_lineEdit.setText(str(data[5]))
            self.main_window.offset_fyash_lineEdit.setText(str(data[6]))
            self.main_window.offset_water_lineEdit.setText(str(data[7]))
            self.main_window.offset_chem_1_lineEdit.setText(str(data[8]))
            self.main_window.offset_chem_2_lineEdit.setText(str(data[9]))

            self.main_window.offset_converyer_silo_time_lineEdit.setText(str(data[10]))
            self.main_window.offset_opan_cement_time_lineEdit.setText(str(data[11]))
            self.main_window.offset_run_mixer_time_lineEdit.setText(str(data[12]))
            self.main_window.offset_time_next_load_lineEdit.setText(str(data[13]))

    def offset_save(self):
        print("offset save")
        try:

            rock1 = float(self.main_window.offset_rock_1_lineEdit.text())
            sand1 = float(self.main_window.offset_sand_1_lineEdit.text())
            rock2 = float(self.main_window.offset_rock_2_lineEdit.text())
            sand2 = float(self.main_window.offset_sand_2_lineEdit.text())
            cement = float(self.main_window.offset_cement_lineEdit.text())
            fyash = float(self.main_window.offset_fyash_lineEdit.text())
            water = float(self.main_window.offset_water_lineEdit.text())
            chem1 = float(self.main_window.offset_chem_1_lineEdit.text())
            chem2 = float(self.main_window.offset_chem_2_lineEdit.text())

            conv_time = float(self.main_window.offset_converyer_silo_time_lineEdit.text())
            cement_time = float(self.main_window.offset_opan_cement_time_lineEdit.text())
            mixer_time = float(self.main_window.offset_run_mixer_time_lineEdit.text())
            next_time = float(self.main_window.offset_time_next_load_lineEdit.text())


            self.db.update_offset_settings(
                rock1, sand1, rock2, sand2, cement, fyash, water,
                chem1, chem2, conv_time, cement_time, mixer_time, next_time
            )

            self.set_offset_form_read_only(True)
            self.main_window.offset_save_pushButton.setEnabled(False)
            self.main_window.offset_edite_pushButton.setEnabled(True)
            self.main_window.offset_cancel_pushButton.setEnabled(False)

            QMessageBox.information(self.main_window, "บันทึกสำเร็จ", "บันทึกค่า Offset เรียบร้อยแล้ว")

        except ValueError:
            QMessageBox.warning(self.main_window, "ข้อมูลผิดพลาด", "กรุณากรอกข้อมูลเป็นตัวเลขให้ถูกต้อง")
        except Exception as e:
            QMessageBox.warning(self.main_window, "ผิดพลาด", f"เกิดข้อผิดพลาด: {e}")

    def offset_edite(self):
        print("offset edite")

        self.set_offset_form_read_only(False)
        self.main_window.offset_save_pushButton.setEnabled(True)
        self.main_window.offset_edite_pushButton.setEnabled(False)
        self.main_window.offset_cancel_pushButton.setEnabled(True)

    def offset_cancel(self):
        print("offset cancel")
        self.load_offset_settings()

        self.set_offset_form_read_only(True)
        self.main_window.offset_save_pushButton.setEnabled(False)
        self.main_window.offset_edite_pushButton.setEnabled(True)
        self.main_window.offset_cancel_pushButton.setEnabled(False)

