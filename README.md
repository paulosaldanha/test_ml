
# Machine Learning and Data Science with Python
This repository is basically a place with some coding what I'm learning about Machine Learning and Data Science, all in Python


## Stock value prediction:
It tries to predict a value from a given share on Brazilian stock exchange based on a date and closing value, with a percentage of correct with a variation of 6% up or down.

# Requirements to Run on Your Local Environment
Be sure that you have pip installed in your local environment (pip already comes into Python default installation since the version 3.6).

You can check Python version, by typing the following command:
`$ python -V`

And then, check if pip is installed typing:
`$ pip -V`

If `pip` is not installed, please install it on your computer, following the official documentation:
 - https://pip.pypa.io/en/stable/


# Installing dependencies
Having Python on version >= 3.6, and pip installed on your machine, it's time to install the dependencies, using `pip` packages manager. You will need to type on your console the following command:
`$ pip install -r requirements.txt`

That command above it will check all dependencies that are described in the `requirements.txt` file, that exists in the project root. `Pip` will then check these dependencies and will search for them in a repository, it will download them and will of all them into your computer.

If you get an error related to `lzma compression` dependency, please find the solution in this following link: 
 - https://stackoverflow.com/questions/57743230/userwarning-could-not-import-the-lzma-module-your-installed-python-is-incomple

Another thing that you have to installed in your local environment is `Chromedriver`, which will be responsible to automate the whole process through `Selenium`. Please find more information about `Chromedriver` (downloads, installation, how to use it, etc.) in the following link: https://sites.google.com/a/chromium.org/chromedriver/getting-started

And if you have done everything until here without any issue, it's time to run the app.

# Running app

In the console, in the project root, you just need to type `python app.py`
