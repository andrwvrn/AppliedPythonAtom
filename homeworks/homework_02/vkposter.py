#!/usr/bin/env python
# coding: utf-8


from homeworks.homework_02.heap import MaxHeap
from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    def __init__(self):
        self._posted_posts = {}
        self._read_posts = {}
        self._followed_for = {}

    def user_posted_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        выложил пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if (self._posted_posts.get(user_id)):
            self._posted_posts[user_id].append(post_id)
        else:
            self._posted_posts[user_id] = [post_id]

    def user_read_post(self, user_id: int, post_id: int):
        '''
        Метод который вызывается когда пользователь user_id
        прочитал пост post_id.
        :param user_id: id пользователя. Число.
        :param post_id: id поста. Число.
        :return: ничего
        '''
        if (self._read_posts.get(user_id) and post_id
                not in self._read_posts.get(user_id)):
            self._read_posts[user_id].append(post_id)
        elif (not self._read_posts.get(user_id)):
            self._read_posts[user_id] = [post_id]

    def user_follow_for(self, follower_user_id: int, followee_user_id: int):
        '''
        Метод который вызывается когда пользователь follower_user_id
        подписался на пользователя followee_user_id.
        :param follower_user_id: id пользователя. Число.
        :param followee_user_id: id пользователя. Число.
        :return: ничего
        '''
        if (self._followed_for.get(follower_user_id)):
            self._followed_for[follower_user_id].append(followee_user_id)
        else:
            self._followed_for[follower_user_id] = [followee_user_id]

    def get_recent_posts(self, user_id: int, k: int)-> list:
        '''
        Метод который вызывается когда пользователь user_id
        запрашивает k свежих постов людей на которых он подписан.
        :param user_id: id пользователя. Число.
        :param k: Сколько самых свежих постов необходимо вывести. Число.
        :return: Список из post_id размером К из свежих постов в
        ленте пользователя. list
        '''
        recent_posts = []

        for followee in self._followed_for[user_id]:
            if (self._posted_posts.get(followee)):
                recent_posts.append(sorted(self._posted_posts[followee]))

        return FastSortedListMerger.merge_first_k(recent_posts, k)

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        popularity = {}
        for user_id in self._read_posts:
            for post_id in self._read_posts[user_id]:
                if (post_id in popularity):
                    popularity[post_id] += 1
                else:
                    popularity[post_id] = 1

        pop_and_recent = [(value, key) for (key, value) in popularity.items()]

        pop_heap = MaxHeap(pop_and_recent)
        popular_posts = []
        for i in range(k):
            if (len(pop_heap._heap) != 0):
                popular_posts.append(pop_heap.extract_maximum())
            else:
                break
        return [post[1] for post in popular_posts]
