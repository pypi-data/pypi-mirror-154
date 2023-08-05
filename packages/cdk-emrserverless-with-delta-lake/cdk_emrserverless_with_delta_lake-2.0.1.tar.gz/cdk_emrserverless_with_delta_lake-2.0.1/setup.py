import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk_emrserverless_with_delta_lake",
    "version": "2.0.1",
    "description": "A construct for the quick demo of EMR Serverless.",
    "license": "Apache-2.0",
    "url": "https://github.com/HsiehShuJeng/cdk-emrserverless-with-delta-lake.git",
    "long_description_content_type": "text/markdown",
    "author": "Shu-Jeng Hsieh",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/HsiehShuJeng/cdk-emrserverless-with-delta-lake.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_emrserverless_with_delta_lake",
        "cdk_emrserverless_with_delta_lake._jsii"
    ],
    "package_data": {
        "cdk_emrserverless_with_delta_lake._jsii": [
            "cdk-emrserverless-with-delta-lake@2.0.1.jsii.tgz"
        ],
        "cdk_emrserverless_with_delta_lake": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.27.0, <3.0.0",
        "constructs>=10.1.25, <11.0.0",
        "jsii>=1.59.0, <2.0.0",
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
