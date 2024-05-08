import setuptools

with open("README.md" ,  "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt","r", encoding="utf-8") as req:
    required = req.read().splitlines()

setuptools.setup(
    name="data_validator",
    version="0.0.1a",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires = required
)