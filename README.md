# Next-Word-Predictor

Installing Virtual Environment :

`pip3 install virtualenv`

Creating a Python Virtual Environment:

`python -m venv venv`

Activating the newly created virtual env - venv:

`.\venv\Scripts\activate`

Install all the libraries from requirements file:

`pip install -r .\requirements`

Making all default migrations to the local:

`python manage.py migrate`

Run the server locally by manually hosting:

`python manage.py runserver`

Activating and running the project on local server

![server](./staticfiles/images/server.jpg)

SignIn Page

![login](./staticfiles/images/login.jpg)

SignUp Page

![login_2](./staticfiles/images/login_2.jpg)

The application runs on a Django framework and gives a rapid response through a Webscoket connection using BERT engine for prediction. The app takes in the user input text and provides a 3 suggested word predcitons that the user can use as follows.

![NWP](./staticfiles/images/ui.gif)

The application stores the user details on the Django's default database viewed from the admin's portal. It stores details like user's name, session id, date and timestamp, typed sentences and predicted words.

![Output](./staticfiles/images/out.jpg)

![db](./staticfiles/images/db.jpg)

Further, in the upcoming developments, this data will be used for developing analytics for the application. Stay tuned!
