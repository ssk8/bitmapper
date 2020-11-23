from setuptools import setup


setup(
    name='bitmapper',
    version="0.4",
    py_modules=['bitmapper'],
    install_requires=['click', 'Pillow', 'qrcode'],
    entry_points='''
        [console_scrips]
        bitmapper=bitmapper:convert
        '''
)