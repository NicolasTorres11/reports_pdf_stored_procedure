from fpdf import FPDF

pdf = FPDF(orientation='P', unit='mm', format='A4')

pdf.add_page()

# pdf.rect(x=90, y=80, w=70, h=95)


pdf.line(20, 30, 190, 30)
pdf.output('ejemplo.pdf')

