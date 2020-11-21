#!/usr/bin/python3

import colorsys
import math
import click
from PIL import Image

@click.command()
@click.option('--threshold', default=127, help='Brightness value at which pixels will be on')
@click.option('--show-output/--no-show-output', default=True, help='Show output image')
@click.option('--invert/--no-invert', default=False, help='Invert output image')
@click.option('--resize', default=False, help='change output dimentions')
@click.option('--rot', default=False, help='rotate by')
@click.option('-qr', is_flag=True, help='make "start-point" qr-code')
@click.argument('start_point')
def convert(start_point, threshold, show_output, invert, resize, rot, qr):
    """
    convert bitmaps to C/C++ headers with pixels represented as byte arrays.
    """
    if qr:
        import qrcode
        im = qrcode.make(start_point)
        start_point = "qrcode._"
    else:
        im = Image.open(start_point)
    if rot:
        im = im.rotate(int(rot))
    if resize:
        im = im.resize([int(n) for n in resize.split()])
    im = im.convert(mode="1", dither=Image.FLOYDSTEINBERG)
    im.show()

    width, height = im.size
    width = int(width)
    height = int(height)
    columns = int(math.ceil(width / 8.0))

    name, _ = start_point.split('.')

    with open(name + '.h', 'w') as header:
        name = 'pic'
        header.write(f"int bmpWidth = {width}, bmpHeight = {height};\n")
        header.write("static const unsigned char " + name + "[] = {\n")

        for y in range(height):
            header.write("\t")

            for column in range(columns):
                pix_byte = ''
                for bit in range(8):
                    x = column * 8 + bit
                    char = "0"
                    if x < width:
                        if hasattr(im.getpixel((x, y)), "__iter__"):
                            pixel = colorsys.rgb_to_hsv(*im.getpixel((x, y))[:3])
                        else:
                            pixel = [0,0,im.getpixel((x, y))]
                        if pixel[2] < threshold:
                            char = "1"
                    if invert:
                        char = "1" if char == "0" else "0"
                    pix_byte += char
                    if show_output:
                        print(" " if char == "0" else "#", end ="")
                header.write(f'{int(pix_byte,2):#x}')
                header.write(", ")
            header.write("\n")
            if show_output:
                print()

        header.write("};\n\n")

if __name__ == '__main__':
    convert()
