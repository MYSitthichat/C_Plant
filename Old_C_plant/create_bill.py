from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem
from PySide6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog
from PySide6.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide6.QtGui import QPainter, QPageSize
from PySide6.QtPdf import QPdfDocument, QPdfPageRenderer
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QDialog
from PySide6.QtGui import QPainter,QPageSize
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtPdf import QPdfDocument

from bill_form import Ui_MainWindow
import sqlite3

from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.fonts import addMapping

# Add Thai font
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import time
import os
import sys
import subprocess

# Register a Thai font


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        
        self.font_path = os.path.join(os.path.dirname(__file__), "fonts", "THNiramitAS.ttf")
        self.template_path = os.path.join(os.path.dirname(__file__), "other_files","bill_templateA5.pdf")
        self.ouput_pdf_path = os.path.join(os.path.dirname(__file__), "billoutput.pdf")
        
        self.pdf_document = QPdfDocument()
                
        self.db_path = os.path.join(os.path.dirname(__file__),"database","main_db.db")
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.treeWidget.setColumnWidth(0, 100)
        self.treeWidget.setColumnWidth(1, 200)
        self.treeWidget.setColumnWidth(2, 300)
        self.treeWidget.setColumnWidth(3, 100)
        # Connect the buttons to their respective functions
        self.printPushButton.clicked.connect(self.print_button_clicked)
        self.reloadPushButton.clicked.connect(self.reload_button_clicked)
        
        # hide the radio buttons
        self.leanRadioButton.hide()
        self.defaultRadioButton.hide()
        
        self.reload_button_clicked()
        self.defaultRadioButton.setChecked(True)
        
        
    def preload_data(self):
        # load data from the sqlite database
        conn = sqlite3.connect(self.db_path)
        # read last tens records from recording table
        cursor = conn.cursor()
        cursor.execute("SELECT Booking_ID, Record_Time, Customer_Name, Amount FROM recording_table ORDER BY Booking_ID DESC LIMIT 40")
        records = cursor.fetchall()
        conn.close()
        return records
        
        # Create a function to draw the name on a canvas
    def create_canvas(self,customer_informtaion):
        # current_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        # Extract the customer information
        [record_time, customer_name, address, amount, comment, strength, ] = customer_informtaion
        
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=landscape(A5))
        pdfmetrics.registerFont(TTFont('THSarabunNew', self.font_path))
        addMapping('THSarabunNew', 0, 0, 'THSarabunNew')
        
        c.setFont("THSarabunNew", 12)
        c.drawString(120, 312, customer_name)
        c.drawString(120, 296, address)
        c.drawString(120, 280, address)
        c.drawString(120, 216, amount)
        # get only the data part of the record time
        record_date = record_time.split(" ")[0]
        
        # convert date to Thai date
        # previous format is yyyy-mm-dd
        # new format is dd-mm-yyyy in Thai
        record_date = record_date.split("-")
        month = ""
        if record_date[1] == "01":
            month = "ม.ค."
        elif record_date[1] == "02":
            month = "ก.พ."
        elif record_date[1] == "03":
            month = "มี.ค."
        elif record_date[1] == "04":
            month = "เม.ย."
        elif record_date[1] == "05":
            month = "พ.ค."
        elif record_date[1] == "06":
            month = "มิ.ย."
        elif record_date[1] == "07":
            month = "ก.ค."
        elif record_date[1] == "08":
            month = "ส.ค."
        elif record_date[1] == "09":
            month = "ก.ย."
        elif record_date[1] == "10":
            month = "ต.ค."
        elif record_date[1] == "11":
            month = "พ.ย."
        elif record_date[1] == "12":
            month = "ธ.ค."
        
        record_date = str(int(record_date[2])) + " " + month + " " + str(int(record_date[0])+543)
        c.drawString(120, 199, record_date)
        record_timestamp = record_time.split(" ")[1]
        c.drawString(280, 199, record_timestamp)
        c.drawString(120, 183, comment)
        
        if strength == "Lean":
            c.drawString(218, 266, "Lean")
            c.drawString(425, 264, " - ")   # age
            c.drawString(125, 235, " - ")   # slump
        else:
            c.drawString(220, 264, strength)
            c.drawString(425, 264, " 28 ")   # age 
            c.drawString(116, 235, "7.5+-2.5")   # slump 7.5 +- 2.5
        c.save()
        packet.seek(0)
        return packet

    def generate_pdf_output(self,customer_informtaion):
        # Create a PdfWriter object to write the output PDF
        output = PdfWriter()

        # Read the existing template PDF
        template_pdf = PdfReader(self.template_path)

        # Iterate through the pages of the template PDF
        for i in range(len(template_pdf.pages)):
            template_page = template_pdf.pages[i]

            # Create a new canvas with the name for the current page
            packet = self.create_canvas(customer_informtaion)
            new_pdf = PdfReader(packet)
            new_page = new_pdf.pages[0]

            # Merge the new content with the template page
            template_page.merge_page(new_page)
            output.add_page(template_page)

        # Write the output PDF to a file
        with open(self.ouput_pdf_path, "wb") as output_stream:
            output.write(output_stream)
        # close the packet
        packet.close()
        

    def print_button_clicked(self):
        # if item in treewidget selected print the item
        # if no item selected show message box
        if self.treeWidget.currentItem() is None:
            QMessageBox.information(self, "Information", "Please select an item to print")
        else:
            item = self.treeWidget.currentItem()
            # get booking id
            booking_id = item.text(0)
            record_time = item.text(1)            
            # load data from the sqlite database
            bill_info = self.load_bill_info(booking_id)
            customer_name = bill_info[0]
            address = bill_info[1]
            amount = str(bill_info[2])
            comment = str(bill_info[3])
            
            strength = ""
            concrete_strength = self.load_concrete_strength(booking_id)[0][0]
            # get ending key of the concrete strength
            ending_key = concrete_strength.find("ksc")
            # if ending key is not found the return is -1
            if ending_key == -1:
                ending_key = concrete_strength.find("Lean")
                if ending_key == 0:     # the record is lean concrete
                    strength = "Lean"
                else:
                    strength = concrete_strength
            else:
                strength = concrete_strength[:ending_key]
                
            # print("Strength: ", strength)
            
            customer_informtaion = [record_time, customer_name, address, amount, comment, strength]
            self.generate_pdf_output(customer_informtaion)
            
            # print command
            print_command = []
            print_command.append('lp')
            print_command.append('-d')
            print_command.append('DCPT220')
            print_command.append(str(self.ouput_pdf_path))
            
            subprocess.run(print_command,check=True)
            
            
    def load_bill_info(self, booking_id):
        # load data from the sqlite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Customer_Name, Address, Amount, Comment FROM booking_table WHERE Booking_ID = ? LIMIT 1", (booking_id,))
        record = cursor.fetchone()
        conn.close()
        return record
            
    def reload_button_clicked(self):
        preloaded_data = self.preload_data()
        # clear the treeview
        self.treeWidget.clear()
        # add preload data to treeview
        for row in preloaded_data:
            item = QTreeWidgetItem(list(map(str,row)))
            self.treeWidget.addTopLevelItem(item)

    def load_concrete_strength(self, booking_id):
        # load data from the sqlite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT Description FROM recording_table where Booking_ID = ? LIMIT 1", (booking_id,))
        records = cursor.fetchall()
        conn.close()
        return records

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
