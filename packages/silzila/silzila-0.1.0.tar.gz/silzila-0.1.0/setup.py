import setuptools

# Standard library imports
import pathlib
# Third party imports
from setuptools import setup
# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent
# The text of the README file is used as a description
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="silzila",                     # This is the name of the package
    version="0.1.0",                        # The initial release version
    author="Balu Mahendran",                     # Full name of the author
    author_email="mail@silzila.org",
    description="App for Dashboarding & Data Exploration",
    # Long description read from the the readme file
    long_description=README,
    long_description_content_type="text/markdown",
    # List of all python modules to be installed
    packages=setuptools.find_packages(),
    include_package_data=True,
    # package_data={'': ['*.html', '*.css', '*.js', '*.jsx']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',                # Minimum version requirement of the package
    # py_modules=["quicksample8"],             # Name of the python package
    # Directory of the source code of the package
    # package_dir={'': 'quicksample8/src'},
    # Install other dependencies if any
    install_requires=['uvicorn', 'fastapi', 'aiosqlite', 'bcrypt', 'cryptography', 'logger',
                      'passlib', 'psycopg2-binary', 'PyJWT', 'PyMySQL', 'pyodbc', 'shortuuid', 'SQLAlchemy', 'typing_extensions', 'python-decouple', 'email-validator', 'python-multipart', 'pathlib'],

    entry_points={'console_scripts': ['silzila = silzila.main.__main__:main']},

)
