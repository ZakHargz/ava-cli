import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()


def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split("\n")

    return requirements


setup(
    name="avacli",
    version="2.0",
    packages=find_packages(),
    include_package_data=True,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ZakHargz/ava-cli",
    author="Zak Hargreaves",
    author_email="zak@hargreaves.xyz",
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
        ava=ava.cli:cli
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
