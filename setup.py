from setuptools import setup, find_packages

setup(
    name="fpl_ml",
    version="0.0.1",
    packages=find_packages(),
    description="Optimize planner for Fantasy Premier League",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/haakools/fpl_ml",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
