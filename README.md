# cowsource
![alt tag](https://images.unsplash.com/photo-1446126102442-f6b2b73257fd?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&s=fdc200e9e5d9d25c2029b39701f15e2a)
http://not.deadcows.org

Mooooooo

Software Development Term 1 Final Project

## Description
Cowsource is a food-based app that combines the utility of Yelp with the convenience of Tinder. Users can upload pictures of food they've had at restaurants and share them with their friends. Clicking the picture will bring up information about the food and restaurant/eatery it's from, allowing users to go and purchase it themselves if they so choose. Users will also be able to discover food near them based on location data. 

## Running the project
Make sure Mongodb works on your system
Git clone the repo
pip install -r requirements
python app.py

Or, just use the website specified above.

## Features
Newcomers need to sign up to access the website. Once signed in, the user can view the home page, which has Google Maps with markers of posts that were eaten near the user's location and a marker for the user's location. Therefore, the user needs to allow the access to their coordinates on login. By clicking on the marker, the user can see the restaurant name and a small version of the post image. <br><br>
In the "Find New" section, the user can view all posts on the website. In addition, posts can be searched based on their tags and their names. Each individual post has its own webpage; users can view more info and comment and like the post. Clicking a button will also re-veal who liked the post. Clicking it again will (cow)hide it.
<br><br>
Each user and restaurant has a separate webpage as well. There, a user can view all posts by a user or all posts in a restaurant, respectively.

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

