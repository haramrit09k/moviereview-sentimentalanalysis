# Movie Review Using Sentimental Analysis

## Linux

Install pip first:

`sudo apt-get install python3-pip`

Then install virtualenv using pip3:

`sudo pip3 install virtualenv`

Now create a virtual environment:

`virtualenv venv`

Active your virtual environment:

`source venv/bin/activate`

(To deactivate, just type `deactivate`)

Run `pip install -r requirements.txt` (Python 2), or `pip3 install -r requirements.txt` (Python 3)

**Optional**:

Then train the data using the following command:

    `python train_data.py`

This step is optional because we have already trained the dataset and stored it as a **pickle** file

## Windows

Installing virtualenv on Windows is a bit complicated than Linux. Refer to [this](http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/) link for installing virtualenv on your Windows machine:

Once in the virtual environment (indicated by virtual environment name shown towards the left in the terminal in parentheses), run the following command:

`pip install -r requirements.txt`

This is to install all the required packages in the virtual environment for running the app.

To start the Flask server:

`python main.py`