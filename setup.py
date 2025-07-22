from setuptools import setup, find_packages

setup(
    name="slackformat",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mistune",
    ],
    python_requires=">=3.7",
)
