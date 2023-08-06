from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, Dict, List

from typing import Union, Callable, Optional
from deanerfi.common import log


@dataclass
class Event:
    name: str


@dataclass
class Command:
    name: str


Message = Union[Event, Command]

EventHandler = Callable[[Event], Optional[List[Message]]]
CommandHandler = Callable[[Command], Optional[List[Message]]]


class MessageBus(ABC):
    def __init__(self, event_handlers: Dict[Type[Event], List[EventHandler]] = None,
                 command_handlers: Dict[Type[Command], CommandHandler] = None, **kwargs) -> None:
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    @abstractmethod
    def send_msg(self, msg: Message) -> None:
        raise NotImplementedError

    def send_msgs(self, msgs: List[Message]) -> None:
        raise NotImplementedError

    @abstractmethod
    def process_msgs(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle(self, msg: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_command(self, command: Command) -> None:
        raise NotImplementedError


class LocalMessageBus(MessageBus):

    def __init__(self, event_handlers: Dict[Type[Event], List[EventHandler]] = None,
                 command_handlers: Dict[Type[Command], CommandHandler] = None, **kwargs) -> None:
        super().__init__(event_handlers, command_handlers)
        self.msg_queue: List[Message] = []

    def send_msg(self, msg: Message) -> None:
        self.msg_queue.append(msg)

    def send_msgs(self, msgs: List[Message]) -> None:
        [self.msg_queue.append(msg) for msg in msgs]

    def process_msgs(self) -> None:
        while self.msg_queue:
            self.handle(self.msg_queue.pop(0))

    def handle(self, msg: Message) -> None:
        if isinstance(msg, Event):
            self.handle_event(msg)
        if isinstance(msg, Command):
            self.handle_command(msg)

    def handle_event(self, event: Event) -> None:
        log.api.info(__name__, 'handling event', data=event)

    def handle_command(self, command: Command) -> None:
        log.api.info(__name__, 'handling command', data=command)
        cmd_handler = self.command_handlers.get(type(command))
        if cmd_handler:
            return_msgs = cmd_handler(command)
            self.send_msgs(return_msgs)

