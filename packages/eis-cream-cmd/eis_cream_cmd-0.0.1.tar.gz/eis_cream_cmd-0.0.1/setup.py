import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eis_cream_cmd",
    version="0.0.1",
    author="Emily Du",
    author_email="emilydu@uw.edu",
    description="data visualization tool for echem data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuefan98/Machine-Learning-on-EIS",
    project_urls={
        "Bug Tracker": "https://github.com/yuefan98/Machine-Learning-on-EIS",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points={
                        'console_scripts': [
                                'ec=eis_cream.eis_cream:main',
                        ]
                },
    python_requires=">=3.6",
)
