import click
from click import HelpFormatter


class PalmFormatter(HelpFormatter):
    def write_heading(self, heading):
        heading = click.style(heading, fg="yellow")
        return super().write_heading(heading)

    def write(self, text: str):
        text = click.style(text, fg="yellow")
        self.buffer.append(text)
        breakpoint()
