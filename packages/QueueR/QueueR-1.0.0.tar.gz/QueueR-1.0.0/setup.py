import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QueueR",
    version="1.0.0",
    author="Rilm2525",
    author_email="rilm2525ce@gmail.com",
    description="The world's simplest queue system for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rilm2525/QueueR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)