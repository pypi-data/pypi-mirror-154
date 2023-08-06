from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = "Additional colormaps"
LONG_DESCRIPTION = "Additional colormaps created with quantum transport measurements in mind"

# Setting up
setup(
        name="eminusmap", 
        version=VERSION,
        author="Dags Olsteins",
        author_email="<dags.olsteins@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
	url="https://github.com/TheGingerbeard/eminusmap",
        install_requires=["numpy","matplotlib"], # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', "plotting", "data", "colormaps"],
        classifiers= [
            "Programming Language :: Python :: 3",
	    "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)