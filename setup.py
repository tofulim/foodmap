from setuptools import find_packages, setup

setup(
    name="crawl",
    packages=find_packages(),
    python_requires=">=3.6.0",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_data={},
    dependency_links=[],
    include_package_data=True,
    zip_safe=False,
)
