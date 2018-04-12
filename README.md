# moviereview-sentimentalanalysis

## Linux:

Install pip first
	sudo apt-get install python3-pip

Then install virtualenv using pip3
	sudo pip3 install virtualenv 

Now create a virtual environment
	virtualenv venv 

Active your virtual environment:
	source venv/bin/activate

(To deactivate, just type deactivate)

Run pip install -r requirements.txt (Python 2), or pip3 install -r requirements.txt (Python 3)

Then train the data using the following command:
	python train_data.py


## Windows:

Installing virtualenv on Windows is a bit complicated than Linux.
Refer to this link for installing virtualenv on your Windows machine: 
	http://timmyreilly.azurewebsites.net/python-pip-virtualenv-installation-on-windows/
