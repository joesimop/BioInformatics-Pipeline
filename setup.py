from setuptools import setup, find_packages

setup(
    version="1.0",
    name="byop",
    packages=find_packages(),
    py_modules=["byop"],
    author="Joe Simopoulos",
    description="Create and run pipelines for bioinformatics tools",
    entry_points={
        'console_scripts': ['byop=byop.byop:main'],
    },
    include_package_data=True,
)