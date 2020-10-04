from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["psycopg2>=2.8"]

setup(
    name="pgload",
    version="0.2.6",
    author="Timote WB",
    author_email="timote.wb@gmail.com",
    description="Library of tools to load data from the web into PostgreSQL ",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/codersnotepad/pgload",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
