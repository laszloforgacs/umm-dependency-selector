import asyncio
from typing import Callable


class NavigationController:
    _stack: list['Screen'] = []

    async def navigate_back(self) -> 'Screen':
        if len(self._stack) > 0:
            popped_screen = self._stack.pop()
            popped_screen.on_destroy()
            screen_to_navigate_to = self._stack[-1]
            await self._navigate_up(screen_to_navigate_to)

    async def navigate_to(self, provide_screen: Callable[[None], 'Screen']):
        if len(self._stack) > 0:
            self._stack[-1].on_destroy()
        screen = provide_screen()
        self._stack.append(screen)
        await screen.on_created()

    async def _navigate_up(self, screen: 'Screen'):
        await screen.on_created()

