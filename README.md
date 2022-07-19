# SiteHoster
This is a simple site hoster for a local network made in Python.

## What it does
* Host .html files.
* Host a static site.
* Go in to directories.
* Show images/files.

## How to use
First open up the config.ini file and see if everything is what you want it to be.  

To access the site from your device click on the 192.168 url. If you want to access it from antother device first make sure they are on the same network as you and then let them go to the site starting with 192.168.  
To access this from anywhere on the world, you need to port forward it.  

## How it works
### Urls
All files that are in the base directory can be accesed on the by putting in the name as the url. For example: filename: users.html | url: 127.0.0.1/users.  
An exception for this is if the name of the .html file is index.html then the name of url is just 127.0.0.1/.  

### Directories
Directories work like this. My .html file is located in: Users/myfile.html  
So if you want to access myfile.html you need to go the url: 127.0.0.1/Users/myfile  

Directories also can go into directories and those can go into directories and so on. For example: /users/info/edit/edit.html will make the url users/info/edit/edit.html.  

Any static files in this directory work kind of the same as the urls. Lets say my photo is located in Users/userimg.png so if you want to see the image in the .html file. Just do this: <img scr="Users/userimg.png">.  
