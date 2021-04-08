import os
import sys
from pdf2image import convert_from_path

def convert_pdf_to_image(pdf_file, image_save_dir, dpi=100):
    infor_pdf = {}
    image_save_dir = os.path.splitext(pdf_file)[0]
    os.makedirs(image_save_dir,exist_ok=True)
    convert_from_path(pdf_file,dpi=dpi,output_folder=image_save_dir,fmt='png',thread_count=4)
    for image_name in os.listdir(image_save_dir):
        old_name = os.path.join(image_save_dir, image_name)
        seg = image_name.split('-')[-1]
        page_number = seg.split('.')[0]
        ext = seg.split('.')[-1]
        new_name = os.path.join(image_save_dir, str(page_number) + '.' + ext)
        os.rename(old_name, new_name)
        infor_pdf[str(page_number)] = new_name.replace('\\', '/')
    return infor_pdf


print(sys.argv[1],sys.argv[2])
print(convert_pdf_to_image(sys.argv[1],sys.argv[2]))