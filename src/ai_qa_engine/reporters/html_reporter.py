import os
from datetime import datetime
from typing import Dict, Any

class HtmlReporter:
    """
    Generates professional HTML evaluation reports.
    Generiert professionelle HTML-Auswertungsberichte.
    """
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_report(self, evaluation_type: str, data: Dict[str, Any]) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{evaluation_type}_report_{timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>AI-QA Report - {evaluation_type}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; color: #333; }}
                .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; }}
                .status-pass {{ color: #27ae60; font-weight: bold; }}
                .status-fail {{ color: #c0392b; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
                th {{ background-color: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>AI-QA Engine Audit Report</h1>
                <p><strong>Evaluation Type:</strong> {evaluation_type}</p>
                <p><strong>Timestamp:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <hr>
                <h2>Results Summary</h2>
                <table>
                    <tr><th>Metric / Parameter</th><th>Value</th></tr>
        """

        for key, value in data.items():
            html_content += f"<tr><td>{key}</td><td>{value}</td></tr>"

        html_content += """
                </table>
            </div>
        </body>
        </html>
        """

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        return filepath