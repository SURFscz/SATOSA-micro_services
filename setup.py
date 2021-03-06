from setuptools import setup

setup(
    name="SCZ_SATOSA_micro_services",
    version="0.1",
    author="Martin van Es",
    author_email="martin@surfnet.nl",
    description=("SCZ SATOSA micro_services."),
    license="Apache 2.0",
    keywords="scz satosa micro service",
    url="https://github.com/SURFscz/SATOSA-micro_services/",
    packages=["scz_micro_services"],
    package_dir={"": "src"},
    install_requires=[
        "mysqlclient", "requests", "future-fstrings"
    ],
    zip_safe=False,
)
