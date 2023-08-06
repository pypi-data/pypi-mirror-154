from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Yet Another Database'
LONG_DESCRIPTION = 'Yet Another Database, a simple database for Python. Easy to use, easy to maintain, easy to extend.'

# Setting up 
setup(
       
        name="YanDB", 
        version=VERSION,
        author="scorpio8k",
        author_email="scorpion8k2@hotmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pillow'], # external packages as dependencies (optional)
        
        keywords=['python', 'DB', 'Database', 'JSON', 'JSON-based', 'JSON-file', 'JSON-file-based', 'JSON-file-based-database', 'JSON-file-based-database-for-python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
