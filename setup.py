import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wordpress_osm_shortcode_generator",
    version="0.0.1",
    author="Sebastian Blaes",
    author_email="sebastianblaes@gmail.com",
    description="Create shortcode and markers file for the OSM wordpress plugin from gpx tracks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s-bl/wordpress-osm-shortcode-generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)