import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "lazy-constructs",
    "version": "0.0.5",
    "description": "lazy-constructs",
    "license": "Apache-2.0",
    "url": "https://github.com/lazinessdevs/lazy-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Marcio Almeida<marcioadev@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/lazinessdevs/lazy-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "lazy_constructs",
        "lazy_constructs._jsii"
    ],
    "package_data": {
        "lazy_constructs._jsii": [
            "lazy-constructs@0.0.5.jsii.tgz"
        ],
        "lazy_constructs": [
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
