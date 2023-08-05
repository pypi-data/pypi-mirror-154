import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gdpshow",
    version="1.0.3",
    author="Arima Naotaka",
    author_email="s2022001@stu.musashino-u.ac.jp",
    description="A package for visualizing any countries GDP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s2022001/",
    install_requires=["pandas","matplotlib"],
    project_urls={
        "Bug Tracker": "https://github.com/s2022001/",
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    package_dir={"": "src"},
    py_modules=['gdpshow'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'gdpshow = gdpshow:main'
        ]
    },
)
