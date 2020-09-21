import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

gh_url = "https://github.com/briandconnelly/airnow-py/issues"

setuptools.setup(
    name="airnow",
    version="0.1.0",
    author="Brian Connelly",
    author_email="x@bconnelly.net",
    description="Retrieve air quality information from AirNow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=gh_url,
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Testing",
    ],
    project_urls={
        "Bug Reports": f"{gh_url}/issues",
        "Source": gh_url,
    },
)
