"""
Setup configuration for Castroix
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="castroix",
    version="1.0.0",
    author="SluberskiHomeLab",
    description="A lightweight cross-platform media streaming launcher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SluberskiHomeLab/castroix",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Pillow>=9.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "castroix=castroix_package.__main__:main",
        ],
        "gui_scripts": [
            "castroix-gui=castroix_package.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.png", "*.json"],
    },
)
