from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from datetime import date
from functools import partial


doc = SimpleDocTemplate("example.pdf", pagesize=A4)
styles = getSampleStyleSheet()
elements = []

elements.append(Paragraph("Contracted Products", styles["Heading3"]))

def create_table(data: list[dict]) -> tuple[Table, float]:
    """
    Creates a table from the given data dictionary.

    Note: The data is in the format of 
    list[{
        "id": api_item.get("artikel_id"),
        "name": api_item.get("artikelname"),
        "qty": api_item.get("anzahl"),
        "price": api_item.get("preis_stk"),
        "category": api_item.get("kategorie"),
        "supplier": api_item.get("lieferant"),
        "subtotal": api_item.get("preis_stk", 0) * api_item.get("anzahl", 0)
    })
    """
    table_data = []
    # Header
    headers = ["Product ID", "Name", "Quantity", "Unit Price (€)", "Line Total (€)"]
    table_data.append(headers)

    """
    [{'id': 'C001', 'name': 'Schraube TX20 4x40', 'description': '', 'quantity': 50, 'price': 0.08, 'supplier': 'Würth'}, {'id': 'C002', 'name': 'Schraube TX20 5x60', 'description': '', 'quantity': 50, 'price': 0.12, 'supplier': 'Würth'}, {'id': 'C003', 'name': 'Schraube TX25 6x80', 'description': '', 'quantity': 25, 'price': 0.18, 'supplier': 'Würth'}, {'id': 'C032', 'name': 'Bit TX20', 'description': '', 'quantity': 2, 'price': 1.9, 'supplier': 'Bosch'}, {'id': 'C033', 'name': 'Bit TX25', 'description': '', 'quantity': 2, 'price': 1.9, 'supplier': 'Bosch'}]
    """

    # Rows
    total = 0
    for item in data:
        row = [
            item.get("id"),
            item.get("name"),
            item.get("quantity"),
            item.get("price"),
            item.get("quantity", 0) * item.get("price", 0)
        ]
        table_data.append(row)
        total += item.get("quantity", 0) * item.get("price", 0)

    table = Table(table_data)
    return table, total


def draw_header(canvas, sender_name, sender_address, recipient_address):
    canvas.saveState()

    width, height = A4
    x_left = 25 * mm

    # ---- Supply Contract title (at the very top) ----
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(x_left, height - 15 * mm, "Supply Contract")

    # ---- Sender (small) ----
    # If sender_address is a list, join it; otherwise use as-is
    if isinstance(sender_address, list):
        sender_addr_str = " · ".join(sender_address)
    else:
        sender_addr_str = sender_address
    
    sender = [sender_name, sender_addr_str]

    y_top = height - 25 * mm

    canvas.setFont("Helvetica", 8)
    canvas.drawString(
        x_left,
        y_top,
        " · ".join(sender)
    )

    # ---- Recipient ----
    recipient = recipient_address

    canvas.setFont("Helvetica", 11)
    y = y_top - 15 * mm
    for line in recipient:
        canvas.drawString(x_left, y, line)
        y -= 5 * mm

    # ---- Date (right aligned) ----
    today = date.today().strftime("%d.%m.%Y")

    canvas.setFont("Helvetica", 10)
    canvas.drawRightString(
        width - 25 * mm,
        y_top - 15 * mm,
        f"{today}"
    )

    canvas.restoreState()


def draw_footer(canvas, supplier_name, customer_name):
    canvas.saveState()

    width, _ = A4
    x_left = 25 * mm
    y_bottom = 40 * mm

    canvas.setFont("Helvetica", 10)

    # Supplier line with signature line
    canvas.drawString(x_left, y_bottom, f"Supplier: ({supplier_name})")
    canvas.line(
        x_left + 70 * mm,
        y_bottom - 2,
        x_left + 140 * mm,
        y_bottom - 2
    )

    # Customer line with signature line
    y_customer = y_bottom - 15 * mm
    canvas.drawString(x_left, y_customer, f"Customer: ({customer_name})")
    canvas.line(
        x_left + 70 * mm,
        y_customer - 2,
        x_left + 140 * mm,
        y_customer - 2
    )

    canvas.restoreState()


def draw_page(canvas, doc, sender_name, sender_address, recipient_name, recipient_address):
    draw_header(canvas, sender_name, sender_address, recipient_address)
    draw_footer(canvas, sender_name, recipient_name)


def generate_pdf_contract(contract_data: list[dict], output_path: str):
    table, total = create_table(contract_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("ALIGN", (2,1), (-1,-1), "CENTER"),
    ]))

    print(contract_data)

    elements.append(table)
    
    # Add some space
    elements.append(Spacer(1, 10*mm))
    
    # Add total as separate line, right-aligned
    total_style = styles["Normal"]
    total_style.alignment = 2  # 2 = right alignment
    total_paragraph = Paragraph(f"<b>Total: €{total:.2f}</b>", total_style)
    elements.append(total_paragraph)
    
    # Add payment terms
    elements.append(Spacer(1, 10*mm))
    from reportlab.lib.styles import ParagraphStyle
    payment_terms_style = ParagraphStyle(
        'PaymentTerms',
        parent=styles['Normal'],
        leftIndent=0,
        firstLineIndent=0,
        alignment=0  # 0 = left alignment
    )
    payment_terms = Paragraph("Payment Terms: Net 30 days from invoice date. Delivery within 5 working days after order confirmation.", payment_terms_style)
    elements.append(payment_terms)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=25*mm,
        leftMargin=25*mm,
        topMargin=60*mm,   # important!
        bottomMargin=25*mm,
    )

    draw_page_with_data = partial(
        draw_page,
        sender_name="Hammer Inc.",
        sender_address=[
            "420 Hammer Street",
            "6969 Hammer City",
        ],
        recipient_name="Supplier GmbH",
        recipient_address=[
            "Supplier GmbH",
            "Industriestraße 8",
            "74653 Künzelsau",
        ],
    )

    doc.build(
        elements,
        onFirstPage=draw_page_with_data,
        onLaterPages=draw_page_with_data,
    )


if __name__ == "__main__":

    mock_data = [
        {'id': 'C001', 'name': 'Schraube TX20 4x40', 'qty': 50, 'price': 0.08, 'category': 'Befestigung', 'supplier': 'Würth', 'subtotal': 4.0},
         {'id': 'C004', 'name': 'Dübel 6mm', 'qty': 25, 'price': 0.1, 'category': 'Kunststoff', 'supplier': 'Fischer', 'subtotal': 2.5},
         {'id': 'C023', 'name': 'Atemschutzmaske FFP2', 'qty': 5, 'price': 1.8, 'category': 'PSA', 'supplier': 'Dräger', 'subtotal': 9.0},
         {'id': 'C019', 'name': 'Arbeitshandschuhe Gr.9', 'qty': 2, 'price': 2.5, 'category': 'PSA', 'supplier': 'Uvex', 'subtotal': 5.0},
         {'id': 'C021', 'name': 'Schutzbrille klar', 'qty': 1, 'price': 4.8, 'category': 'PSA', 'supplier': 'Uvex', 'subtotal': 4.8},
         {'id': 'C062', 'name': 'Spachtel 50mm', 'qty': 1, 'price': 2.8, 'category': 'Handwerkzeug', 'supplier': 'Stanley', 'subtotal': 2.8},
         {'id': 'C063', 'name': 'Spachtel 100mm', 'qty': 1, 'price': 3.6, 'category': 'Handwerkzeug', 'supplier': 'Stanley', 'subtotal': 3.6},
         {'id': 'C064', 'name': 'Mischstab Farbe', 'qty': 1, 'price': 1.9, 'category': 'Handwerkzeug', 'supplier': 'Collomix', 'subtotal': 1.9},
         {'id': 'C061', 'name': 'Baueimer 10L', 'qty': 1, 'price': 3.2, 'category': 'Behälter', 'supplier': 'Obi', 'subtotal': 3.2},
         {'id': 'C091', 'name': 'Abstandskeile', 'qty': 20, 'price': 0.25, 'category': 'Kleinmaterial', 'supplier': 'Wolfcraft', 'subtotal': 5.0},
         {'id': 'C092', 'name': 'Fliesenkreuze 3mm', 'qty': 100, 'price': 0.12, 'category': 'Kleinmaterial', 'supplier': 'Wolfcraft', 'subtotal': 12.0},
         {'id': 'C093', 'name': 'Fliesenkreuze 5mm', 'qty': 50, 'price': 0.14, 'category': 'Kleinmaterial', 'supplier': 'Wolfcraft', 'subtotal': 7.0},
         {'id': 'C039', 'name': 'Silikon transparent', 'qty': 2, 'price': 3.8, 'category': 'Dichtstoffe', 'supplier': 'Soudal', 'subtotal': 7.6},
         {'id': 'C041', 'name': 'Acryl weiß', 'qty': 2, 'price': 2.9, 'category': 'Dichtstoffe', 'supplier': 'Soudal', 'subtotal': 5.8},
         {'id': 'C036', 'name': 'Schleifpapier 120', 'qty': 10, 'price': 0.6, 'category': 'Konsum', 'supplier': 'Klingspor', 'subtotal': 6.0},
         {'id': 'C037', 'name': 'Schleifpapier 240', 'qty': 5, 'price': 0.65, 'category': 'Konsum', 'supplier': 'Klingspor', 'subtotal': 3.25},
         {'id': 'C047', 'name': 'Zollstock', 'qty': 1, 'price': 3.2, 'category': 'Messwerkzeug', 'supplier': 'Stabila', 'subtotal': 3.2},
         {'id': 'C046', 'name': 'Wasserwaage 60cm', 'qty': 1, 'price': 18.0, 'category': 'Messwerkzeug', 'supplier': 'Stabila', 'subtotal': 18.0},
         {'id': 'C048', 'name': 'Bleistift Baustelle', 'qty': 3, 'price': 0.9, 'category': 'Schreibwaren', 'supplier': 'Stanley', 'subtotal': 2.7},
         {'id': 'C053', 'name': 'Müllsack 120L', 'qty': 5, 'price': 0.8, 'category': 'Entsorgung', 'supplier': 'Deiss', 'subtotal': 4.0},
         {'id': 'C055', 'name': 'Putztuch Rolle', 'qty': 1, 'price': 6.2, 'category': 'Reinigung', 'supplier': 'Tork', 'subtotal': 6.2}
    ]

    generate_pdf_contract(mock_data, "example.pdf")