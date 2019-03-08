#!/usr/bin/env python
# coding: utf-8


from homeworks.homework_02.heap import MaxHeap
from homeworks.homework_02.fastmerger import FastSortedListMerger


class VKPoster:

    def __init__(self):
        self._posted_posts = {}
        self._read_posts = {}
        self._followed_for = {}
        self._recent_posts = {}
        self._popularity = {}

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
        self._recent_posts[user_id] = []

        for user in self._followed_for[user_id]:
            if (self._posted_posts.get(user)):
                self._recent_posts[user_id] += self._posted_posts[user]
        self._recent_posts[user_id] = sorted(self._recent_posts[user_id])[::-1]
        return self._recent_posts[user_id][:k]

    def get_most_popular_posts(self, k: int) -> list:
        '''
        Метод который возвращает список k самых популярных постов за все время,
        остортированных по свежести.
        :param k: Сколько самых свежих популярных постов
        необходимо вывести. Число.
        :return: Список из post_id размером К из популярных постов. list
        '''
        self._popularity = {}
        for user_id in self._read_posts:
            for post_id in self._read_posts[user_id]:
                if (post_id in self._popularity):
                    self._popularity[post_id] += 1
                else:
                    self._popularity[post_id] = 1

        sorted_posts = sorted(self._popularity.items(),
                              key=lambda id_and_pop:
                              (id_and_pop[1], id_and_pop[0]))

        return [post[0] for post in sorted_posts[::-1][:k]]
