import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reportlab-pdf-table-builder",  # Replace with your own username
    version="0.0.9",
    author="Timotheos Savva",
    author_email="timotheos.savva12@gmail.com",
    description="A simple pdf table builder using the ReportLab Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cutomsols/pdf-table-builder",
    packages=setuptools.find_packages(),
    install_requires=[
        'reportlab',
        'pillow'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
