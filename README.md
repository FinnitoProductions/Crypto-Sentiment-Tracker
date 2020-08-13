# finndex
## Setup (Display Purposes)
### Cloning the Repository
In the command line, execute
```shell
git clone https://github.com/FinnitoProductions/finndex.git
```
Git must be installed for this command to function correctly. Alternatively, download the [notebook](https://github.com/FinnitoProductions/finndex/blob/master/sentiment-analysis.ipynb) stored in the outermost directory of the Git repository.
### Library Installation
Install the the latest version of `finndex` using [pip](https://pip.pypa.io/en/stable/installing/):
```shell
pip3 install finndex
```
All necessary dependencies will be installed in parallel.
### Stanford NLP
To use the sentiment analysis tools included in the library, you must have Stanford's Natural Language Processing library downloaded and stored in the correct location. Download the `.zip` archive at [https://stanfordnlp.github.io/CoreNLP](https://stanfordnlp.github.io/CoreNLP) and place the extracted folder in your home directory. [Java](https://www.java.com/en/) must be installed for the StanfordNLP library to correctly execute.
### Showcasing Key Features
To showcase the key features of the `finndex` library, activate the Jupyter notebook `sentiment-analysis.ipynb` by executing the following command in your terminal after navigating to the directory containing the notebook.
```shell
jupyter notebook
```
The execution of this command will open the Jupyter web interface in your default browser; open the notebook using the presented interface.
## Setup (Development Purposes)
### Virtual Environment
Once you have cloned the repository (see [Cloning the Repository](#cloning-the-repository)), create a virtual environment from which all the notebook code will be executed. This will ensure that all of the installed libraries used are of the correct version.

Within the cloned repository's directory, execute the following commands in your command line.
```shell
cd tests # navigate to the 'tests' directory
python3 -m venv cryptickoenv
source cryptickoenv/bin/activate # activates the Python virtual environment
pip3 install ipykernel
ipython3 kernel install --user --name=cryptickoenv
```
### Installing Libraries
Install all necessary libraries (as dictated in `requirements.txt`) by executing the following command within the `tests` directory to which you navigated in the previous step.
```shell
pip3 install -r ../requirements.txt
```
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
