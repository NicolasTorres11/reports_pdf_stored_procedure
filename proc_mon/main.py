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


# FUNCION PARA LLAMAR EL PROCEDIMIENTO DE ALAMCENADO
# TRAEREMOS LA CONEXION A LA BD, EL NOMBRE DEL PROCEDIMIENTO, LA OPCION DEL PROCEDIMIENTO, Y LA CATEGORIA, LOS CUALES SON PARAMETROS
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


# TITULO DEL PDF
pdf_title = 'Vencimientos Vehiculos'

# Imagen y logo
pdf_image = 'Berlinas.png'
# CONNECION A LA BD
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=172.16.0.25;Database=Gestor;UID=developer;PWD=123456'
# NOMBRE DEL PROCEDIMIENTO
procedure_name = 'TP_obtenerVencimientos2'

# OPCIONES DEL PROCEDIMIENTO
options = [
    (1, 'TARJETAS DE OPERACION VENCIDAS'),
    (2, 'TARJETAS DE OPERACION POR VENCER'),
    (3, 'SOAT VENCIDOS'),
    (4, 'SOAT POR VENCER'),
    (5, 'RTM VENCIDOS'),
    (6, 'RTM POR VENCER')
]

# CATEGORIAS(CIUDADES) Y NOMBRES DEL PDF
category = [
    (1, 'vencimientosBogota.pdf'),
    (2, 'vencimientosBarranquilla.pdf')
]


# TEMPLATE DEL PDF
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


# FUNCION PARA LA CREACION DEL PDF
# TENDREMOS COMO PARAMETROS, DATA -> QUE SERA LA INFORMACION QUE CONTENDRA EL PDF, ESTA VENDRA DEL PROCEDIMIENTO
# CATEGORY_NUMBER -> A ESTE LE PASAREMOS LA TUPLA DE CATEGORY PARA CONTROLAR LAS CIUDADES DEL PROCEDIMIENTO
# PDF_TITLE -> EL TITULO DE NUESTRO PDF
# PDF_IMAGE -> IMAGEN DEL PDF
def create_pdf(data, category_number, pdf_title, logo_image):

    # recorrer la categoria y segun el numero generar el nombre del pdf
    # ademas de devolvernos el numero de la categoria para pasarlo al procedimiento
    category_name = None
    for num, name in category:
        if num == category_number:
            category_name = name
            break
    if category_name is None:
        raise ValueError(
            f"Categoría {category_number} no encontrada en la lista")

    # este out_pdf traera el nombre del pdf
    out_pdf = category_name
    # generaremos los estilos iniciales del pdf
    doc = MyDocTemplate(out_pdf, pagesize=landscape(letter))
    story = []
    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'Times-Bold'
    styles['Normal'].textColor = colors.white
    styles['Normal'].fontName = 'Times-Bold'
    styles['Heading2'].fontName = 'Times-Bold'
    title = Paragraph(f'<b>{pdf_title}</b>', styles['Title'])

    logo = Image(logo_image, width=1.5 * inch, height=1.5 * inch)
    logo_frame = Frame(
        doc.leftMargin, doc.height + doc.topMargin - 1.5 * inch,
        1.5 * inch, 1.5 * inch, id="logo_frame"
    )
    logo_frame.addFromList([logo], doc)
    story.append(title)
    story.append(Spacer(1,  0.5 * inch))

    # Esta sera el for para recorrer los datos del procedimiento de almacenado
    # el cual tendra el titulo del procedimiento y las opciones
    for option, title_procedure in options:
        # llamaremos al procedimiento y la pasaremos los datos
        # recorreremos la lista de options y category_number
        data = execute_procedure(
            connection_string, procedure_name, option, category_number)
        table_data = {
            'title': f' {title_procedure}',  # titulo del procedimiento
            # headers del procedimiento
            'header': ['Empresa', 'Número de Vehículo', 'Placa del Vehículo', 'Número de Documento', 'Fecha Vencimiento'],
            'data': data  # informacion que le pasaremos al procedimiento
        }

        # Titulo de la tabla
        table_title = table_data['title']
        # header de la tabla
        table_header = table_data['header']
        # datos de la tabla
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
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))

        # footer de la tabla con la fecha y hora de generacion
        now = datetime.datetime.now()
        footer_text = f'Documento Generado el {now:%Y-%m-%d %H:%M:%S}'
        footer = Paragraph(footer_text, styles['Normal'])
        story.append(footer)

        story.append(PageBreak())

    doc.build(story)


if __name__ == '__main__':
    for category_num, _ in category:
        create_pdf(None, category_num, pdf_title, pdf_image)
    print(f'PDF GENERADO SIN ERRORES')
