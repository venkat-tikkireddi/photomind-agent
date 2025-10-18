# PhotoMind Agent

## Create a virtual environment

Create the virtual environment: Execute the python -m venv command followed by the desired name for your virtual environment. A common practice is to name it venv or env. 
Code

    python -m venv venv

## To activate virtual environment

This command will create a new directory (e.g., venv) within your project folder, containing a self-contained Python installation and its associated packages.
Activate the virtual environment:
On Windows:
Code

        .\venv\Scripts\activate
On macOS/Linux.
Code

        source venv/bin/activate

## Install the dependencies

Run the below command

Code

        pip install -r requirements.txt

## Create a environment file (.env) and the API keys

1. create .env file
2. Add the API Keys