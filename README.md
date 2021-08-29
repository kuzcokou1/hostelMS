## Operational Requirements.

1. Python(v2.7+) must be installed and running on the PC. This should be accessible through the system variables. 
2. A local server for testing should also be installed. (XAMPP, LAMPP, WAMPP).
3. This web application is able to run on any hardware provided the software requirements are met.

## System Features

1. Manage Users/Staff/Wardens.
	* Add, Update, Delete users

2. Profile
	* View the logged in user information

3. Manage Hostels
	* Add, view, update and Delete Hostels

4. Manage Students
	* Add, update, view and Delete students


## Log in credentials

username: kuzco_kou
password: password

**You should be able to change those credentials once the system is up and running. (Recommended)**


## Server Requirements

PHP version 5.6 or newer is recommended.

    It should work on 5.3.7 as well, but we strongly advise you NOT to run
    such old versions of PHP, because of potential security and performance
    issues, as well as missing features.

Application Server

    You can choose to install any of the following Application Server: LAMP, MAMP, XAMMP. 


## Getting Started.

1. Clone the project from GitHub onto your desired location on your computer. [https://github.com/kuzcokou1/hostelMS.git]
2. Open PhpMyAdmin from your local Application Server.
3. Create new database and name it as "hostel"
4. Import hostel.sql to your hostel database.
5. Turn On Apache and MySQL on your Application Server Control Panel.
6. Assuming you have successfully cloned the project. Open your command prompt/Terminal and change your directory into your project folder. For example, cd/Desktop/hostelMS.
7. You should be able to install all the project dependecies and libraries through the **requirements.txt** file in the project folder. This is achieved by running *pip* in the command prompt/Terminal. **pip install -r requirements.txt**. 
8. Once all is successfully done without errors, proceed and run *python app.py* or *flask run* on the command prompt/Terminal.
9. To access the system, it should be found on *http://127.0.0.1:5000/*.


# Acknowledgement

Great Project. Updates
