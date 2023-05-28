import image_module, pdf_module
import os

def test():
    image_module.extract_multiple_images_text("text_from_images.txt")
    image_module.mirror_image('image.png', direction=1)
    image_module.mirror_image('image.png', direction=2)
    image_module.convert_image('image.png', 'jpeg')
    image_module.image_to_pdf("output.pdf")

    os.remove("image.jpeg")
    os.remove("image_flip.png")
    os.remove("image_mirror.png")
    os.remove("text_from_images.txt")

    pdf_module.pdf_to_word("sample.pdf")
    pdf_module.pdf_to_images("sample.pdf")
    pdf_module.merge_pdfs("merged.pdf")
    pdf_module.split_pdf("sample.pdf", [7, "2-5"])

    os.remove("sample_pages_7_2_3_4_5.pdf")
    os.remove("merged.pdf")
    os.remove("sample.docx")
    for index in range(1, 11):
        os.remove(f'page_{index}.jpg')
    os.remove("output.pdf")

test()