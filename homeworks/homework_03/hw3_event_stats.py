#!/usr/bin/env python
# coding: utf-8

import collections


class TEventStats:
    FIVE_MIN = 300

    def __init__(self):
        # TODO: реализовать метод
        self.user_timestamps = {}

    def register_event(self, user_id, time):
        """
        Этот метод регистрирует событие активности пользователя.
        :param user_id: идентификатор пользователя
        :param time: время (timestamp)
        :return: None
        """
        # TODO: реализовать метод
        if (self.user_timestamps.get(user_id)):
            self.user_timestamps[user_id].append(time)
        else:
            self.user_timestamps[user_id] = [time]

    def query(self, count, time):
        """
        Этот метод отвечает на запросы.
        Возвращает количество пользователей, которые за последние 5 минут
        (на полуинтервале времени (time - 5 min, time]), совершили ровно count действий
        :param count: количество действий
        :param time: время для рассчета интервала
        :return: activity_count: int
        """
        # TODO: реализовать метод
        user_actions = dict.fromkeys(self.user_timestamps.keys(), None)

        for user in self.user_timestamps:

            for timestamp in self.user_timestamps[user]:
                if (time - timestamp <= self.FIVE_MIN and time >= timestamp):
                    if (not user_actions[user]):
                        user_actions[user] = 0
                    user_actions[user] += 1
                elif (time >= timestamp):
                    user_actions[user] = 0

        action_count = [value for value in user_actions.values() if value]

        return collections.deque(action_count).count(count)
