import pdf2docx, pdf2image, img2pdf
import PIL, PyPDF2, pathlib
import os.path
   
def pdf_to_word(pdf_path):
	# Generate the output file name based on the input file name
	docx_path = pdf_path.replace(".pdf", ".docx")  
	# Convert the PDF to Word
	pdf2docx.parse(pdf_path, docx_path) 
	print(f"Conversion complete. Output file saved as {docx_path}")

def merge_pdfs(*file_names):
    if len(file_names) == 1:
        if isinstance(file_names[0], list):
            file_names = file_names[0]
        elif file_names[0].endswith('.txt'):
            with open(file_names[0], 'r') as f:
                file_names = f.read().splitlines()
    # Create a PdfMerger object
    merger = PyPDF2.PdfMerger()
    # Loop through each file and add it to the merger
    for i, file_name in enumerate(file_names, start=1):
        # Make sure the file exists
        if not os.path.isfile(file_name):
            print(f"{file_name} does not exist.")
            continue
        # Add the file to the merger
        with open(file_name, 'rb') as f:
            merger.append(PyPDF2.PdfReader(f))
    # Write the merged PDF to a new file
    with open('merged_pdf.pdf', 'wb') as f:
        merger.write(f)
    print("Merged PDF file saved as merged_pdf.pdf")

def split_pdf(filename, pages):
    # Combine the page ranges from all arguments into a single list
    all_pages = []
    for page_range in pages:
        if isinstance(page_range, int):
            all_pages.append(page_range)
        elif isinstance(page_range, str):
            start, _, end = page_range.partition('-')
            if not start.isdigit() or not end.isdigit():
                raise ValueError(f'Invalid page range: {page_range}')
            start = int(start)
            end = int(end)
            if start > end:
                raise ValueError(f'Invalid page range: {page_range}')
            all_pages.extend(range(start, end + 1))
        else:
            raise ValueError(f'Invalid page range: {page_range}')
    
    # Open the PDF file
    with open(filename, 'rb') as f:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(f)
        # Get the total number of pages
        num_pages = len(reader.pages)        
        # Validate the pages argument
        if not all(1 <= p <= num_pages for p in all_pages):
            raise ValueError('Invalid page range')  
        # Create a PDF writer object
        writer = PyPDF2.PdfWriter()       
        # Add the specified pages to the writer object
        for p in all_pages:
            writer.add_page(reader.pages[p - 1])    
        # Create a new PDF file with the specified pages
        new_filename = os.path.splitext(filename)[0] + '_pages_' + '_'.join(str(p) for p in all_pages) + '.pdf'
        with open(new_filename, 'wb') as f:
            writer.write(f)      
        # Print the filename of the new PDF file
        print(f'New file created: {new_filename}')

def pdf_to_img(filename):
    # Open the PDF file
    with open(filename, 'rb') as pdf_file:
        # Use pdf2image library to convert PDF pages to images
        images = pdf2image.convert_from_path(pathlib.Path(pdf_file.name), dpi=1000)       
        # Iterate over each page in the PDF and save as JPG image
        for idx, img in enumerate(images):
            img.save(f'page_{idx+1}.jpg', 'JPEG', quality=80)
        print("PDF converted successfully")        
        # Close the PDF file
        pdf_file.close()

def image_to_pdf(*image_paths, pdf_path="output.pdf"):
    # creating list of image objects
    images = [PIL.Image.open(image_path) for image_path in image_paths]
    # converting images to chunks using img2pdf
    pdf_bytes = img2pdf.convert([image.filename for image in images])
    # opening or creating pdf file
    with open(pdf_path, "wb") as file:
        # writing pdf files with chunks
        file.write(pdf_bytes)
    # closing image files
    for image in images:
        image.close()
    # output
    print("Successfully made pdf file")
        
def main():
    pdf_to_word("sample.pdf")
    merge_pdfs("sample.pdf","sample.pdf") 
    split_pdf("sample.pdf", [7,"2-5"]) 
    pdf_to_img("sample.pdf")
    image_to_pdf("image.png")
    os.remove("sample_pages_7_2_3_4_5.pdf")
    os.remove("merged_pdf.pdf")
    os.remove("sample.docx")
    for index in range(1, 11):
        os.remove(f'page_{index}.jpg')
    os.remove("output.pdf")
main()                                
