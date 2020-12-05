# Data Pirates Challenge

The challenge consists in gathering data from Correios' "Busca Faixa CEP" website, and produce a JSON file which each line is a record containing: unique id, location, CEP range.

# Run the application

This solution was developed using Python 3 and Selenium.

Make sure you have Python 3 installed.

Then, you may want to activate a virtual environment.

To run the script, simply run:

pip install -r requirements.txt

python main.py

# Some observations

The file "geckodriver.exe" was added to the source code to make it simpler to setup the app.
This is necessary to make Selenium open a Firefox browser and navigate through the website.