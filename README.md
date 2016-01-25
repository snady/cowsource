# cowsource
![alt tag](https://images.unsplash.com/photo-1446126102442-f6b2b73257fd?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&s=fdc200e9e5d9d25c2029b39701f15e2a)
Mooooooo

Software Development Term 1 Final Project

## Description
Cowsource is a food-based app that combines the utility of Yelp with the convenience of Tinder. Users can upload pictures of food they've had at restaurants and share them with their friends. Clicking the picture will bring up information about the food and restaurant/eatery it's from, allowing users to go and purchase it themselves if they so choose. Users will also be able to discover food near them based on location data, and establish preferences for restaurants and food. 

## Features
Newcomers need to sign up to access the website. Once signed, the user can view the home page, which has a Google maps with markers of posts that were taken nearby the user's location. Therefore, the user needs to allow the access to their coordinates. In the "Find New" section, one can view the list of all posts on the website. In addition, posts can be searched based on their tags and their names. Each individual post has its own webpage; users can comment and like the post. Each user and restaurant has its own webpage as well. 

## APIs
This website makes use of several APIs. Yelp API is used for identifying each restaurant. To provide posts taken nearby the user's location, Google Maps and Geolocation APIs are used to display and calculate the distances.

## Collaborators
|   **Member**         |            **Role**            |
|----------------------|--------------------------------|
|Dong Shin             | Leader                         |
|Sandy Fang            | UX/JS                          |
|Katherine Gershfeld   | Database                       |



## Deadlines
+ 1/11 Login on all ends, Yelp API stuff name-id-display address
+ 1/12 Make post, Display post, dynamic dropdown 
+ 1/13 Basic functioning app
+ 1/14 User pages, Restaurant pages, Comments
+ 1/15 
##Database design
+ Users: ID Name Password
+ Comments: ID text userid postid
+ Posts: ID pic date userid restid location likes info tags
