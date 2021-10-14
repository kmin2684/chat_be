# chat

Distinctiveness and Complexity:

My Chat project is distinct from the other projects in this course because this project's main feature is real-time communication between users and relies on Websocket connections, whereas in previous projects only standard HTTP was utilized. Also, although the previous projects only utilized vanilla Javascript, React library is used for this project. Therefore static files are not included in the Django application anymore. Instead, this project is composed of separate backend and frontend parts. Because this project requires two hosting servers, session based authentication could no longer be used. Instead token based authentication is adopted.

This projects is substantially more complex than previous projects because this project is built using many modern web frameworks (Django-Rest-Framework, Django-Channels, React) and incorporates many features like token-authentication, websocket connection, client-side routing and so on. Also, a separate redis server had to be established to handle websocket communications.

How to run this application:
To run the Django application for backend, libraries listed in the "chat > requirements.txt" file should be installed first, prefereablly using pip installer. For running on the local environment, redis server has to be established. In my case, I used Docker container app to run the redis server at localhost:6379.

To run the React application for the frontend part,

File description:
Django application
chat > chat > asgi.py
This file is required to establish the web server and sets which settings file is to be used for the Django application.

chat > chat_app > models.py
contains Django models to establish data structure

chat > chat_app > model_method.py
includes additional methods to be included within each model class

chat > chat_app > serializers.py.py
contains serializer for registering users

chat > chat_app > url.py
maps different API endpoints with different urls

chat > chat_app > admin.py
registers models so that data can be managed from the Django admin page

chat > chat_app > views.py
specifies which operation should take place

chat > WebSocket > consumers.py
speicifies which opeartion should take place when connection is established using websocket protocol.

chat > WebsCcket > routing.py
transfers Websocket connection to the comsumers.py

chat > Websocket > middleware.py
used to authenticate websocket connection by populating websocket connection to a user based on included authentication token in the url

React application
chat_fe > src > App.js
this file provides the main structure for the frontend part of the app

chat_fe > src > App.css
contains most of the stylings applied on the app

chat_fe > scr > components > \*
smaller sub-components that get imported in the App.js file

chat_fe > scr > icons > \*
svg icons for visuals
