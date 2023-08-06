import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ondc',
    version="0.0.1",
    author="Krishna",
    author_email='info@vambook.in',
    description="python adaptor for ondc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vamc-k/python-ondc",
    project_urls={
        "Bug Tracker": "https://github.com/vamc-k/python-ondc/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    keywords='ondc adaptor',
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[],
)
