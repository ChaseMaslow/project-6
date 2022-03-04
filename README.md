# UOCIS322 - Project 6 #

#### Description
This is a Flask-RESTful app designed to replace the [ACP Brevet Control calculator](https://rusa.org/octime_acp.html) found on the Randonneurs USA official website. The web page responds to user input live, with no redirects or refreshes. The calculator accepts miles or kilometers, and does conversions automatically. Data can be stored and retrieved by the user from a MongoDB database, accessed using the API server.

### How it Works
The algorithm used here is based on the information on the Randonneurs USA website, and what their calculator spits out. They have an informational page about that [here](https://rusa.org/pages/acp-brevet-control-times-calculator). On that page, there's a table of minimum and maximum speeds for different locations.

* To calculate a control's opening time, we use the maximum speed of every range preceding its location, summing together the expected traversal time for someone moving at maximum speed. For the closing time, we use just the minimum speed of the bracket the control falls within.
	* For example: A control at 550km opens at 200/34 + 200/32 + 150/30 = 17H08, and closes at 550/15 = 36H40.

My program has an internal copy of this table, with an additional bracket added to account for the more recent rule that relaxes closing times within the first 60km. For such controls, the minimum speed is treated as 20km/hr, and one hour is added to the time.

The table in the webpage is operated by a Javascript (+JQuery) front-end, while the algorithm is contained in the Python (+Flask) back-end. The Flask app sends requests to a Flask-RESTful API service whenever the user clicks the Submit or Display buttons, and the API takes care of all interactions with the database. The database is a MongoDB server.

##### Modules Used
* Flask, Flask-RESTful, Requests, Arrow, MongoEngine, PyMongo, Nose (testing)
* JQuery, Moment

##### Authors & Author Info
* Chase Maslow - chasemaslow@gmail.com
* Ali Hassani (API code)

## How to start

#### Docker
Go into your terminal or shell and navigate to the main directory. With Docker installed, enter:

	`docker-compose up -d`

Wait for it to finish. Now if you go to "http://localhost:5000" (default) in your web browser, you should see the webpage.

#### Web App
You should see a webpage titled "ACP Brevet Times" and a table with the columns "Miles", "Km", "Location", and so on.

When you input a distance into "Miles" or "Km", the app should automatically fill the other column, and calculate the opening and closing times. You can change the total brevet distance with the dropdown menu to the upper left, and the beginning date and time with the menu to the upper right.

* Remember that when typing in input fields, you'll have to click somewhere on the page or press enter to get a response.

It is intended that inputted control distances be within the brevet distance selected, and in ascending order. If you input control distances greater than the brevet distance, or give a control a distance that is lower than that of the control immediately before it, the app will show you non-disruptive "error" messages under the "notes" column.

At the bottom of the table, there are two buttons labelled "Submit" and "Display". Click the Submit button to save your data, including distances, locations, and times. This will also clear all fields. Click the Display button to get back what you last saved.
