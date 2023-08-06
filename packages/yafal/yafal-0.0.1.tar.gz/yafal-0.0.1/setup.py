import setuptools

__version__ = "0.0.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yafal",
    version=__version__,
    author="Manex Serras",
    author_email="mserras001@gmail.com",
    description="Identification of Fake Labels using Large Model embeddings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://yafal.llinguai.eus",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    keywords=[
        "Natural Language Processing",
        "Artificial Intelligence",
        "Fake Label detection",
        "Deep Learning"
    ],
    package_dir={"": "yafal"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=["pydantic", "numpy", "torch", "transformers", "scikit-learn"]
)