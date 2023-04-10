import asyncio
import os.path
from asyncio import Future
import aiohttp
import aiofiles
import datetime
import re

timestamp_format = '%Y-%m-%d'


def print_help() -> None:
    def formatter(string: str) -> str:
        return '{:~^120}\n'.format(string)

    header = '{:~^120}\n'.format('HELP')
    delimeter = '{:~^120}\n'.format('')
    print(f'{header}{formatter("The following commands can be performed:")}{delimeter}'
          f'{formatter("get_all - get all posts and write it to the file in folder posts;")}'
          f'{formatter("get_one <id> - get one post by spec. id, if given id is absent do nothing, print warning;")}'
          f'{delimeter}')


async def get_all(session: aiohttp.ClientSession, future: Future) -> None:
    url = 'https://jsonplaceholder.typicode.com/posts'
    async with session.get(url) as response:
        result = await response.json()
        future.set_result(result)


async def write_all(future: Future) -> None:
    time_stamp = datetime.datetime.now().strftime(timestamp_format)
    file_path = '/'.join(['posts', f'all_{time_stamp}.txt'])
    content = await asyncio.ensure_future(future)
    async with aiofiles.open(file_path, 'w') as write_all_file:
        await write_all_file.write('userId|id|title|body\n')
        [await write_all_file.write('{0}|{1}|{2}|{3}\n'.format(row['userId'],
                                                               row['id'],
                                                               row['title'],
                                                               row['body'].replace('\n', ''))) for row in content]


async def get_all_posts_and_write_to_file() -> None:
    app_connector = aiohttp.TCPConnector(ssl=False, limit=100, limit_per_host=25)
    tasks = []
    print('Get all started')
    async with aiohttp.ClientSession(connector=app_connector) as session:
        future_get_all = Future()
        tasks.append(asyncio.create_task(get_all(session, future_get_all)))
        tasks.append(asyncio.create_task(write_all(future_get_all)))
        await asyncio.gather(*tasks)
        await asyncio.sleep(10)
        print('\nGet all finished\n'
              'Please input command to do:')


async def get_one(session: aiohttp.ClientSession, future: Future, id_in: str) -> None:
    url = f'https://jsonplaceholder.typicode.com/posts/{str(id_in)}'
    async with session.get(url) as response:
        result = await response.json()
        future.set_result(result)


async def write_one(future: Future) -> None:
    time_stamp = datetime.datetime.now().strftime(timestamp_format)
    file_path = '/'.join(['posts', f'single_{time_stamp}.txt'])
    content = await asyncio.ensure_future(future)
    async with aiofiles.open(file_path, 'w') as write_all_file:
        await write_all_file.write('userId|id|title|body\n')
        await write_all_file.write('{0}|{1}|{2}|{3}\n'.format(content['userId'],
                                                              content['id'],
                                                              content['title'],
                                                              content['body'].replace('\n', '')))


async def get_one_post_and_write_to_file(id_in: str) -> None:
    app_connector = aiohttp.TCPConnector(ssl=False, limit=100, limit_per_host=25)
    tasks = []
    print('Get single started')
    async with aiohttp.ClientSession(connector=app_connector) as session:
        future_get_one = Future()
        tasks.append(asyncio.create_task(get_one(session, future_get_one, id_in)))
        tasks.append(asyncio.create_task(write_one(future_get_one)))
        await asyncio.gather(*tasks)
        await asyncio.sleep(10)
        print('\nGet single finished\n'
              'Please input command to do:')


async def main(loop: asyncio.AbstractEventLoop) -> None:
    print(type(loop))
    tasks = []
    while True:
        command = await loop.run_in_executor(None, input, '\nPlease input command to do:')
        if command == 'index':
            print(f'Preparing task to fetching all post')
            tasks.append(asyncio.ensure_future(get_all_posts_and_write_to_file(), loop=loop))
        elif bool(re.match('get_one{1}.{1}', command)):
            post_id = command.split(' ')[1]
            if int(post_id) <= 100:
                print(f'Preparing task to fetching post with id: {post_id}')
                tasks.append(asyncio.ensure_future(get_one_post_and_write_to_file(post_id), loop=loop))
            else:
                print(f'You entered number more than 100')
        elif command == 'help':
            print(print_help())
        elif command == 'exit':
            break
        else:
            print('Unknown command entered')


if __name__ == '__main__':
    # Create posts folder in the root if folder is not exists
    if os.path.isdir('posts'):
        pass
    else:
        os.makedirs('posts')
    print('{:~^120}\n'.format('For help input command help'))
    m_loop = asyncio.get_event_loop()
    m_loop.run_until_complete(main(m_loop))
    m_loop.close()
