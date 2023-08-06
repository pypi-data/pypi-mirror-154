import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "test-contruct-lib",
    "version": "0.0.3",
    "description": "test-contruct-lib",
    "license": "Apache-2.0",
    "url": "https://github.com/fsalamida/test-contruct-lib.git",
    "long_description_content_type": "text/markdown",
    "author": "Francesco Salamida<salamida@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/fsalamida/test-contruct-lib.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "test_contruct_lib",
        "test_contruct_lib._jsii"
    ],
    "package_data": {
        "test_contruct_lib._jsii": [
            "test-contruct-lib@0.0.3.jsii.tgz"
        ],
        "test_contruct_lib": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.27.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.60.1, <2.0.0",
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
