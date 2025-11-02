import os
import subprocess
from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from Controller.load_data import load_data

from PyPDF2 import PdfReader, PdfWriter


class CreateBillConfig:
    def __init__(self):
        # Template path - in templates folder
        self.template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "bill_templateA5.pdf")
        self.template_path = os.path.normpath(self.template_path)
        
        # Font path - in fonts folder
        self.font_path = os.path.join(os.path.dirname(__file__), "..", "fonts", "THNiramitAS.ttf")
        self.font_path = os.path.normpath(self.font_path)
        
        # Bills directory - organized by date
        self.bills_dir = os.path.join(os.path.dirname(__file__), "..", "bills")
        self.bills_dir = os.path.normpath(self.bills_dir)
        
        # Create bills directory if it doesn't exist
        os.makedirs(self.bills_dir, exist_ok=True)
    
    def get_bill_save_path(self, id, date_string=None):
        """Get the full path to save the bill PDF"""
        if date_string is None:
            date_string = datetime.now().strftime("%Y-%m-%d")
        
        # Convert date to folder name format: "01January2024"
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        folder_name = date_obj.strftime("%d%B%Y")
        
        # Create date folder if it doesn't exist
        date_folder = os.path.join(self.bills_dir, folder_name)
        os.makedirs(date_folder, exist_ok=True)
        
        # Bill filename: {id}.pdf
        bill_filename = f"{id}.pdf"
        
        return os.path.join(date_folder, bill_filename)


class BillGenerator:
    def __init__(self):
        self.config = CreateBillConfig()
        self.data_loader = load_data()
        
    def convert_to_thai_date(self, date_string):
        """Convert date from yyyy-mm-dd to Thai format"""
        month_thai = {
            "01": "ม.ค.", "02": "ก.พ.", "03": "มี.ค.", "04": "เม.ย.",
            "05": "พ.ค.", "06": "มิ.ย.", "07": "ก.ค.", "08": "ส.ค.",
            "09": "ก.ย.", "10": "ต.ค.", "11": "พ.ย.", "12": "ธ.ค."
        }
        
        parts = date_string.split("-")
        day = str(int(parts[2]))
        month = month_thai.get(parts[1], parts[1])
        year = str(int(parts[0]) + 543)  # Convert to Buddhist year
        
        return f"{day} {month} {year}"
    
    def create_canvas(self, customer_information):
        """Create PDF canvas with customer information overlay"""
        [record_time, name, address, amount, strength, age, slump] = customer_information
        
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=landscape(A5))
        
        # Register Thai font
        pdfmetrics.registerFont(TTFont('THSarabunNew', self.config.font_path))
        addMapping('THSarabunNew', 0, 0, 'THSarabunNew')
        
        c.setFont("THSarabunNew", 12)
        
        # Draw customer information
        c.drawString(120, 312, name)
        c.drawString(120, 296, address)
        c.drawString(120, 216, str(amount))
        
        # Parse and format date
        record_date = record_time.split(" ")[0]
        thai_date = self.convert_to_thai_date(record_date)
        c.drawString(120, 199, thai_date)
        
        # Add time
        record_timestamp = record_time.split(" ")[1] if " " in record_time else ""
        c.drawString(280, 199, record_timestamp)
        
        # Add strength, age, and slump information from database
        c.drawString(220, 264, str(strength))
        c.drawString(425, 264, str(age))
        c.drawString(116, 235, str(slump))
        
        c.save()
        packet.seek(0)
        return packet
    
    def generate_pdf_output(self, customer_information, id, date_string=None):
        """Generate final PDF by merging template with overlay"""
        output = PdfWriter()
        
        # Read the template PDF
        template_pdf = PdfReader(self.config.template_path)
        
        # Iterate through template pages
        for i in range(len(template_pdf.pages)):
            template_page = template_pdf.pages[i]
            
            # Create overlay canvas
            packet = self.create_canvas(customer_information)
            new_pdf = PdfReader(packet)
            new_page = new_pdf.pages[0]
            
            # Merge overlay with template
            template_page.merge_page(new_page)
            output.add_page(template_page)
        
        # Get archive path
        if date_string is None:
            record_time = customer_information[0]
            date_string = record_time.split(" ")[0]  # Extract date (yyyy-mm-dd)
        
        archive_path = self.config.get_bill_save_path(id, date_string)
        
        # Save to archive
        with open(archive_path, "wb") as archive_stream:
            output.write(archive_stream)
        
        packet.close()
        
        return archive_path
    
    def print_pdf(self, pdf_path):
        """Print PDF using system printer"""
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return False
        
        try:
            import platform
            system = platform.system()
            
            if system == "Windows":
                # Option 1: Use default PDF viewer (will open PDF)
                os.startfile(pdf_path)
                
            else:
                # Linux/Unix printing (for deployment)
                print_command = ['lp', '-d', 'DCPT220', str(pdf_path)]
                subprocess.run(print_command, check=True)
            
            return True
            
        except ImportError as e:
            print(f"Import error: {e}. Install pywin32 for direct Windows printing.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Print error: {e}")
            return False
        except FileNotFoundError:
            print("Print command 'lp' not found. Make sure CUPS is installed.")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def generate_and_print_bill(self, id):
        """Main method to generate and print bill for a customer ID"""
        try:
            # Load bill information using data_loader
            bill_info = self.data_loader.load_bill_info(id)
            if not bill_info:
                print(f"No bill information found for ID: {id}")
                return False
            
            name = bill_info[0] if bill_info[0] else ""
            address = bill_info[1] if bill_info[1] else ""
            amount = str(bill_info[2]) if bill_info[2] else "0"
            
            # Load record time using data_loader
            record_time = self.data_loader.load_record_time(id)
            if not record_time:
                print(f"No record time found for ID: {id}")
                return False
            
            # Load concrete strength from formula_name using data_loader
            strength = self.data_loader.load_concrete_strength(id)
            
            # Parse strength to extract base value
            if strength:
                ending_key = strength.find("ksc")
                if ending_key == -1:
                    ending_key = strength.find("Lean")
                    if ending_key == 0:
                        strength = "Lean"
                else:
                    strength = strength[:ending_key]
            else:
                strength = ""
            
            # Load age and slump using data_loader
            age = self.data_loader.load_concrete_age(id)
            slump = self.data_loader.load_concrete_slump(id)
            
            # Prepare customer information
            customer_information = [
                record_time,
                name,
                address,
                amount,
                strength,
                age,
                slump
            ]
            
            # Generate PDF
            pdf_path = self.generate_pdf_output(customer_information, id)
            success = self.print_pdf(pdf_path)

            return success
            
        except Exception as e:
            print(f"Error generating/printing bill: {e}")
            import traceback
            traceback.print_exc()
            return False