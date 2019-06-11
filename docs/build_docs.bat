set SPHINX_APIDOC_OPTIONS=members
sphinx-apidoc -f -o source/ ../PyFlow
make html
pause