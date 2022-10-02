import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='gym_browser_dashboard',
     version='0.1',
     author="Valerio Biscione",
     author_email="valerio.biscione@gmail.com",
     description="Use the browser as a dashboard for your gym environment. Show dynamic images and lineplots.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/ValerioB88/gym-browser-dashboard",
     packages=['gym_browser_dashboard'],
     include_package_data=True,
     install_requires=[
        'fastapi',
        'uvicorn[standard]',
     ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )