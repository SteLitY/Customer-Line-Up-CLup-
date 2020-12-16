
# Customer Line-Up Web Application
COVID has added safety restrictions for stores. We need to make sure that the store
isn’t too crowded and that the lines don’t have too many people on it. The goal of this
project is to develop an easy-to-use webapp that
1. Allows store managers to regulate the amount of people inside the store

2. Save the client’s time from having to physically wait in line (especially when the
weather is bad). 
3. Make sure the store continues to remains profitable with our line management system. Attention will also be given to the store’s profits (ex: the more people in the store, the
more money the store earns. So, we need to let clients in as soon as there is space
available). If we don’t pay attention to the store’s profit, they will not use the app. 

Staff and managerial personnel will be able to see the amount of people within their store and
the amount of people in the queue. A QR code is generated for those who sign up on
the web application. Individuals or groups will scan their QR codes to get into the store,
when they are finished shopping, a cashier will scan them out, and the next person or
group may enter the store.

## List of features:
* Innovative ticket system
	* Allow people to sign up online, in person, and over the phone. The tickets
	numbers will be given starting from 1. People coming in person or are calling
	over the phone will have their spot on-the-line tracked by the online system.
	Ticket numbers are first come first serve. The smaller your ticket number, the
	closer you are to the front of the line.
* Monitor inflow/outflow
	* Allow people to sign up groups of people (one person in queue can mean more
than 1 customer going into the store)
	* Limit the amount of people in store (don’t let clients in if the capacity is reached)
* Capacity monitor
	* Prevent clients from going past capacity.
	* Keep track of how many people are currently in the store.
		* Scan in and scan out with QR code (Assume cashier scans customer out after checking out their items)
		* Include count for employees. During "rush hours" where there are more
clients, they also need more staff to accommodate them (ex: more
employees to restock shelves). Include the extra staff in the store capacity.
	* Optional feature - allow the business to send messages to everyone in the
queue through email or text message. (ex: send an alert to customer if
item has run out or if they want to give a special offer to people waiting on
queue, etc.)
* COVID Requirements to enter store
	* Masks - Reminders to wear a mask - (can be added to the message sent
to clients when they successfully entered the queue. If we have time, ask
client to take a photo of themselves with a mask on and use machine
learning to see if group has mask on)
* Reservation (line)
	* Button to go on the line and leave it.
	* Time limit to come. If the client doesn’t arrive when it’s their turn. Send an
alert to the client telling them they have ___ minutes to come. After ___
minutes, take the client off queue, increment tardiness_ by 1.
* Warn customers when they’re 10th/5th/1st person on the queue. Number
is relative to how fast the store serves clients. Ex: A bigger store can serve
100 clients a minute while a smaller store with fewer employees can serve
10 a minute. We want to give the client time to come to the store so the
bigger store would have a warning when they’re 200th on the queue, while
the smaller store might warn the client when they’re 10th on the queue.
* Timestamp (know when client arrives + leaves)

* Vicinity to store
	* “I’m nearby” button
* Times of operations
	* Closing and Opening of stores. Prevent clients from entering the queue
when they are not expected to get in before the store closes.
	* Reservation closing time.

## Test plan
To test this web application, our team will open the webapp on different platforms and browsers
(iphone, android, PC. firefox, chrome, IE). We will test different client sign-up methods and
apply stress tests to each feature to test the extents to which the app may break. We will set up
a mock store on a machine and populate the queue with new users in the
virtual line. We will have a given number of QR codes in an “active” state meaning that they are
inside the store and several customers outside the store in an inactive state. We will test the variable store_capacity_ and make sure it properly decrements its value when a group or indiividual leaves the store


## Technologies 
* Django
* mySQL 
    * Workbench

## Linux 
### Dependencies
1. Donwload Python 3.8 
<https://www.python.org/downloads/>
* Create / Activate the environment\
	```pipenv shell``
* ```pip install requirements.txt``` 

2. While in the virtual environment 
* You will see *(project-clup-*******)* prefacing your CLI input
    * This means you are in your virtual environment  

3. Install mySQL
* This will allow you to manage data migrations\
```pip install mysqlclient```
* If you encounter any errors with this, [click here](https://stackoverflow.com/questions/35190465/virtualenvpython3-4-pip-install-mysqlclient-error)

4. Install other libraries
* ```pip install django-crispy-forms``` This will allow forgot password forms to work

* ```pip install django-ses``` This is for sending emails for things like "forgot password". 

* ```pip install django-filter``` This is a search filter

* ```pip install boto3```  This is for sending text messages
* ```pip install django-heroku``` This is for deployment of the website
* ```pip install qrcode``` This is to generate the qrcode
* ```pip install pillow``` Supports qrcode
* ```pip install dj_Static ``` 

## How to use:

1. open cmd (windows) or terminal and navigate to the src folder using the cd command

2. type: "python manage.py runserver"

3. open http://127.0.0.1:8000/




## Final Written Report
### Abstract (4 sentences) : 
**CustomerLineup** is a web application that modulates the influx of customers for registered stores. Our service offers a safe and efficient method to monitor customers in store and those on line with an innovative ticketing system. We understand that **COVID-19** has made shopping stressful and uncertain. We strive to return in-store shopping to its former glory by creating an easy and intuitive step-based system of lining up, shopping, and exiting a given store reflected in an easy-to-use customer queue.              
###  Introduction (0.5 pages):
   *   State the problem. Use an example.
   *   State your contributions (the rest of the paper explains how you achieved these)
###  Main content section:
  *   Recap problem, this time with details. (0.5 pages)
  *  The idea (1 page)
        -   What is novel about your work?
   *   Technical details (1 page per team member)
        
		(Ethan)
		AJAX was used to create a data flow for the Business Control 	Panel and Customer Queue view. We needed to first understand the stateless nature of http requests, meaning that there isn’t memory held in an HTTP request, and instead that HTTP has Cookies which allow the server to track and read the user’s state. This also keeps track of user connections. AJAX stands for Asynchronous JavaScript and XML. By design, it exchanges small amounts of data with the server under-the-hood, therefore we used a JavaScript function to simultaneously make a GET request to the database to retrieve the number of customers current In store and update the current value of in-store customers on a portion of the view, asynchronously. To do this, a callback function was triggered to increment or decrement the database’s instore value, while also sending back an HTTP Response to reflect that newly updated value on the front-end.

		 To fulfill the webservices portion of the project, the team used Azure to connect a mySQL database for our backend and PythonAnywhere’s web-hosting service to deploy our web-application with SSL encryption. Our use-case of the MySQL relational database was to log customer and business data. This server-side service supports fast writes for customer and business registration and can take the load of many read/writes for entering and leaving the queue.

		The team fulfilled the native client requirement by using the MySQL Workbench client. In Django, the creation of models written in python describe the structure of data reflected in the backend tables. With the commands ``python manage.py makemigrations`` and ``python manage.py migrate``, we were able to translate models written in python to raw SQL data which could be read by the MySQL Workbench Client and be manipulated by user-created queries.

		Customer Lineup’s security is handled by Django’s onboard middleware. Django’s Cross site scripting (XSS) protection leverages Django templating to mitigate these types of attacks. Its Cross site request forgery (CSRF) protection is built into the framework and checks for a secret when POST requests are made. This helps to mitigate malicious users from “replaying” requests made to compromise potentially sensitive information.


Technical details (2) (David)

The way our algorithm works is that first a business needs to sign up for our webapp and enter their business hours. Then the business can tell customers to use our webapp to join the line. New mysql tables (model) were created for customers and business. The customer uses the auth_user table, posts_profile table and posts_customer table. The business uses all of that and an additional table named posts_business. posts_profile is an extension of the auth_user table and allows us to have extra fields such as phone numbers. Posts_business was made to hold the businesses' information which includes the store's address, the store's hours of operations, and store's phone number.

After the user signs up for an account, they are automatically authenticated and logged in. Once logged in, the user will be redirected to another page. If they are a customer, they will be redirected to "Enter The Line" page where they can find a list of business and be able to go on line for that business. 
	
## If the user is a business
If the user is a business, they are redirected to the "control panel page" where they can see how many people are signed up for their business. If they click on "scheduled" or the number that appears scheduled, they can see a list of users that signed up for their store.

"Scheduled" shows the customers that signed up for their store using our webapp. "In Line" means the user has already been notified that their turn is coming up, they've clicked "I'm near the vicinity" button and they're outside the store in line waiting  to scan their QR code. "In Store" shows a list of people that have already scanned their QR code and are currently shopping in the store. When the customer is ready to leave, the same person who scanned their QR code to let them into the store scans them out. 
## Customer goes on line
When the user leaves the line, it will remove the user from customer_queue. Our algorithm has a variable named total_people_to_email_line which is the number of groups to notify when they're turn is about to come up. For example if total_people_to_email_line = 2, then it will email the first two people on line that their turn is coming up. It will not email people who are ahead of the person that left the line. For an example, if the position numbers are 1,2,3. If the user with position number 2 leaves the line, only the person in position 3 will be emailed, because the person in position 1 has been notified already. 


Technical details (3) (Kasey)
Starting off this project, we all needed to learn all our used languages from scratch. We took a poll of popular programming languages and decided to use Python. Choosing python meant we’d use a web application. After deciding that, we needed to decide a framework. At first our main two picks were React and Express. However, after consulting with our professor, we decided Django would be our best option. Django is a full-stack Python web framework, therefore it provided everything we needed for our web application, we just needed to learn more to figure out how to use them. After a solid week and a half of research, we met up with our gained knowledge and started our Django application. We split the team into two parts Ethan and I at the front-end, and David, Christos and Mengzhen at the backend. We decided to use bootstrap for the design of the front-end and MySQL for the backend. Although the teams were readjusted a bit, our goals were still being accomplished. Everyone in the front-end were required to learn HTML and CSS in order to construct our site a beautiful as we wanted. It took plenty of trial and error, but we decided a purple and white theme, that would remain for the entirety of the project. From having our theme, creating the looks for each page was just a matter of rearranging containers and rows to fulfill our needs. As for the backend, we discovered Django has its own form of tables for the database called Django “model”. Although we had already manually written MySQL tables, we decided it would be best to Django’s models rather than to manually code. The models were fairly easy to implement, so setting up all the models we needed was a breeze. The trouble came when we needed to manipulate or iterate over the tables. We found quite some difficulty learning the limitations and functions of the models. Since it was easy to setup, it was assumed that it would be easy to maneuver as well. With time and research, we found our way around it and from there dealing with models were black and white. 

To create the signup and login pages, we used Django “forms”. With the forms, we were able to label fields, grab and clean data and were able to set if a field was required. From getting this data with request “GET” or “POST”, we were able to create users and authorize them in the backend. Django also has a built-in function that create new users to the database and stores only certain information about the user, so we could not find a way to differentiate a business from a customer. So, we then created models for both businesses and customers that store all necessary information, such as contact information and store information, as well as a Boolean indicator to tell if the user is a business or customer. With this implementation, we were able use one HTML page but display different objects depending on if they were a business or customer. This mainly impacted the home page and profile settings. In addition, we were also able to set limits on what page can be viewed depending on the type of user as well. For example, a customer would not be able to see the ‘control panel’ page, a page to check in and out customers out of a business. This Boolean proved to be helpful in the implementation of the queue system as well. 

Additional functions that are vital to our project are “please_login_view “, “user_must_login” and “login_excluded” which helps to secure the integrity of our website. This first function “please_login_view”, will ask the user to enter their login information if they are trying to access any pages that needs user information. The function, “user_must_login”, requires user to login before they are allowed to go certain pages, else it redirects them to another page, mainly the home page. The function “login_excluded” does the opposite. It requires a user to be logged out to see certain pages, for example, resetting their password. 



Technical details (4)


Technical details (5)



###  Related projects (0.5 pages and only if needed)
###  Conclusions and further work (0.5 pages)
###  References
   >Website, links, citations, etc…


