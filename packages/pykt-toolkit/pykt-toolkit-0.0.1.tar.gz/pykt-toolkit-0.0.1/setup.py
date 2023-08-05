import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pykt-toolkit",
    version="0.0.1",
    author="pykt-team",
    author_email="pykt.team@gmail.com",
    description="pyKT: A Python Library to Benchmark Deep Learning based Knowledge Tracing Models",
    long_description="pyKT: A Python Library to Benchmark Deep Learning based Knowledge Tracing Models",
    long_description_content_type="text/markdown",
    index="https://github.com/pykt-team/pykt-toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/pykt-team/pykt-toolkit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['pykt'],
    python_requires=">=3.5",
    include_package_data=True,
    install_requires=['pandas'],
)