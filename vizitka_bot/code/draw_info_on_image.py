import io
from PIL import Image, ImageDraw, ImageFont

def resizer(card, file_data):
    image = Image.open(io.BytesIO(file_data))
    width, height = image.size
    new_width = 192
    new_height = 256
    scaling_factor = min(new_width/width, new_height/height)
    resized_image = image.resize((int(width*scaling_factor), int(height*scaling_factor)))
    card.paste(resized_image, (83, 192))
    return card

def visit_card_maker(card_type, card_name, card_phone, card_company, file_data):
    if card_type == 'dark':
        image = Image.open(r'vizitka_bot\content\visit_card_dark.png')
        color = (255, 255, 255)
    elif card_type == 'light':
        image = Image.open(r'vizitka_bot\content\visit_card_light.png')
        color = (0, 0, 0)
    else:
        print("an exception occurred")

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', 32)

    draw.text((600 + 10, 150 - font.size - 10), card_name, font=font, fill=color)
    draw.text((600 + 10, 250 - font.size - 10), card_phone, font=font, fill=color)
    draw.text((600 + 10, 350 - font.size - 10), card_company, font=font, fill=color)

    if file_data:
        image = resizer(image, file_data)
    image.save('vizitka_bot\content\modified_visit_card.png')
    image_bytes = io.BytesIO()
    image.save(image_bytes, "PNG")
    image_bytes.seek(0)
    return image_bytes

if __name__ == "__main__":
    image = visit_card_maker('light', 'Paul Johnson', '89202145402', 'Razrabot', file_data = r'C:\Users\veledara\Pictures\leo.png') # wrong test