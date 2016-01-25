# cowsource
####crowdsourcing cows
![alt tag](https://images.unsplash.com/photo-1446126102442-f6b2b73257fd?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&s=fdc200e9e5d9d25c2029b39701f15e2a)

http://not.deadcows.org

Mooooooo

Software Development Term 1 Final Project

## Description
Cowsource is a food-based webapp that combines the utility of Yelp with the convenience of Tinder. Upload photos of food, preferably containing beef and/or cow-related products, and browse uploaded pictures. Most importantly, discover all the food near you that you've been missing all these years.

## Running the project
Make sure Mongodb works on your system
Git clone the repo
(in a pythonvirtual environment or not): `pip install -r requirements`
<br>`python app.py`

Or, just use the website specified above.

## Features
Newcomers need to sign up to access the website. Once signed in, the user can view the home page, which has Google Maps with markers of posts that were eaten near the user's location and a marker for the user's location. Therefore, the user needs to allow the access to their coordinates on login. By clicking on the marker, the user can see the restaurant name and a small version of the post image. If you do not see any restaurants nearby, please make a new post for a nearby restaurant. The markers/map are two of the few redeeming qualities here... <br><br>
In the "Find New" section, the user can view all posts on the website. In addition, posts can be searched based on their tags and their names. Each individual post has its own webpage; users can view more info and comment and like the post. Clicking a button will also re-veal who liked the post. Clicking it again will (cow)hide it.
<br><br>
Each user and restaurant has a separate webpage as well. There, a user can view all posts by a user or all posts in a restaurant, respectively.
<br><br>
When making a post, it is advised to use only Yelp restaurants. The autocomplete helps to match to one. Please be patient with it, as it is a bit laggy sometimes. Also, you can only search for restaurants in your city as of now.

## APIs
This website makes use of several APIs. Yelp API is used for identifying each restaurant. To provide posts taken near the user's location, Google Maps and Geolocation APIs are used to display and calculate the distances.

## Implementation
Python/Flask was used for the web application itself, and the webpage routes. MongoDB was used for database systems. On the front end, Javascript was used to interact with Google APIs and more. http://purecss.io/ was used for CSS. Gunicorn was used to implement the web server, and Ngnix was utilized to deal with domain implementation.

## Collaborators
|      **Member**      |               **Github**              |         **Roles**          |
|----------------------|---------------------------------------|----------------------------|
|Dong Shin             | [`@map32`](https://github.com/map32)  |Leader, Middleware, Yelp    |
|Sandy Fang            | [`@snady`](https://github.com/snady)  |Frontend                    |
|Katherine Gershfeld   | [`@kagers`](https://github.com/kagers)|Backend, Google             |

## Demo
See a demonstration of our project here: https://youtu.be/hj8X2BAdIAk

