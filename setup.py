from setuptools import setup, find_packages

setup(
    name="axiom-battle",
    version="0.1.0",
    description="公理对抗赛引擎 — Popper证伪主义的代码化",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="悟道体系",
    author_email="zhouhailiang0116@github.com",
    url="https://github.com/zhouhailiang0116/axiom-battle",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
