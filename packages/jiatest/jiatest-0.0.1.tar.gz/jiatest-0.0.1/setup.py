from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jiatest',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url='https://github.com/pypa/sampleproject',
    license='meituan',
    author='jiahaha',
    author_email='jiahaha@example.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['facebook-wda == 1.4.6'],
    classifiers=[
   
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
  
    ],
    python_requires='>=3.6',
)

# pypi-AgEIcHlwaS5vcmcCJGQ5MzBjMDQzLWYwYTMtNDMwZS1iYmQ3LWMyMGUxYTdhODIzMgACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYg2erBmTU7RaGmPTkXtuPa3zpjik8fLwKlh8XvU0nrtSc