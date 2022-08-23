from PIL import Image, ImageDraw, ImageFont

def graph_receipt(receipt: object)-> object:
    max_min = receipt.get_max()
    main_blocks = receipt.get_all_list_info_blocks()

    width = max_min[0] + 5
    height = max_min[1] + 5
    
    white = (250, 250, 250)
    black = (0, 0, 0)
    gray = (70, 70, 70)

    img  = Image.new( mode = "RGB", size = (width, height) , color= white)
    draw = ImageDraw.Draw(img)

    color=[gray, black, gray]
    size = 29

    for n in range(3):
        for i in main_blocks[n]:
            # draw.rectangle((i[0], i[1], i[4], i[5]), outline=black)

            font = ImageFont.truetype("arial.ttf", size)
            draw.text((i[0], i[1]),i[-1],font=font, fill=color[n])

            size = 17

    return img