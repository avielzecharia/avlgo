from setuptools import find_packages, setup

setup(
    name="avlgo",
    version="0.0.0",
    description='A simple API for advanced algorithms & data-structures',
    author='Aviel Zecharia',
    author_email="avielz1199@gmail.com",
    python_requires=">=3.9.1",
    url="https://github.com/avielzecharia/avlgo",
    include_package_data=True,
    install_requires=["numpy", "pympler"],
    packages=find_packages(exclude=["tests"])
)
