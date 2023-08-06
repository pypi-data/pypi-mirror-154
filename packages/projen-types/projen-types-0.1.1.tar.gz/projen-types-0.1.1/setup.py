import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "projen-types",
    "version": "0.1.1",
    "description": "My custom projen project types",
    "license": "Apache-2.0",
    "url": "https://github.com/mnoumanshahzad/projen-types.git",
    "long_description_content_type": "text/markdown",
    "author": "mnoumanshahzad<mnoumanshahzad@hotmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/mnoumanshahzad/projen-types.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "projen-types",
        "projen-types._jsii"
    ],
    "package_data": {
        "projen-types._jsii": [
            "projen-types@0.1.1.jsii.tgz"
        ],
        "projen-types": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "jsii>=1.60.1, <2.0.0",
        "projen>=0.58.2, <0.59.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
