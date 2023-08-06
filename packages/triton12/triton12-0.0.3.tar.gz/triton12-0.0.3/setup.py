import setuptools
VERSION = '0.0.3' 
DESCRIPTION = "commands for t12 data"
LONG_DESCRIPTION = "commands for reading and working with t12 format data plus some additional useful commands"

# Setting up
setuptools.setup(
        name="triton12", 
        version=VERSION,
        author="Dags Olsteins",
        author_email="<dags.olsteins@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
	url="https://github.com/TheGingerbeard/eminusmap",
        install_requires=["numpy","pandas","scipy"], # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', "plotting", "data", "colormaps"],
        classifiers= [
            "Programming Language :: Python :: 3",
	    "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ],

	package_dir={"": "src"},
    	packages=setuptools.find_packages(where="src"),
)