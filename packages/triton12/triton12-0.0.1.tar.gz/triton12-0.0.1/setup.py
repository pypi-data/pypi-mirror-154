from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = "Basic commands for T12 data loading and analysis"
LONG_DESCRIPTION = "Commands to explore and load T12 data. Some useful commands for data analysis"

# Setting up
setup(
        name="triton12", 
        version=VERSION,
        author="Dags Olsteins",
        author_email="<dags.olsteins@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
	url="https://github.com/TheGingerbeard/Tritons-dozen",
        install_requires=["numpy", "pandas", "scipy"], # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', 'T12', "data"],
        classifiers= [
            "Programming Language :: Python :: 3",
	    "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)