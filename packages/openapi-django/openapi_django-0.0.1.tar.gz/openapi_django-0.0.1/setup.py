import setuptools


setuptools.setup(
     name='openapi_django',
     author="Y. Chudakov",
     author_email="kappasama.ks@gmail.com",
     version='0.0.1',
     description="A package for generate django openapi doc",
     packages=setuptools.find_packages(),
     package_dir={'openapi_django': 'openapi_django/'},
     install_requires=[],
     classifiers=[
         "Programming Language :: Python :: 3",
     ],
     python_requires='>=3.8'
)
