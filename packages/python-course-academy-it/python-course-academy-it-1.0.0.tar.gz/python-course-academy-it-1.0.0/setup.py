from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'Demonstrating python packaging tools'
LONG_DESCRIPTION = 'Demonstrating python packaging tools ....'

setup(
    name="python-course-academy-it",
    version=VERSION,
    author="Example Author",
    author_email="author@example.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "core"},
    packages=find_packages(where="core"),
    python_requires=">=3.6",
)