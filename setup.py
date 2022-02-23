import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openkmi",
    version="0.0.1",
    author="Tim Franken",
    author_email="tim.franken@sumaqua.be",
    description="Python package to download synoptic measurements from RMI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/TimFranken/openkmi",
    project_urls={
        "Documentation": "https://gitlab.com/TimFranken/openkmi",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)