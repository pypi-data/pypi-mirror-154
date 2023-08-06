from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import (
	Protocol, 
	Callable,
	Dict,
	List
)

Callback = Callable[[dict], None]


class Subscriber(Protocol):

	def subscribe_handler(self, payload: dict, callback: Callback = None):
		...


class SubscriberAbstract(ABC):

	@abstractmethod
	def subscribe_handler(self, payload: dict, callback: Callback = None):
		raise NotImplementedError


@dataclass
class Channel:

	name: str

	def __post_init__(self):
		self.name = self.name.upper()

	@staticmethod
	def with_name(name: str)-> Channel:
		return Channel(name)

	def get_name(self)-> str:
		return self.name


class PubSubProtocol(Protocol):

	def create_channel(self, channel: Channel)-> None:
		...

	def subscribe(self, channel: Channel, subscriber: Subscriber)-> None:
		...

	def publish(self, channel: Channel, payload: dict, callback: Callback = None)-> None:
		...


class PubSub:

	channels: Dict[str, List[Subscriber]] = {}

	def create_channel(self, channel: Channel)-> None:
		if self.__channel_exists(channel):
			return

		self.channels[channel.get_name()] = []

	def subscribe(self, channel: Channel, subscriber: Subscriber)-> None:
		if not self.__channel_exists(channel):
			return

		self.channels[channel.get_name()].append(subscriber)

	def publish(self, channel: Channel, payload: dict, callback: Callback = None)-> None:
		if not self.__channel_exists(channel):
			return

		for sub in self.channels[channel.get_name()]:
			sub.subscribe_handler(payload, callback)

	def __channel_exists(self, channel: Channel)-> bool:
		if channel.get_name() in self.channels:
			return True

		return False