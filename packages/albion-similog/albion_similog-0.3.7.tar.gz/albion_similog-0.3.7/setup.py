from setuptools import find_packages, setup

with open("albion_similog/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split("=")[1].strip(" '\"")
            break
    else:
        __version__ = "0.3.7"

with open("README.md", "rb") as f:
    readme = f.read().decode("utf-8")

setup(
    name="albion_similog",
    version=version,
    description="Compute a consensus dataseries with FAMSA algorithm.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Oslandia",
    author_email="infos@oslandia.com",
    maintainer="Oslandia",
    maintainer_email="infos@oslandia.com",
    url="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=find_packages(),
)
