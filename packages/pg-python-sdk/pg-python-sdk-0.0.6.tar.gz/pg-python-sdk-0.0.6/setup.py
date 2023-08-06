import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pg-python-sdk",
    version="0.0.6",
    author="Abdulmejid Shemsu",
    author_email="abdudlh1@gmail.com",
    description="Python SDK for the Payment Gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abdulmejidshemsu/pg-python-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/abdulmejidshemsu/pg-python-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
)
