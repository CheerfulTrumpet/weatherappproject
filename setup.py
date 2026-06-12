"""
Setup configuration for Cognitive Weather Oracle
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cognitive-weather-oracle",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A sophisticated weather app that translates meteorological data into human-centric cognitive narratives",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cognitive-weather-oracle",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    install_requires=[
        "customtkinter>=5.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "advanced": [
            "cairosvg>=2.7.0",
            "Pillow>=10.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cognitive-weather-oracle=main:main",
        ],
    },
)
