import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="earthquakealert-ID",
    version="0.0.1",
    author="Christopher Lorence",
    author_email="lorence80@gmail.com",
    description="Retrieve latest earthquake alert from https://www.bmkg.go.id/",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChristCoding/indonesian-earthquake-alert",
    project_urls={
        "Bug Tracker": "https://github.com/ChristCoding/indonesian-earthquake-alert/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)