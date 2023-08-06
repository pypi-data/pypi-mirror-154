from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'A tkinter game maker'
LONG_DESCRIPTION = 'Tk game is an package that helps make games with tkinter. it is really basic right now, but it will be improved in the future.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="TkGame", 
        version=VERSION,
        author="scorpio8k",
        author_email="scorpion8k2@hotmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pillow'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'game', 'tkinter'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
