# DESCRIPTION
This three scripts provide functioanlity to automate fetching images from hubblesite.org, spacex and uploading them to your instagramm account. Each script locates in its own file.
# HOW TO INSTALL
Python has to be installed on your system. Use pip (or pip3 if there is conflict with Python 2) to install dependences.
```
pip install -r requirements.txt
```
It is recommended to use virtual environment virtualenv/venv to isolate your project.

# QUICKSTART

This script provides simple console interface. In case you dont know wich collection to choose you can run script with -c argument, as can be seen below:
```
$python ./insta_photo.py -c
```
When you choose distinct collection, you want to fetch - run script whith -i argument and collection name after space:

```
$python ./insta_photo.py -i CRS-16
```
In case you make a mistake in collection's name - you'll recieve a message.

```
Incorrect collection
```

## Load local images to your instagramm account
All images from folder `./image` upload to your instagramm account. Login and password must be stored in .env file in your project folder.

```
$python insta_photo.py -u
```

# PROJECT GOALS
Project was created for educational purposes. Training course for web-developers - [dvmn.org](https://dvmn.org)
