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
    Image
)
from reportlab.lib.styles import getSampleStyleSheet

data_tables = [
    {
        'title': 'Tabla 1',
        'header': ['Encabezado 1', 'Encabezado 2'],
        'data': [
            [1, 2],
            [3, 4],
            [5, 6]
        ]
    },
    {
        'title': 'Tabla 2',
        'header': ['Header A', 'Header B', 'Header C'],
        'data': [
            [10, 20, 30],
            [40, 50, 60]
        ]
    },
    {
        'title': 'Tabla 3',
        'header': ['Header X', 'Header Y'],
        'data': [
            [100, 200],
            [300, 400]
        ]
    },
    # # ... tus otras tablas aquí ...
]

pdf_title = 'EJEMPLO DE PDF '
out_pdf = 'pdf.pdf'
pdf_image = 'logo.png'


def create_pdf(data_tables, out_pdf, pdf_title, logo_image):
    doc = SimpleDocTemplate(out_pdf, pagesize=landscape(letter))
    story = []
    styles = getSampleStyleSheet()

    # Agregar el logo al PDF
    logo = Image(logo_image, width=1.5 * inch, height=1.5 * inch)
    story.append(logo)

    # Agregar el título del PDF
    title = Paragraph(f"<b>{pdf_title}</b>", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 0.5 * inch))

    story.append(Spacer(1, 0.5 * inch))

    for table_data in data_tables:
        table_title = table_data['title']
        table_header = table_data['header']
        table_content = table_data['data']

        title_paragraph = Paragraph(f'<b>{table_title}</b>', styles['Heading2'])
        header_paragraphs = [Paragraph(cell, styles['Normal']) for cell in table_header]
        table = Table([[title_paragraph], header_paragraphs] + table_content)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)


if __name__ == "__main__":
    create_pdf(data_tables, out_pdf, pdf_title, pdf_image)
    print(f"PDF generado: {out_pdf}")