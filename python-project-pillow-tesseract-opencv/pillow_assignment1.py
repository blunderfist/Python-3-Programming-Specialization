import PIL
from PIL import Image,ImageEnhance,ImageColor, ImageFont, ImageDraw

#change individual band value, append to new list, return list
def make_imgs_list(image, contact_sheet):
    r,g,b = image.split()
    bands = [r,g,b]
    ratios = [0.1, 0.5, 0.9]
    new_bands = [r,g,b]
    img_lst = []
    font = ImageFont.truetype('readonly/fanwood-webfont.ttf', 50)
    #write_txt = ImageDraw.Draw(image)

    for i in range(len(bands)):
        for j in range(len(bands)):
            new_rgb = bands[i].point(lambda x: x*ratios[j])
            new_bands[i] = new_rgb
            result = Image.merge('RGB', new_bands)
            write_txt = ImageDraw.Draw(contact_sheet)
            #(800x450)
            write_txt.text((j*800,450+(i*500)), "channel {} intensity {}".format(i, ratios[j]), font = font)
            
            img_lst.append(result)
    return img_lst

# read image and convert to RGB
image=Image.open("readonly/msi_recruitment.gif")
image=image.convert('RGB')
#print(image.size)

# create a contact sheet
first_image=image
contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*3,first_image.height*3+150))
x=0
y=0

imgs = make_imgs_list(image, contact_sheet)

for img in imgs:
    # paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height + 50
    else:
        x=x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
display(contact_sheet)
