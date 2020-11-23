bitmapper
=========
python tool to convert image for use in monochromatic displays, e.g. eInk including byte arrays in c/c++ header format

This tool will create a jpg of image or QR-code of input text. The -h option will create (or append) an img.h file. I'm using these with Arduino language for output to e-paper display. All created QR-code images appended will have the same variable name in the header file so will need to be fixed manually.

.. image::https://raw.githubusercontent.com/ssk8/bitmapper/main/fine.jpeg
