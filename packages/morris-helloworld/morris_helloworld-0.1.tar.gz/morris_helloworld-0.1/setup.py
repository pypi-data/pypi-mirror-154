from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='morris_helloworld',
    version='0.01',
    description='Say Hello by Morris !',
    py_modules=["helloworld"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type = "text/markdown",
    author ="Morris Lee",
    author_email="info.leekahwin@gmail.com",
)