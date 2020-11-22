from PIL import Image, ImageOps
from pathlib import Path
import click


@click.command()
@click.option('--threshold', default=127, help='Brightness value at which pixels will be on')
@click.option('--show-output/--no-show-output', default=True, help='Show output image')
@click.option('--invert/--no-invert', default=False, help='Invert output image')
@click.option('-r', is_flag=True, help='rotate by 90')
@click.option('-qr', is_flag=True, help='make "start-point" qr-code')
@click.option('-h', is_flag=True, help='make C/C++ header')
@click.argument('start_point')
@click.argument('size')
def convert(start_point, size, threshold, show_output, invert, r, qr, h):
    """
    optimize images for monocrome displays including C/C++ headers with pixels represented as byte arrays.
    size should be in "wxh"
    """

    if qr:
        import qrcode
        im = qrcode.make(start_point)
        img_file = Path("qrcode")
    else:
        img_file = Path(start_point)
        im = Image.open(start_point)
    if r:
        im = im.transpose(Image.ROTATE_90)
    im = im.resize([int(n) for n in size.split("x")])
    im = im.convert(mode="1", dither=Image.FLOYDSTEINBERG)
    im.show()
    im.save(img_file.with_name(f"{img_file.stem}_{im.size[0]}x{im.size[1]}.jpg"), "JPEG")
    if h: make_header(im, threshold, img_file)


def make_header(im: Image, threshold, img_file: Path, invert=False, show_output=False, ):
    width, height = im.size
    im = ImageOps.invert(im.convert('L')).convert('1')
    with img_file.with_name(f"{img_file.stem}.h").open('w') as header:
        header.write(f"int bmpWidth = {width}, bmpHeight = {height};\n")
        header.write(f"static const unsigned char {img_file.stem}[] = {{\n")
        for b in im.tobytes():
            header.write(f"{b:#x}, ")
        header.write("};\n\n")


if __name__ == '__main__':
    convert()
