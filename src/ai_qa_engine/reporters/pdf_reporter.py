import os
from datetime import datetime
from typing import Dict, Any
# Note: to install reportlab package: pip install reportlab
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class PdfReporter:
    """
    Generates professional PDF evaluation reports using ReportLab.
    Generiert professionelle PDF-Auswertungsberichte.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_report(self, evaluation_type: str, data: Dict[str, Any]) -> str:
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab is not installed. Run `pip install reportlab` to enable PDF generation.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{evaluation_type}_report_{timestamp}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor("#2c3e50"),
            spaceAfter=15
        )

        story.append(Paragraph(f"AI-QA Engine Report: {evaluation_type}", title_style))
        story.append(Paragraph(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 15))

        table_data = [["Metric / Parameter", "Value"]]
        for key, value in data.items():
            table_data.append([str(key), str(value)])

        t = Table(table_data, colWidths=[200, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f8f9fa")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#2c3e50")),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#ddd"))
        ]))

        story.append(t)
        doc.build(story)

        return filepath