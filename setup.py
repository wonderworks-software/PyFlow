from setuptools import setup, find_packages
from PyFlow.Core.version import currentVersion

setup(
    name="PyFlow",
    version=str(currentVersion()),
    packages=find_packages(),
    scripts=['pyflow'],
    include_package_data=True,
    author="Ilgar Lunin, Pedro Cabrera",
    author_email="TODO@example.com",
    description="A general purpose runtime extendable python qt node editor.",
    keywords="visual programming nodeeditor",
    url="https://github.com/IlgarLunin/PyFlow/",   # project home page
    project_urls={
        "Bug Tracker": "https://github.com/IlgarLunin/PyFlow/issues",
        "Documentation": "https://pyflow.readthedocs.io",
        "Source Code": "https://github.com/IlgarLunin/PyFlow/",
    },
    classifiers=[
        'License :: Appache-2.0'
    ],
    install_requires=["enum", "Qt.py", "blinker", "nine", "docutils"],
    extra_requires=["PySide2"]
)
