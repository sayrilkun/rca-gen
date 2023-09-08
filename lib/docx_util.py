#
# Imports
#
from xml.dom.minidom import Document
import docx
from lorem import *
import function
import ruthinit

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

def build_word_document(inc_timeline):
    log.info("Creating Document")
    #initialize document
    doc = docx.Document()

    #Main Header
    doc.add_heading('RUTH Analysis', 0)

    log.info("Filling up RCA Details.")
    #RCA Details
    doc.add_heading('Root Cause Analysis Details', 1)
    rcaparagraph1 = doc.add_paragraph(lorem1)
    rcaparagraph2 = doc.add_paragraph(lorem2)
    rcaparagraph3 = doc.add_paragraph(lorem3)

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

    doc.add_page_break()
    doc.save('output.docx')