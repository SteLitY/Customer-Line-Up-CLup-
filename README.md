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

		 To fulfill the webservices portion of the project, the team used azure to connect a mySQL database for our backend. Our use-case of this relational database is to log customer and business data. This server-side service supports fast writes for customer and business registration and can take the load of many read/writes for entering and leaving the queue.
		    -   Include your API documentation in an appendix.
        -   How did you fulfill the multiple native client requirements?
        -   How did you fulfill the security requirements of the project?
*  Related projects (0.5 pages and only if needed)
*   Conclusions and further work (0.5 pages)

*  References
   >Website, links, citations, etc…


