from typing import Callable


class NavigationController:
    _stack: list['Screen'] = []

    def navigate_back(self):
        if len(self._stack) > 1:
            popped_screen = self._stack.pop()
            popped_screen.on_destroy()
            screen_to_navigate_to = self._stack[-1]
            self.navigate_to(screen_to_navigate_to)

    def navigate_to(self, provide_screen: Callable[[None], 'Screen']):
        screen = provide_screen()
        screen.on_created()
        self._stack.append(screen)
