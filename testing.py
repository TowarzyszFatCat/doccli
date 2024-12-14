from InquirerPy import inquirer
from termcolor import colored
from rich import print
from rich.layout import Layout
from rich.console import Console


import utils
import modules

layout = Layout()
layout.split_row(Layout(name="Info"), Layout(name="Menu"))

print(layout)


print(utils.doccli_logo_centered())
print(utils.service_statuses())
utils.fuzzy_menu(message=utils.doccli_logo_centered())

