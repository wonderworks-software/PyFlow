pip install -r requirements.txt
set SPHINX_APIDOC_OPTIONS=members,show-inheritance
sphinx-apidoc -f -o source/ ../PyFlow ../PyFlow/UI/resources.py
make html
pause