#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class CacheComponent(ABC):
    @abstractmethod
    def is_enabled(self):
        raise NotImplementedError

    @abstractmethod
    def set(self, key, value):
        raise NotImplementedError

    @abstractmethod
    def get(self, key):
        raise NotImplementedError

    @abstractmethod
    def delete(self, key):
        raise NotImplementedError

    @abstractmethod
    def expire(self, key, seconds):
        raise NotImplementedError

    @abstractmethod
    def get_ttl(self, key):
        raise NotImplementedError
