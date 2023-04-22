import pdf_module
import os

def main():
    pdf_module.pdf_to_word("sample.pdf")
    pdf_module.merge_pdfs(2) 
    pdf_module.split_pdf("sample.pdf", [7,"2-5"]) 
    pdf_module.pdf_to_img("sample.pdf")

    os.remove("sample_pages_7_2_3_4_5.pdf")
    os.remove("merged_pdf.pdf")
    os.remove("sample.docx")
    for index in range(1, 11):
        os.remove(f'page_{index}.jpg')
        
main()        
