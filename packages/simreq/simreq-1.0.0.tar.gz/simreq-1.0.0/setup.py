import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "simreq",
    version = "1.0.0",
    author = "Jiro",
    author_email = "contact@jiroawesome.tech",
    description = "A simple library that is similar to requests.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jiroawesome/simreq.py",
    project_urls = {
        "Bug Tracker": "https://github.com/jiroawesome/simreq.py/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)