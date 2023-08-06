#
#     Copyright (C) 2022  Nikolas Boling
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see
#     https://github.com/Nikolai558/CyberByte/blob/development/LICENSE.txt.
#

# Instructions on uploading to PyPi
#   python -m pip install --upgrade build
#   python -m pip install --upgrade twine
#   ---------------------------------------------------------
#   Update Version Number in Setup.py
#   ---------------------------------------------------------
#   python -m build
#   ---------------------------------------------------------
#   python -m twine upload --repository testpypi dist/*
#   OR
#   python -m twine upload dist/*
#   ---------------------------------------------------------
#   Enter "__token__" for the username, then enter your PyPi Token.
#   ---------------------------------------------------------

from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="cyberByte",
    version="0.0.4",
    author="Nikolai558",
    author_email="38259407+Nikolai558@users.noreply.github.com",
    description="A Packaged that was created to practice the logic of Blockchains!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nikolai558/CyberByte",
    project_urls={
        "Bug Tracker": "https://github.com/Nikolai558/CyberByte/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        # "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    license="LICENSE.txt",
)
