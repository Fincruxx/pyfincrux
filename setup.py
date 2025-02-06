from setuptools import find_packages, setup

setup(
    name="fincrux",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    test_suite="tests",
    author="Harshit Bansal",
    author_email="harshitbansal587@gmail.com",
    description="The official Python client library for the Fincrux APIs",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
