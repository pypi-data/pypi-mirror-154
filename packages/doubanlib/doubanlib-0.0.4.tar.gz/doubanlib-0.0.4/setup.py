import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="doubanlib",
    version="0.0.4",
    author="xhboke",
    author_email="2361903575@qq.com",
    description="An api tool for DouBan movie.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xhboke/douban",
    project_urls={
        "Bug Tracker": "https://github.com/xhboke/douban/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)