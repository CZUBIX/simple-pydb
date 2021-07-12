import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "simple-pydb",
    version = "1.2.1",
    author = "czubix",
    description = "Simple python database",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/CZUBIX/simple-pydb",
    license = "MIT",
    project_urls = {
        "Bug Tracker": "https://github.com/CZUBIX/simple-pydb/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
)
