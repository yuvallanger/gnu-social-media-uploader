#!/usr/bin/env python3

import pathlib
import random
import logging
import getpass
import sys

import gnusocial as gs
import gnusocial.media
import gnusocial.statuses


logging.basicConfig(level=logging.DEBUG)

SERVER_URL = 'https://shitposter.club'
USERNAME = 'cow2001'
PASSWORD = ''

SOURCE_IMAGE_DIRECTORY = pathlib.Path('source_directory').absolute()
SINK_IMAGE_DIRECTORY = pathlib.Path('sink_directory').absolute()

STATUS = "An image."


def get_random_image_path(source_image_directory):
    return random.choice(list(source_image_directory.glob('*'))).absolute()


def upload_image(image_absolute_path,
                 server_url,
                 username,
                 password,
):
    with image_absolute_path.open('rb') as image_file:
        return gs.media.upload(server_url=server_url,
                               media=image_file,
                               username=username,
                               password=password,
        )


def move_image(image_path,
               sink_image_directory,
):
    image_path.rename(sink_image_directory.joinpath(image_path.name))


def update_status(#image_absolute_path,
                  server_url,
                  status,
                  username,
                  password,
                  media_ids
):
    result = gs.statuses.update(server_url=server_url,
                                username=username,
                                password=password,
                                status=status,
                                media_ids=media_ids,
    )
    return result


def main(server_url,
         username,
         password,
         source_image_directory,
         sink_image_directory,
         status,
):
    random_image_absolute_path = get_random_image_path(source_image_directory)
    upload_response = upload_image(image_absolute_path=random_image_absolute_path,
                                   server_url=server_url,
                                   username=username,
                                   password=password,
    )
    
    media_ids = [upload_response['media_id']]

    update_status_response = update_status(
        server_url=server_url,
        status=status,
        username=username,
        password=password,
        media_ids=media_ids,
    )
    
    logging.debug(str(update_status_response))
    
    move_image(random_image_absolute_path,
               sink_image_directory=sink_image_directory)


if __name__ == '__main__':
    actual_password = PASSWORD if PASSWORD != '' else getpass.getpass()

    main(server_url=SERVER_URL,
         username=USERNAME,
         password=actual_password,
         sink_image_directory=SINK_IMAGE_DIRECTORY,
         source_image_directory=SOURCE_IMAGE_DIRECTORY,
         status=STATUS
    )
