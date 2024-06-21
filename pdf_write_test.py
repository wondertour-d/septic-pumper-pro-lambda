from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter




def create_single_overlay_with_fields(overlay_pdf_path, fields):
    """
    Create a single overlay PDF with form fields.

    Parameters:
    overlay_pdf_path (str): Path to save the overlay PDF.
    fields (list of dict): List of fields with format {'type': 'text'|'checkbox'|'radio', 'name': str, 'x': float, 'y': float, 'page': int, 'checked': bool, 'selected': str (for radio buttons), 'options': list (for radio buttons)}.
    """
    c = canvas.Canvas(overlay_pdf_path, pagesize=letter)
    width, height = letter

    for field in fields:
        field_type = field['type']
        name = field['name']
        x = field['x']
        y = height - field['y']  # ReportLab uses bottom-left as origin

        if field_type == 'text':
            c.drawString(x, y, name)
        elif field_type == 'checkbox':
            c.rect(x, y - 10, 10, 10)  # Draw a rectangle to represent checkbox
            c.drawString(x + 15, y, name)  # Add text label next to checkbox
            if field.get('checked', False):
                c.line(x, y - 10, x + 10, y)  # Draw check mark
                c.line(x, y, x + 10, y - 10)
        elif field_type == 'radio':
            options = field.get('options', [])
            selected = field.get('selected', None)
            for option in options:
                c.circle(x + 5, y - 5, 5)  # Draw a circle to represent radio button
                c.drawString(x + 15, y, option)
                if option == selected:
                    c.circle(x + 5, y - 5, 3, fill=1)  # Fill the selected radio button
                y -= 20  # Move y position for the next radio button

    c.save()


def merge_pdfs(base_pdf_path, overlay_pdf_path, output_pdf_path):
    """
    Merge a base PDF with an overlay PDF.

    Parameters:
    base_pdf_path (str): Path to the base PDF.
    overlay_pdf_path (str): Path to the overlay PDF.
    output_pdf_path (str): Path to save the merged PDF.
    """
    base_pdf = PdfReader(base_pdf_path)
    overlay_pdf = PdfReader(overlay_pdf_path)
    output_pdf = PdfWriter()

    overlay_page = overlay_pdf.pages[0]  # Assuming a single overlay page

    for page_num in range(len(base_pdf.pages)):
        base_page = base_pdf.pages[page_num]
        base_page.merge_page(overlay_page)
        output_pdf.add_page(base_page)

    with open(output_pdf_path, 'wb') as output_file:
        output_pdf.write(output_file)


# Example usage
input_pdf_path = 'septage_pumping_report_form_blank.pdf'
output_overlay_path = 'overlay.pdf'
output_pdf_path = 'output_form.pdf'

data = {
  "customerInfo": {
    "firstName": "Henry",
    "lastName": "Hudson",
    "address": "3457 Gravy Lane",
    "pumpingDate": "4/1/2023",
    "county": "Franklin",
    "township": "Fred",
    "phone": "614-909-0999",
    "email": "test@wt.com",
    "isOwner": True,
    "customerType": "residential"
  },
  "tankSystem": {
    "tanks": [
      {
        "tankNumber": 1,
        "material": {
          "concrete": True,
          "fiberglass": False,
          "plastic": True,
          "brick": False,
          "metal": False
        },
        "condition": "Good",
        "tankType": "Aeration",
        "typeOther": "",
        "aerationType": "new",
        "aeratorMotor": "Present",
        "risers": "Present",
        "riserLocation": {
          "inlet": True,
          "centerOfTank": False,
          "outlet": False
        },
        "riserLids": "Absent",
        "riserCondition": "Poor",
        "evidenceOfLeaking": "Yes",
        "leakingLocation": {
          "tank": False,
          "riser": True,
          "inlet": False,
          "outlet": False,
          "inconclusive": False
        },
        "waterLevel": "Could Not Determine",
        "previousHighWaterLevel": "No",
        "baffleAndTees": "Present",
        "baffleAndTeesCondition": "Good",
        "effluentFilters": "Present",
        "effluentFiltersCleaned": "Yes",
        "otherSolidsRemoved": {
          "none": True,
          "filtermedia": False,
          "peat": False,
          "otherCheckbox": False,
          "other": ""
        },
        "gallonsPumped": 10
      },
      {
        "tankNumber": 2,
        "material": {
          "concrete": True,
          "fiberglass": False,
          "plastic": False,
          "brick": False,
          "metal": False
        },
        "condition": "Good",
        "tankType": "Holding",
        "typeOther": "",
        "aerationType": "",
        "aeratorMotor": "",
        "risers": "Present",
        "riserLocation": {
          "inlet": True,
          "centerOfTank": True,
          "outlet": True
        },
        "riserLids": "Present",
        "riserCondition": "Good",
        "evidenceOfLeaking": "Inconclusive",
        "leakingLocation": {
          "tank": False,
          "riser": False,
          "inlet": False,
          "outlet": False,
          "inconclusive": False
        },
        "waterLevel": "No",
        "previousHighWaterLevel": "No",
        "baffleAndTees": "Absent",
        "baffleAndTeesCondition": "",
        "effluentFilters": "Present",
        "effluentFiltersCleaned": "Yes",
        "otherSolidsRemoved": {
          "none": False,
          "filtermedia": True,
          "peat": True,
          "otherCheckbox": False,
          "other": "paper"
        },
        "gallonsPumped": 10
      }
    ]
  },
  "generalInfo": {
    "dewateringNecessary": "Yes",
    "dewateringGallons": 100,
    "dewateringWasteWaterFacility": "Delaware City, WW",
    "spillageOccured": "Yes",
    "spillageCleaned": "Yes",
    "repairsAndAdditionalWork": "additional repairs done on septic system",
    "comments": "nice customers",
    "disposalLocation": "Waste Water Treatment Facility",
    "nameOfFacility": "Delaware City, WW",
    "permitNumber": 10000,
    "permitAddress": "123 Newfield Blvd",
    "technicianName": "Marcus Caplin",
    "septageHaulingCompany": "MJC Septic",
    "companyPhone": "740-816-3945",
    "registrationNumber": 189465,
    "yearsTilNextService": 3,
    "monthsTilNextService": 0
  },
  "systemInfo": {
    "isProd": True
  }
}

# List all form fields
list_form_fields(input_pdf_path)

fields = [
    {'type': 'text', 'name': 'John Doe', 'x': 50, 'y': 100, 'page': 0},
    {'type': 'text', 'name': '123 Main St', 'x': 50, 'y': 150, 'page': 0},
    {'type': 'text', 'name': 'Anytown, USA', 'x': 50, 'y': 200, 'page': 0},
    {'type': 'checkbox', 'name': 'Agree to terms', 'x': 50, 'y': 250, 'page': 0, 'checked': True},
    {'type': 'radio', 'name': 'Gender', 'x': 50, 'y': 300, 'page': 0, 'options': ['Male', 'Female', 'Other'],
     'selected': 'Male'}
]

create_single_overlay_with_fields(output_overlay_path, fields)
merge_pdfs(input_pdf_path, output_overlay_path, output_pdf_path)
