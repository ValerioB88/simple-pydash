from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="simple_pydash",
    version="0.3.5",
    author="Valerio Biscione",
    author_email="valerio.biscione@gmail.com",
    description="Lightweight, modular Python library for creating real-time interactive dashboards in the web browser.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ValerioB88/simple-pydash",
    packages=["simple_pydash"],
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "numpy",
        "Pillow",
        "plotly",
        "sty",
        "matplotlib",
        "jinja2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
