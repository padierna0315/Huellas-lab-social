import asyncio
from typing import Callable, Awaitable, Dict, Set, Any

class PubSubBroker:
    def __init__(self):
        # topic -> set of subscriber callbacks
        self._subscribers: Dict[str, Set[Callable[[Any], Awaitable[None]]]] = {}

    def subscribe(self, topic: str, callback: Callable[[Any], Awaitable[None]]):
        if topic not in self._subscribers:
            self._subscribers[topic] = set()
        self._subscribers[topic].add(callback)

    def unsubscribe(self, topic: str, callback: Callable[[Any], Awaitable[None]]):
        if topic in self._subscribers:
            self._subscribers[topic].discard(callback)
            if not self._subscribers[topic]:
                del self._subscribers[topic]

    async def publish(self, topic: str, message: Any):
        if topic in self._subscribers:
            callbacks = self._subscribers[topic]
            # Run all callbacks concurrently
            tasks = [callback(message) for callback in callbacks]
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

# Singleton instance for the application
broker = PubSubBroker()