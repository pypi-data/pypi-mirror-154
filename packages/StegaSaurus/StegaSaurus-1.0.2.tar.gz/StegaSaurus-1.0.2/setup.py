import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="StegaSaurus",
    version="1.0.2",
    scripts=['./scripts/StegaSaurus'],
    author="Alexander Bisland",
    author_email="biztecbritain@gmail.com",
    description="Dependency-free library for steganography (GUI and CLI included)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BizTecBritain/StegaSaurus",
    project_urls={
        "Bug Tracker": "https://github.com/BizTecBritain/StegaSaurus/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    install_requires=["setuptools>=42", "pillow>=9.0.0"],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
