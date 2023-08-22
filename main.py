import pyodbc
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Spacer,
    Paragraph,
    PageBreak,
    Image,
    PageTemplate,
    Frame
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas


def execute_procedure(connection_string, procedure_name, option, category):
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    cursor.execute(
        f'EXEC {procedure_name} @usuarioID=22, @rolID=7, @opcion={option}, @Categoria={category}, @resultado=0'
    )

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


pdf_title = 'Vencimientos Vehiculos'
out_pdf = 'vencimientosBogota.pdf'
pdf_image = 'Berlinas.png'
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=172.16.0.25;Database=Gestor;UID=developer;PWD=123456'
procedure_name = 'TP_obtenerVencimientos2'

options = [
    (1, 'TARJETAS DE OPERACION VENCIDAS'),
    (2, 'TARJETAS DE OPERACION POR VENCER'),
    (3, 'SOAT VENCIDOS'),
    (4, 'SOAT POR VENCER'),
    (5, 'RTM VENCIDOS'),
    (6, 'RTM POR VENCER')
]

category = [
    (1, 'vencimientosBogota.pdf'),
    (2, 'vencimientosBarranquilla.pdf')
]


class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.page_template = PageTemplate(id="AllPages", frames=[Frame(
            self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")])
        self.addPageTemplates([self.page_template])

    def after_page(self):
        now = datetime.datetime.now()
        footer_text = f'Documento Generado el {now:%Y-%m-%d %H:%M:%S}'
        self.page_template.add(Frame(
            self.leftMargin, self.bottomMargin + self.height - inch,
            self.width, inch, id="footer", showBoundary=0
        ))
        self.page_template.add(Paragraph(footer_text, styles["Normal"]))
        super().after_page()


def create_pdf(data, category_number, pdf_title, logo_image):
    category_name = None
    for num, name in category:
        if num == category_number:
            category_name = name
            break
    if category_name is None:
        raise ValueError(
            f"Categoría {category_number} no encontrada en la lista")

    out_pdf = category_name
    doc = MyDocTemplate(out_pdf, pagesize=landscape(letter))
    story = []
    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'Times-Bold'
    styles['Normal'].textColor = colors.white
    styles['Normal'].fontName = 'Times-Bold'
    styles['Heading2'].fontName = 'Times-Bold'
    title = Paragraph(f'<b>{pdf_title}</b>', styles['Title'])
    story.append(title)
    story.append(Spacer(1,  0.5 * inch))

    for option, title_procedure in options:
        data = execute_procedure(
            connection_string, procedure_name, option, category_number)
        table_data = {
            'title': f' {title_procedure}',
            'header': ['Empresa', 'Número de Vehículo', 'Placa del Vehículo', 'Número de Documento', 'Fecha Vencimiento'],
            'data': data
        }

        table_title = table_data['title']
        table_header = table_data['header']
        table_content = [list(row)for row in table_data['data']]

        table_title_paragraph = Paragraph(table_title, styles['Heading2'])
        story.append(table_title_paragraph)

        header_paragraphs = [Paragraph(cell, styles['Normal'])
                             for cell in table_header]

        table = Table([header_paragraphs] + table_content)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        c = canvas.Canvas(out_pdf, pagesize=landscape(letter))
        logo = Image(logo_image, width=1.5 * inch, height=1.5 * inch)
        # Dibujar la imagen en la esquina superior izquierda del lienzo
        logo.drawOn(c, inch, doc.height + doc.topMargin - 1.5 * inch)
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))

        now = datetime.datetime.now()
        footer_text = f'Documento Generado el {now:%Y-%m-%d %H:%M:%S}'
        footer = Paragraph(footer_text, styles['Normal'])
        story.append(footer)

        story.append(PageBreak())
        c.save()

    doc.build(story)


if __name__ == '__main__':
    for category_num, _ in category:
        create_pdf(None, category_num, pdf_title, pdf_image)
    print(f'PDF GENERADO SIN ERRORES')
