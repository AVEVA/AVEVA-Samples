import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ocs_sample_library_preview",
    version="0.0.6_preview",
    author="OSIsoft",
    author_email="dendres@osisoft.com",
    description="A preview of an OCS (OSIsoft Cloud Services) client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/osisoft/ocs-samples",
    packages=setuptools.find_packages(),    
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)