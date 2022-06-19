# SiteHoster
## Does not yet work with directories
This is a simple site hoster for a local network made in Python.

## How to use
First open up the config.ini file and see if everything is what you want it to be.  
If you are using any static files like photo's and such make sure to put /static/ on the start of the file location.
After that install flask using the command line. And run the main.py file.  

To access the site from your device click any of the 2 links. But if you want to access it from antother device first make sure they are on the same network as you and then let them go to the site starting with 192.168  

## How it works
### Urls
All files that are in the base directory can be accesed on the by putting in the name as the url. For example: filename: users.html | url: 127.0.0.1/users.  
An exception for this is if the name of the html file is index.html then the name of url is just 127.0.0.1/.  

### Directories
Directories work like this. My .html file is located in: Users/myfile.html  
So if you want to access myfile.html you need to go the url: 127.0.0.1/Users/myfile  

Any static files in this directory work kind of the same as the urls. Lets say my photo is located in Users/userimg.png so if you want to see the image in the .html file. Just do this: <img scr="static/Users/userimg.png">. It just needs a static/ at the beginning of the file location 
