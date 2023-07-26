import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_pydash",
    version="0.1",
    author="Valerio Biscione",
    author_email="valerio.biscione@gmail.com",
    description="Use the browser as a dashboard for your experiments. Show dynamic images and lineplots. Expecially suited for Open AI gym.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ValerioB88/simple-pydash",
    packages=["simple_pydash"],
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
