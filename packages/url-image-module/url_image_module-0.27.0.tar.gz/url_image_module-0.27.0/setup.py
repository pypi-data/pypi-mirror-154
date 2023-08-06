import setuptools
import sys
import os
sys.path.append(os.path.dirname(__file__))
import versioneer

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setuptools.setup(
    name="url_image_module",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Urban Risk Lab",
    author_email="url_googleai@mit.edu",
    description="Image Module of REACT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/react76/url-image-module",
    project_urls={
        "Bug Tracker": "https://gitlab.com/react76/url-image-module/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
