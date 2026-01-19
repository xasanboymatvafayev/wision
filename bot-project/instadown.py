import instaloader
import os

loader = instaloader.Instaloader()

def download_instagram_post(url):
    shortcode = url.split('/')[-2]
    post = instaloader.Post.from_shortcode(loader.context, shortcode)
    loader.download_post(post, target="instadown")

def clean_download_folder():
    for file in os.listdir('instadown'):
        os.remove(f'instadown/{file}')
    os.rmdir('instadown')