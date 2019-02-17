# wsd2018-project

### 1. Team

* `728010` Sataponn Phutrakul
* `721130` Ekaterina Shmeleva
* `528621` Felipe Gonzalez Carceller


### 2. Goal

The goal is to develop an online game store where *(1)* developers can publish and sell games and view statistics for games and *(2)* players can search for games, purchase games via an online payment system, launch and play games, leave public comments for developers and other players, and view leaderboards for individual games.

### 3. Features

#### 3.1 Basic Features

##### Authentication

**_200 points_**

* Signing in and logging in and out are implemented with the [Django authentication system](https://docs.djangoproject.com/en/2.1/topics/auth/);
* We send a verification link to the email address used to sign up using [console backend](https://docs.djangoproject.com/en/2.1/topics/email/#console-backend) during development and [SendGrid](https://sendgrid.com/) in production. The user must verify the email address before they can access their account.
* We integrated Google sign-in into the app (*see 3.2*).

##### Player Functionalities
**_300 points_**

Players can:
* Search games and filter games by genre and ownership;
![Search](screenshots/Screenshot10.png)
* Purchase games via an online payment system;
* Launch and play games;
* View leaderboards for individual games;
* View their own latest and high scores for individual games;
* Leave public Facebook comments and share games on social media (*see 3.2*).

##### Security
* Players are only able to play games they have purchased: however, we deliberately do not protect against accessing games through their URL as it is not included in the scope of this project;
* Players are not able to publish games;
* Etc.

##### Developer Functionalities
**_200 points_**

Developers can:

* Publish, remove and manage games, including setting and making changes to its URL, description, categories, image and price;
* View sales statistics including _a revenue graph_ (implemented with [FusionCharts](https://www.fusioncharts.com)) and detailed game purchases (pending, canceled, failed, successful).

##### Security
* Developers can only view, modify and access statistics of their own games and are not be able to impersonate other developers;
* Developers cannot play games;
* Etc.

##### Game Interactions
**_200 points_**
* The game runs in the `iframe`. Once it is over, the score is posted from the `iframe` that holds the game to its parent with the `window.postMessage()`. Then, the score is posted to the backend using AJAX. The latest and high personal scores and global high scores are updated accordingly.

##### Quality of Work
**_90 points_**
* We did not comment each and every line because good code should be self-documenting and that is what we were trying to achieve. Yet, we use comments where necessary, e.g. for providing a description for methods.
* In order to allow better modularity, we use separate applications for different models, e.g. `games` for `Game` model, `purposes` for `Purchase` model, etc. All logic, forms, templates, styles are placed in corresponding applications. Furthermore, we have an additional application for RESTful API.
* In order to achieve better code reusability, we use custom `Manager`s and `QuerySet`s for querying games, purchases and results. We also use _template tags_ that can be reused in multiple templates.
* A substantial part of application logic is located in `QuerySet`s, not in views. This applies, for example, to the _search_ and _sales statistics_. The same code is reused between views and RESTful API.
* The UI is mobile-friendly (*see 3.2*). For the UI, we selected a dark theme and an [Anonymous Pro](https://fonts.google.com/specimen/Anonymous+Pro) font which seamed appropriated for an online game store. We also used icons provided by [Font Awesome](https://fontawesome.com/).
* We used [`w3c-validation`](https://atom.io/packages/w3c-validation) package for Atom text editor for validating HTML and CSS files. All features are logically organized and easily accessible.

  ![Logo](screenshots/Screenshot14.png)
* While testing our responsive design, we used both physical mobile devices and Google Chrome developer tools for emulating a variety of screen sizes.
* All modules of the application were tested manually. These tests included _penetration tests_.

##### Non-Functional requirements
**_200 points_**

We mostly communicated using [Telegram](https://telegram.org/) and, additionally, we were meeting in person for a discussion at least once week or more often, if it was required.

We first started working on mandatory features. At each stage, we divided tasks among team members, so that everyone knew what they should work on next. [Trello](https://trello.com) was used to create, define, assign, and track tasks:

![Logo](screenshots/Screenshot15.png)

#### 3.2 Extra Features

##### Save/Load and Resolution Feature
**_100 points_**

* The service supports saving and loading for games with the simple message protocol described in Game Developer Information.
* The service is able to receive additional style settings which are then applied to the iframe

##### 3rd Party Login
**_100 points_**

* Google sign-in is added as an alternative to the standard email registration using [social-auth-app-django](https://github.com/python-social-auth/social-app-django).

##### RESTful API
**_100 points_**

* We implemented an API with [Django REST framework](https://www.django-rest-framework.org/). The API provides the following methods:
  * A public `GET` method for searching games by a keyword and categories;
  * A public `GET` method for retrieving information about a specific game;
  * A public `GET` method for retrieving high scores for individual games;
  * A private `GET` method for retrieving game sale statistics;
  * A private `GET` method for retrieving game sale revenue.
* Private API can only be accessed with a developer API access token.

##### Own game
**_100 points_**

* A simple Breakout game using Javascript;
* Is able to communicate with the service using postMessage. The score is saved once the player loses, the current game progress can be saved and the latest saved game state can be loaded from the server.

##### Social Media Sharing
* We will add [Facebook](https://developers.facebook.com/docs/plugins/share-button/) and [Twitter](https://developer.twitter.com/en/docs/twitter-for-websites/tweet-button/overview.html) share buttons so that users can share a game (including its image, description, and URL) and their high scores.

##### Mobile Friendly
* We will build our application using [Bootstrap](https://getbootstrap.com/docs/3.3/) to support a variety of devices, including smartphones, tablets, and desktops.

##### Facebook Comments
* We will use the [Facebook Comments Plugin](https://developers.facebook.com/docs/plugins/comments/) to let players comment on games.

### 4. Process and Time Schedule

We will mostly communicate using [Telegram](https://telegram.org/) and, additionally, we will meet in person for a discussion at least once week or more often, if required.

We will first start working on mandatory features. At each stage, we will divide tasks among team members, so that everyone knows what they should work on next. [Trello](https://trello.com) will be used to create, define, assign, and track tasks.

* Week 1: Set up a database and build a simple layout. DONE
* Week 2: Implement authentication.
* Weeks 3-4: Basic player and developer functionalities and CSS.
* Week 5: RESTful API.
* Week 6: Social media sharing and Facebook comments.

### 5. Models

First of all, we will [extend](https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model) the existing `User` model using a one-to-one link:

`UserProfile`
* `role`
* `user = models.OneToOneField(User, on_delete=models.CASCADE)`

`Game`
* `title`
* `image`
* `description`
* `price`
* `url`
* `developer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)`
* `categories = models.ManyToManyField(Category, on_delete=models.CASCADE)`

`Purchase`
* `user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)`
* `game = models.ForeignKey(Game, on_delete=models.CASCADE)`
* `timestamp`

`Result`
* `user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)`
* `game = models.ForeignKey(Game, on_delete=models.CASCADE)`
* `score`
* `timestamp`

`Category`
* `title`

### 6. Layout Sketch

We used [Marvel](https://marvelapp.com) to build a simple clickable prototype; it can be found [HERE](https://marvelapp.com/405c5bh) 👈

The thumbnail pictures are taken from [MINICLIP](https://www.miniclip.com/games/en/) and are only used for educational purposes.

![alt text](screenshots/Screenshot1.jpg)

![alt text](screenshots/Screenshot2.jpg)

![alt text](screenshots/Screenshot3.jpg)

### 7. Screenshots

![alt text](screenshots/Screenshot4.png)

![alt text](screenshots/Screenshot8.png)

![alt text](screenshots/Screenshot9.png)


![alt text](screenshots/Screenshot7.png)

![alt text](screenshots/Screenshot5.png)

![alt text](screenshots/Screenshot6.png)
