"""Generate two clearly fictional PDFs. Never use for real engineering decisions."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
root=Path(__file__).parent
base=['Product: TD-PANEL-DEMO','Thickness: 12 mm','Density: 480 kg/m3','Grade: DEMO-C24','Usage conditions: Service Class 1 and 2','Application limits: Synthetic illustration only','Certificate: SYNTHETIC-NOT-VALID','Revision date: 2026-01-01']
new=['Product: TD-PANEL-DEMO','Thickness: 1.2 cm','Density: 480 kg/m3','Grade: DEMO-C24','Usage conditions: Service Class 1 only','Application limits: Synthetic illustration only','Certificate: SYNTHETIC-NOT-VALID','Revision date: 2026-02-01']
for name,lines in [('tracedelta-v1-synthetic.pdf',base),('tracedelta-v2-synthetic.pdf',new)]:
    c=canvas.Canvas(str(root/name),pagesize=A4);c.setFont('Helvetica-Bold',16);c.drawString(48,790,'SYNTHETIC MATERIAL DATASHEET - NOT FOR ENGINEERING');c.setFont('Helvetica',11)
    for i,line in enumerate(lines):c.drawString(48,735-i*35,line)
    c.save();print(root/name)
