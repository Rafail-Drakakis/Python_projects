# Import the required module
import pdf2docx

# Prompt the user for the input file name
pdf_path = input("Enter the name of the PDF file to convert (include the .pdf extension): ")

# Generate the output file name based on the input file name
docx_path = pdf_path.replace(".pdf", ".docx")

# Convert the PDF to Word
pdf2docx.parse(pdf_path, docx_path)

print(f"Conversion complete. Output file saved as {docx_path}")

