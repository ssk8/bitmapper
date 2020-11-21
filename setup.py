from setuptools import setup


setup(
    name='bitmapper',
    version="0.4",
    py_modules=['convert'],
    install_requires=['click', 'pillow'],
    entry_points='''
        [console_scrips]
        convert=convert:cli
    ''',
)