#
# Imports
#
from xml.dom.minidom import Document
import docx
from lorem import *
import function
import ruthinit
from docx2pdf import convert
import aspose.words as aw
from docx.shared import RGBColor

#
# Globals
#
log = ruthinit.log

def build_docx(output_text):
        

    # Create a document
    doc = docx.Document()

    # Add a paragraph to the document
    p = doc.add_paragraph()

    # Add some formatting to the paragraph
    p.paragraph_format.line_spacing = 1
    p.paragraph_format.space_after = 0

    # Add a run to the paragraph
    run = p.add_run("python-docx")

    # Add some formatting to the run
    run.bold = True
    run.italic = True
    run.font.name = 'Arial'
    run.font.size = docx.shared.Pt(16)


    # Add more text to the same paragraph
    run = p.add_run(" Tutorial")

    # Format the run
    run.bold = True
    run.font.name = 'Arial'
    run.font.size = docx.shared.Pt(16)

    # Add another paragraph (left blank for an empty line)
    doc.add_paragraph()

    # Add another paragraph
    p = doc.add_paragraph()

    # Add a run and format it
    run = p.add_run(output_text)
    run.font.name = 'Arial'
    run.font.size = docx.shared.Pt(12)

    # Save the document
    doc.save("output.docx")

def build_word_document(rca_det, inc_timeline):
    log.info("Creating Document")
    #initialize document
    doc = docx.Document()

    # Main Color: Core Green (75,205,62)
    # Supporting Color 1: Teal (0,151,117)
    # Supporting Color 2: Dark Teal (1,91,126)

    #Main Header
    h1 = doc.add_heading('RUTH Analysis', 0)
    h1.style.font.color.rgb = RGBColor(75,205,62)

    log.info("Filling up RCA Details.")
    #RCA Details
    doc.add_heading('Root Cause Analysis Details', 1)
    doc.add_heading('Root Cause', 2)
    rcaparagraph1 = doc.add_paragraph(rca_det[0])
    doc.add_heading('RCA Executive Summary', 2)
    rcaparagraph1 = doc.add_paragraph(rca_det[1])
    doc.add_heading('Investigation & Resolution', 2)
    rcaparagraph1 = doc.add_paragraph(rca_det[2])
    doc.add_heading('Contributing Factors', 2)
    rcaparagraph1 = doc.add_paragraph(rca_det[3])

    log.info("Filling up incident timeline.")
    #incident timeline
    doc.add_heading('Incident Timeline', 1)
    timeline_table = doc.add_table(rows=1, cols=3)
    columns = timeline_table.rows[0].cells
    columns[0].text = "Date"
    columns[1].text = "Time"
    columns[2].text = "Contents"
    
    log.info(inc_timeline[0])

    for x in inc_timeline:
        log.info(f"processing {x}")
        row = timeline_table.add_row().cells
        row[0].text = x["Date"]
        row[1].text = x["Time"]
        row[2].text = x["Contents"]

    # doc.font.color.rgb = RGBColor(75,205,62)
    doc.add_page_break()
    doc.save('output.docx')

def convert_word_to_pdf(filepath, filename='output'):
    '''
    convert word to pdf

    parameters:
        filepath - docx filepath
    
    return:
        path - pdf path
    '''
    log.info("Converting DOCX to PDF")
    path = f'{filename}.pdf'

    log.info(f"pdf path and name: {path}")
    convert(filepath, path)

    return path

def convert_word_to_pdf_unix(filepath, filename='output'):
    '''
    convert word to pdf

    parameters:
        filepath - docx filepath
    
    return:
        path - pdf path
    '''

    path = f"{filename}.pdf"
    log.info("Converting DOCX to PDF")
    docfile = aw.Document(filepath)
    docfile.save(path)

    log.info(f"pdf path and name: {path}")

    return path