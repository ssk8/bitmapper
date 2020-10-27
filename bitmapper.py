import sys, math, colorsys
import click
from PIL import Image

@click.command()
@click.option('--threshold', default=127, help='Brightness value at which pixels will be on')
@click.option('--show-output/--no-show-output', default=True, help='Show output image')
@click.option('--invert/--no-invert', default=False, help='Invert output image')
@click.option('--new_dim', default=False, help='change output dimentions')
@click.argument('image_file')
def convert(image_file, threshold, show_output, invert, new_dim):
    """
    img2h will convert bitmaps to C/C++ headers with pixels represented
    as byte arrays.
    """
    im = Image.open(image_file)
    width, height = im.size
    columns = int(math.ceil(width / 8.0))
    if new_dim:
        new_width, new_height = [int(n) for n in new_dim.split()]
    width = int(width)
    height = int(height)
    
    name, ext = image_file.split('.')
    with open(name + '.h', 'w') as header:
        header.write(f"int bmpWidth = {width}, bmpHeight = {height};\n")
        header.write("static const unsigned char " + name + "[] = {\n")

        for y in range(0, height):
            header.write("\t")

            for column in range(0, columns):
                pix_byte = ''
                for bit in range(0, 8):
                    x = column * 8 + bit
                    char = "0"
                    if x < width:
                        #print(im.getpixel((x, y)))
                        pixel = colorsys.rgb_to_hsv(*im.getpixel((x, y))[:3])
                        if pixel[2] < threshold:
                            char = "1"
                    if invert:
                        char = "1" if char == "0" else "0"
                    pix_byte += char
                    if show_output:
                        sys.stdout.write(" " if char == "0" else "#")
                header.write(f'{int(pix_byte,2):#x}')
                header.write(", ")
            header.write("\n")
            if show_output:
                sys.stdout.write("\n")

        header.write("};\n\n")

if __name__ == '__main__':
    convert()