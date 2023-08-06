from setuptools import setup, find_packages

classifiers = [

    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

setup(
    name='global_tools_win',
    version='0.1.0',
    description='Batch tools running on Windows 10//Deneme Version',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Ersse',
    author_email='ms1msp0136@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Global_Tools_Win',
    packages=find_packages(),
    install_requires=['random','tkinter','urllib','ip2geotools','ip2geotools.databases.noncommercial','socket','bs4','pygame','qrcode','turtle','pyfiglet','sys','datetime',"instaloader","colorama"]
)