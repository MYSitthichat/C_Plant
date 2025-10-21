from fpdf import FPDF

pdf = FPDF('P', 'mm', 'A4')
pdf.add_page()

pdf.add_font('Kinnari', '', '/fonts/Kinnari.ttf')
pdf.set_font('Kinnari', '', 12) # 12 is font size

pdf.cell(0, 10, u'สวัสดี')
pdf.ln(10) # new line
pdf.cell(0, 10, u'ชาวโลก')
pdf.line(8, 20, 30, 20) # draw line(x1, y1, x2, y2)

pdf.output('exam.pdf') # generate pdf file