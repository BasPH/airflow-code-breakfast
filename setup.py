import setuptools

setuptools.setup(
    name="airflow_breakfast",
    version="0.1",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "apache-airflow~=1.10.3",
        "pytest~=4.4.1",
        "pytest-helpers-namespace~=2019.1.8",
        "pytest-mock~=1.10.4",
    ],
    python_requires="==3.6.*",
)
