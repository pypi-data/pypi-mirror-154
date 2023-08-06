import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="argofamiglia",
    version="0.1.0",
    author="salvatore.abello",
    author_email="salvatore.abello2005@gmail.com",
    description="Simple library that allows you to interface Python with the API of Argo Scuola Next.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/salvatore-abello/ArgoFamigliaAPI",
    install_requires=['certifi==2022.5.18.1', 'charset-normalizer==2.0.12', 'idna==3.3', 'requests==2.27.1', 'urllib3==1.26.9'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
