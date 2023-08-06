import webbrowser

from rich.text import Text
from textual import events
from textual.app import App
from textual.widget import Widget
from textual.widgets import Footer

LINKS = [
    ("home", "https://waylonwalker.com/"),
    ("blog", "https://waylonwalker.com/archive/"),
    ("YouTube", "https://youtube.com/waylonwalker"),
    ("Twitch", "https://www.twitch.tv/waylonwalker"),
    ("Twitter", "https://twitter.com/_waylonwalker"),
    ("Dev.to", "https://dev.to/waylonwalker"),
    ("LinkedIn", "https://www.linkedin.com/in/waylonwalker/"),
]


class Link(Widget):
    def __init__(self, label, url):
        self.label = label
        self.name = label
        self.url = url
        self.is_selected = False
        super().__init__()

    def render(self):
        return Text.assemble(
            (self.label, ("black on #c122ac" if self.is_selected else "")),
            (" ", ("black on #c122ac" if self.is_selected else "")),
            (self.url, ("white on #c122ac" if self.is_selected else "#c122ac")),
        )


class WaylonWalker(App):
    async def on_load(self, event: events.Load) -> None:
        await self.bind("ctrl+c", "quit", show=False)
        await self.bind("g", "submit", show=False)
        await self.bind("q", "quit", "Quit")
        await self.bind("j", "next", "Next")
        await self.bind("k", "previous", "Previous")
        await self.bind("enter", "open", "Open")

    async def action_open(self) -> None:

        webbrowser.open(self.links[self.selected].url)

    async def on_mount(self, event: events.Mount) -> None:

        self.selected = 0
        self.links = [Link(*link) for link in LINKS]
        self.links[self.selected].is_selected = True

        footer = Footer()
        await self.view.dock(*self.links, footer)

        self.view.refresh()

    async def action_next(self) -> None:
        self.links[self.selected].is_selected = False
        self.links[self.selected].refresh()
        self.selected = self.selected + 1
        self.links[self.selected].is_selected = True
        self.links[self.selected].refresh()

    async def action_previous(self) -> None:
        self.links[self.selected].is_selected = False
        self.links[self.selected].refresh()
        self.selected = self.selected - 1
        self.links[self.selected].is_selected = True
        self.links[self.selected].refresh()


if __name__ == "__main__":

    WaylonWalker.run(title="Waylon Walker")
