# office-inventory-system

* [Main Technologies](#main-technologies)
* [Key Features](#key-features)
* [Installation](#installation)
* [Usage](#usage)
* [Demo Access](#demo-access)
* [Additional Information](#additional-information)

A simple application for tracking office equipment, with three user types - Administrator, Support, Employee, the ability to submit service requests and assign equipment to different users.



## Main Technologies

* Python 3.13
* Django 5.1.6
* PostgreSQL
* HTML5
* CSS3

## Key Features

* **Equipment Assignment to Employee(s):** Allows assigning equipment to specific users, ensuring clear tracking.
* **Internal Serial Number System with Validation:** Ensures the uniqueness of each piece of equipment through serial number validation, preventing errors and duplication.
* **Service Request Submission System:** Simplifies the process of submitting repair or maintenance requests for equipment, ensuring efficient response to issues.
* **Three User Types (Administrator, Support, Employee):** Distribution of access rights according to user roles, ensuring security and control.

## Installation

1.  Clone the repository: `git clone https://github.com/YBlck/office-inventory-system.git`
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the virtual environment:
    * Windows: `venv\Scripts\activate`
    * macOS/Linux: `source venv/bin/activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Run migrations: `python manage.py migrate`
6.  Create a superuser: `python manage.py createsuperuser`
7.  Start the server: `python manage.py runserver`

## Usage

1.  Open a browser and go to `http://127.0.0.1:8000/`.
2.  Log in using administrator credentials (or create a new user).
3.  Use the navigation menu to access system functions.

## Demo Access

* Website: https://gear-tracker.onrender.com
* Test User: `employee` / `support` / `admin`
* Password: `1qazcde3`

## Additional Information

* The application uses the PostgreSQL database for data storage.
* The standard Django authentication system is used to configure user access rights.
