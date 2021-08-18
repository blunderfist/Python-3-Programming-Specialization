import zipfile
from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')


def get_from_zip(zipped_file):
    with zipfile.ZipFile(zipped_file, 'r') as zip:
        file_lst = []
        #print("List of files in zip")
        #zip.printdir()
        zip.extractall()
        for x in zip.namelist():
            file_lst.append(x)
        
    return file_lst
        
def get_words(img_file):
    
    img_to_read = Image.open(img_file).convert('L')
    words = pytesseract.image_to_string(img_to_read)
    words_lst = []
    for word in words.split():
        words_lst.append(word)
        
    return words_lst



def find_faces(img_file):
    
    image = cv.imread(img_file)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3,  minNeighbors=5, minSize=(40,40))
    temp_image = Image.fromarray(gray)
    drawing = ImageDraw.Draw(temp_image)

    for x,y,w,h in faces:
        drawing.rectangle((x,y,x+w,y+h), outline='white')
        #display(temp_image)
        
    return faces, gray


def create_faces_list(faces, gray):
    
    face_img_lst = []
    temp_image = Image.fromarray(gray)

    for face in faces:
        face_box = (face[0], face[1], face[0]+face[2], face[1]+face[3])
        facial = temp_image.crop(face_box)
        facial = facial.resize((100, 100))
        face_img_lst.append(facial)
        
    return face_img_lst


def make_contact_sheet(face_img_lst):
    
    sheet_width = int(100 * 5)
    sheet_height = int(100 * len(face_img_lst)/5)+100
    contact_sheet = Image.new("RGB", (sheet_width, sheet_height))
    x = 0
    y = 0
    
    for face in face_img_lst:
        contact_sheet.paste(face, (x,y))
        if x + face.width == contact_sheet.width:
            x = 0
            y = y + face.height
        else:
            x = x + face.width
    
    return contact_sheet


zip_files = ['readonly/small_img.zip', 'readonly/images.zip']

def run_ocr(zip_files):
    for zip_file in zip_files:
        image_lst = get_from_zip(zip_file)
        word_search = input('Enter a word to search: ')
    
        for file in image_lst:
            get_text = get_words(file)
            if word_search in get_text:
                print("Results found in file {}".format(file))
                get_faces = find_faces(file)
                get_list = create_faces_list(*get_faces)
                contacts = make_contact_sheet(get_list)
                if len(get_list) > 0:
                    display(contacts)
                else:
                    print("But there were no faces in that file!")

run_ocr(zip_files)
