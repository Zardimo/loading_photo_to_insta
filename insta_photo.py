import os
import requests
import urllib3
from instabot import Bot
import argparse


def create_parser():
	parser = argparse.ArgumentParser(
		description='This program dowloading images from any(your write) collection of hubblesite.org'
		'or spacex for your choice')
	parser.add_argument('-c', '--collections', action='store_true')
	parser.add_argument('-i', '--image')
	parser.add_argument('-u', '--upload_image', action='store_true')
	return parser


def dowload_image(image_name, image_url):
    pathfile = os.path.join(os.getcwd(), 'images')
    os.makedirs('images', exist_ok=True)
    response = requests.get(image_url, verify=False)
    with open(os.path.join(pathfile, image_name), 'wb') as image:
        image.write(response.content)


def pull_out_prefix(image_url):
    return os.path.splitext(image_url.split('/')[-1])[1]


def collection_image_spacex():
    lounch_list = requests.get('https://api.spacexdata.com/v3/launches/').json()
    all_lounch = {}
    for lounch in lounch_list:
        if len(lounch['links']['flickr_images'])>1:
            all_lounch.update({lounch['mission_name'] : lounch['links']['flickr_images']})
    return all_lounch

def dowload_spacex_image(all_lounch, libriary):
    try:
        for image_num, image_url in enumerate(all_lounch[libriary]): 
            image_name = f'spacex_{libriary}_{image_num}{pull_out_prefix(image_url)}'
            print(f'Download {image_name}\n.....')
            dowload_image(image_name, image_url)
    except KeyError:
        exit('Неверно указана библиотека')


def collection_image_hubble():
    url = 'http://hubblesite.org/api/v3/images/all'
    params = {
        'page' : 'all'
    }
    response = requests.get(url, params)
    return list(set([image['collection'] for image in response.json()]))


def get_collection_id_list(collection):
    url_id = 'http://hubblesite.org/api/v3/images/'
    response = requests.get(f'{url_id}{collection}').json()
    return list(image['id'] for image in response)


def dowload_hubble_image(collection):
    url_image = 'http://hubblesite.org/api/v3/image/'
    extensions = ['.png', '.jpg', '.jpeg', 'pdf']
    for id in get_collection_id_list(collection):
        response = requests.get(f'{url_image}{id}').json()
        images = list(image['file_url'] for image in response['image_files'])
        final_url = (f'http:{images[-1]}')
        prefix = pull_out_prefix(final_url)
        image_name = f'{collection}_{id}{prefix}'
        if os.path.splitext(image_name)[1].lower() in extensions:
            print(f'download {image_name} ....')
            dowload_image(image_name, final_url)


def insta_bot(path, image_name):
    bot = Bot()
    bot.login(username='insta_bot_spacex_hubble', password='123321csk', proxy=None)
    write_name = os.path.splitext(image_name)[0]
    bot.upload_photo(path, write_name)


def get_image_list_from_path(path):
    image_list = []
    extensions = ['.png', '.jpg', '.jpeg', 'pdf']
    for image in os.listdir(path):
        if os.path.splitext(image)[1].lower() in extensions:
            image_list.append(image)
    return(image_list)


if __name__ == '__main__':
    urllib3.disable_warnings()
    path = os.path.join(os.getcwd(), 'images')
    parser = create_parser()
    args_namespace = parser.parse_args()
    if args_namespace.collections:
    	print('hubble collections:')
    	for collection in collection_image_hubble():
    		print(collection)
    	print('\nspacex libriary:')
    	for libriary in collection_image_spacex().keys():
    		print(libriary)
    elif args_namespace.image in collection_image_spacex():
        dowload_spacex_image(collection_image_spacex(), args_namespace.image)
    elif args_namespace.image in collection_image_hubble():
        dowload_hubble_image(args_namespace.image)
    elif args_namespace.upload_image:
    	for image in  get_image_list_from_path(path):
        	insta_bot(os.path.join(path, image), image)
    else:
    	print('Incorrect collection')