import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi-logs",
    version="0.0.0",
    author="Cyberbolt",
    author_email="dtconlyone@gmail.com",
    description="In development.",
    long_description=long_description,
    long_description_content_type="text/markdown",    
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fastapi'
    ]    
)