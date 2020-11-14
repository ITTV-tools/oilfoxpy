import setuptools

setuptools.setup(
    name="oilfoxpy",
    version="0.1",
    author="ittv-tools",
    description="API call to oilfox",
    url="https://github.com/ITTV-tools/olifoxpy",
    py_modules=["oilfox"],
    package_dir={'': 'src'},
    install_requires=['jwt', 'json', 'requests'],
    classifieres=[
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9"
    ]

)
