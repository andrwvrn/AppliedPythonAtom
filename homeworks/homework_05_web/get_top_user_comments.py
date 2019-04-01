import re
import csv
from bs4 import BeautifulSoup
from collections import OrderedDict

import asyncio
import aiohttp


async def get_html(link: str, q: asyncio.Queue) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as response:
            if (response is not None):
                await q.put((link, await response.text()))


async def process_html(q: asyncio.Queue) -> tuple:
    link, text = await q.get()
    html = BeautifulSoup(text, 'html.parser')
    list_of_users = [re.sub(r'<.+?>', '', str(user)) for user in html.findAll('span',
                     attrs={'class': 'user-info__nickname_comment'})]
    comment_dict = dict.fromkeys(list_of_users, None)
    for user in comment_dict:
        comment_dict[user] = list_of_users.count(user)

    q.task_done()
    return (link, OrderedDict(sorted(comment_dict.items(), key=lambda kv: kv[1], reverse=True)))


def write_to_csv(filename: str, res: list) -> None:
    with open(filename, 'w') as f:
        fieldnames = ['link', 'username', 'count_comment']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for article in res:
            for user in article[1]:
                writer.writerow({'link': article[0], 'username': user,
                                 'count_comment': article[1][user]})


async def main(filename: str, links: list) -> None:
    q = asyncio.Queue()
    html_getters = [asyncio.create_task(get_html(link, q)) for link in links]
    html_processors = [asyncio.create_task(process_html(q)) for _ in range(len(links))]
    res = await asyncio.gather(*html_processors)
    res = sorted(res, key=lambda link_dict: sum(link_dict[1].values()), reverse=True)
    write_to_csv(filename, res)


if __name__ == '__main__':
    import sys

    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    asyncio.run(main(filename, links))
