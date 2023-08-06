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

from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name="cyberByte",
    version="0.0.1",
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
    package_dir={"": "cyberByte"},
    packages=find_packages(where="cyberByte"),
    python_requires=">=3.9",
    license="LICENSE.txt",
)
