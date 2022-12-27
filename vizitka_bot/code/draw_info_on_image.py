from PIL import Image, ImageDraw, ImageFont

def resizer(card, image_path):
    image = Image.open(image_path)
    width, height = image.size
    new_width = 192
    new_height = 256
    scaling_factor = min(new_width/width, new_height/height)
    resized_image = image.resize((int(width*scaling_factor), int(height*scaling_factor)))
    card.paste(resized_image, (83, 192))
    return card

def visit_card_maker(card_type, card_name, card_phone, card_company, card_image_path = None):
    color = ()
    if card_type == 'dark':
        image = Image.open(r'vizitka_bot\content\visit_card_dark.png')
        color = (255, 255, 255)
    elif card_type == 'light':
        image = Image.open(r'vizitka_bot\content\visit_card_light.png')
        color = (0, 0, 0)
    else:
        print("an exception occurred")

    draw = ImageDraw.Draw(image)
    # Choose a font and font size
    font = ImageFont.truetype('arial.ttf', 32)

    draw.text((600 + 10, 150 - font.size - 10), card_name, font=font, fill=color)
    draw.text((600 + 10, 250 - font.size - 10), card_phone, font=font, fill=color)
    draw.text((600 + 10, 350 - font.size - 10), card_company, font=font, fill=color)

    if card_image_path == None:
        pass
    else:
        image = resizer(image, card_image_path)
    image.save('vizitka_bot\content\modified_visit_card.png')
    return image

if __name__ == "__main__":
    image = visit_card_maker('light', 'Paul Johnson', '89202145402', 'Razrabot', card_image_path = r'C:\Users\veledara\Pictures\leo.png')