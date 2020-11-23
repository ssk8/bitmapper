from PIL import Image, ImageOps
from pathlib import Path
import click


@click.command()
@click.option('-s', is_flag=True, help='Show output image')
@click.option('-r', is_flag=True, help='rotate by 90')
@click.option('-qr', is_flag=True, help='make "start-point" qr-code')
@click.option('-h', is_flag=True, help='make C/C++ header')
@click.argument('start_point')
@click.argument('size')
def convert(start_point, size, s, r, qr, h, ):
    """
    optimize images for monocrome displays including C/C++ headers with pixels represented as byte arrays.
    usage: bitmapper img_file.image_format hxw  where h and w are the desired hight and width of output.
    e.g. bitmapper sample.jpg 250x122
    or to generate QR code:
    bitmapper -qr QRmessage 250x122
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
    if s: im.show()
    im.save(img_file.with_name(f"{img_file.stem}_{im.size[0]}x{im.size[1]}.jpg"), "JPEG")
    if h: make_header(im, img_file)


def make_header(im: Image, img_file: Path, ):
    width, height = im.size
    im = ImageOps.invert(im.convert('L')).convert('1')
    with img_file.with_name("img.h").open('a') as header:
        header.write(f"int {img_file.stem}Width = {width}, {img_file.stem}Height = {height};\n")
        header.write(f"static const unsigned char {img_file.stem}[] = {{\n")
        for n, b in enumerate(im.tobytes(), 1):
            header.write(f"{b:#x}, ")
            if not n%16: header.write('\n')
        header.write("};\n\n")


if __name__ == '__main__':
    convert()
