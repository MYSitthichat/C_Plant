import os
import tkinter as tk
from tkinter import  DISABLED, StringVar, font
from share_library import center_screen, default_window_size,read_concrete_formula_from_db,record_booking_data,read_booking_queue,remove_booking_queue,process_booking_queue
from share_library import get_processing_queue,relife_booking_queue,fail_booking_queue,read_concrete_formula
from share_library import complete_booking_queue,save_complete_queue
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from os.path import exists

from PyPDF2 import PdfFileReader,PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
present_time = datetime.now()
current_date_string = present_time.strftime('%d %B %Y')
current_time_string = present_time.strftime("%H:%M:%S")
date_string = present_time.strftime('%d%B%Y')

software_path = os.path.dirname(os.path.realpath(__file__))

bill_path1 = os.path.join(software_path,"bills")
bill_path2 = os.path.join(bill_path1 ,date_string)

output_temp_file1 = os.path.join(bill_path1 ,"customer_bill_temp.pdf")
output_temp_file2 = os.path.join(bill_path1 ,"owner_bill.pdf")
output_file_name = "customer" + str(456) + ".pdf"
output_path = os.path.join(bill_path2,output_file_name)

output_temp_file = os.path.join(bill_path1 ,"temp_bill.pdf")


dir_path = os.path.dirname(os.path.realpath(__file__))
font_path = dir_path + r'/fonts/THNiramitAS.ttf'
input_path = dir_path + r'/other_files/customer_bill.pdf'


# create information file
ctempfile = canvas.Canvas(output_temp_file1)
pdfmetrics.registerFont(TTFont('THNiramit', "/home/plant/Documents/CemenPlant/fonts/THNiramitAS.ttf"))
ctempfile.setFont("THNiramit",12)
ctempfile.saveState()

cemen_amount_string = "1.0"

ctempfile.drawString(155, 664, "ลุงน้อย")                           # customer name
ctempfile.drawString(155, 649, "1433")                                 # customer address
ctempfile.drawString(245, 618, "1123 ksc")                # cemen formula
ctempfile.drawString(155,570,cemen_amount_string)                              # concrete amount
ctempfile.drawString(160,553,current_date_string)                              # add date
ctempfile.drawString(320,553,current_time_string)                              # add time
ctempfile.drawString(160,537,"กบ 356")                                # name plate
ctempfile.restoreState()
ctempfile.save()

# merge files
output = PdfFileWriter()
input1 = PdfFileReader(input_path,'rb')
watermark = PdfFileReader(output_temp_file1,'rb')
for p in range(input1.getNumPages()):
    page = input1.getPage(p)
    page.mergePage(watermark.getPage(0))
    output.addPage(page)
outputStream = open(output_path,'wb')
output.write(outputStream)
outputStream.close()