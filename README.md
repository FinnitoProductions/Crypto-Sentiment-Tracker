# Crypticko Sentiment Tracker
## Setup
### Virtual Environment
Once you have cloned the repository, create a virtual environment from which all the notebook code will be executed. This will ensure that all of the installed libraries used are of the correct version.

Within the cloned repository's directory, execute the following commands in your command line.
```shell
python3 -m venv cryptickoenv
source cryptickoenv/bin/activate # activates the Python virtual environment
pip install ipykernel
ipython kernel install --user --name=cryptickoenv
```
### Installing Libraries
Install all necessary libraries (as dictated in `requirements.txt`) by executing the following command in the project directory.
```shell
pip install -r requirements.txt
```
### Stanford NLP
Stanford's Natural Language Processing library (used in this project for Sentiment analysis) requires a large download. Download the `.zip` archive at [https://stanfordnlp.github.io/CoreNLP](https://stanfordnlp.github.io/CoreNLP) and place the extracted folder in your home directory.
### Running the Notebook
To activate the Jupyter notebook, execute the following command &mdash; Anaconda and Jupyter must be installed.
```shell
jupyter notebook
```
This should take you to a page on your preferred browser which lists the contents of the project directory. Open `sentiment-analysis.ipynb`. To ensure all code is executed in your newly created virtual environment, open the `Kernel` tab and select `Change Kernels > cryptickoenv`. You are now ready to run the notebook. To run every cell, select `Cell > Run All`. To run an individual cell, select that cell and type the `Shift-Enter` keyboard shortcut.
## Project Contributors
* **Finn Frankis** - *Software Developer* - [FinnitoProductions](https://github.com/FinnitoProductions)
* **Somnath Banerjee** - *Software Mentor* - [sbanerjee2020](https://github.com/sbanerjee2020)
* **Sumantro Banerjee** - *Financial Analyst*
* **Michael Frankis** - *Financial Mentor*
