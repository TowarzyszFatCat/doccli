# Version: 1.0.5
"""

> Cloudzik <
Interactive-Python-Menu
1.0.5
16.11.2023
https://github.com/Cloudzik1337/Interactive-Python-Menu


Changelog:
1.0.5
This version strongly focuses on optimization and code readability.
1.0.4 pylint rating was 7.5/10 now in 1.0.5 its 9.79/10
------------------------------------------------------------------
Your code has been rated at 9.78/10 (previous run: 7.48/10, +2.30)
------------------------------------------------------------------
"""

# Import necessary libraries
import os
import keyboard
from pystyle import Center


# Class definition for the menu colors
class _Colors:
    """Menu colors"""

    @staticmethod
    def _color_code(code):
        """Static method to format color codes"""
        return f'\033[{code}m'

    ENDC: str = _color_code(0)
    BOLD: str = _color_code(1)
    UNDERLINE: str = _color_code(4)
    BLACK: str = _color_code(30)
    RED: str = _color_code(31)
    GREEN: str = _color_code(32)
    YELLOW: str = _color_code(33)
    BLUE: str = _color_code(34)
    MAGENTA: str = _color_code(35)
    CYAN: str = _color_code(36)
    WHITE: str = _color_code(37)
    REDBG: str = _color_code(41)
    GREENBG: str = _color_code(42)
    YELLOWBG: str = _color_code(43)
    BLUEBG: str = _color_code(44)
    MAGENTABG: str = _color_code(45)
    CYANBG: str = _color_code(46)
    WHITEBG: str = _color_code(47)
    GREY: str = _color_code(90)
    REDGREY: str = _color_code(91)
    GREENGREY: str = _color_code(92)
    YELLOWGREY: str = _color_code(93)
    BLUEGREY: str = _color_code(94)
    MAGENTAGREY: str = _color_code(95)
    CYANGREY: str = _color_code(96)
    WHITEGREY: str = _color_code(97)
    GREYBG: str = _color_code(100)
    REDGREYBG: str = _color_code(101)
    GREENGREYBG: str = _color_code(102)
    YELLOWGREYBG: str = _color_code(103)
    BLUEGREYBG: str = _color_code(104)
    MAGENTAGREYBG: str = _color_code(105)
    CYANGREYBG: str = _color_code(106)
    WHITEGREYBG: str = _color_code(107)


# Class definition for the menu styles
class _Styles:
    """Menu styles"""
    DEFAULT: int = 1
    SELECTED: int = 2
    ARROW: int = 3
    CENTERED: int = 11
    CENTEREDSELECTED: int = 22
    ARROWCENTERED: int = 33


# Create instances of the classes
Colors = _Colors()
Styles = _Styles()


# Class definition for the menu system
class Menu:
    """Menu system"""

    def __init__(self,
                 options: list = None,
                 color: str = Colors.CYAN,
                 style: int = Styles.DEFAULT,
                 pretext: str = None):  # Use ANSI escape code for color
        """

        :options: list of menu options format: ["Option 1", "Option 2", "Option 3"]
        :color: ANSI escape code for color format: Colors.CYAN
        :style: menu style format: Styles.DEFAULT or Styles.SELECTED
        or Styles.CENTERED or Styles.CENTEREDSELECTED
        :pretext: text to display before the menu otherwise it will earesed
        To get the selected option, use menu.selected or menu.selected_index


        Example:
        import menu
        options = ["Option 1", "Option 2", "Option 3"]
        my_menu = menu.Menu(options=options, style=menu.Styles.SELECTED)
        User_choice = my_menu.launch(response="String") # can be "String" or "Index"
        # There are two ways to get the selected option
        # 1. Get the index of the selected option
        print(my_menu.selected_index)
        # 2. Get the string of the selected option
        print(my_menu.selected)
        # also you can get the index or string by using the variable User_choice
        print(User_choice) # change response to "Index" or "String" to get the index or string
        """
        self.pretext = str(pretext)
        self.style = style
        self.options = options
        self.color = color
        self.index = 0
        if options is not None:
            self.index_max = len(options)
        self.selected = None
        self.json = {}
        self.selected_index = None
        self.last_known_index = 1

    def launch(self, response: str = "String"):

        """Launch the menu
        :response: Let user decide if menu should return index or string"""
        return self._create_menu(response)

    def _create_menu(self, response: str = "String"):
        # Create a dictionary mapping index to menu options
        for index, option in enumerate(self.options):
            self.json[index] = option

        # Set up hotkeys for navigation
        keyboard.add_hotkey('up', self._up, suppress=True)
        keyboard.add_hotkey('down', self._down, suppress=True)
        keyboard.add_hotkey('enter', self._enter, suppress=True)
        keyboard.add_hotkey('right', self._enter, suppress=True)

        # Display the menu and wait for user input
        self._display()

        # Unhook all hotkeys after menu display
        keyboard.unhook_all()
        if response == "String":
            return self.selected
        return self.selected_index

    def _up(self):
        # Move the selection index up
        self.index = (self.index - 1) % self.index_max

    def _down(self):
        # Move the selection index down
        self.index = (self.index + 1) % self.index_max

    def _enter(self):
        # Set the selected option based on the current index
        self.selected = self.index

    def _style_parse_non_center(self):
        """ Parse the style and display the menu
        1 = default,
        2 = > option < style
        3 = ↳ option style
        11 = 1 but with a centered title
        22 = 2 but with a centered title
        33 = 3 but with a centered title
        """
        # This if statement chain determines the style of the menu
        if self.style == 1:
            for i in range(self.index_max):
                if i == self.index:
                    print(self.color + self.json[i] + Colors.ENDC)
                else:
                    print(self.json[i])
        elif self.style == 2:
            for i in range(self.index_max):
                if i == self.index:
                    print(self.color + "> " + self.json[i] + " <" + Colors.ENDC)
                else:
                    print(self.json[i])
        elif self.style == 3:
            for i in range(self.index_max):
                if i == self.index:
                    print(self.color + "↳ " + self.json[i] + Colors.ENDC)
                else:
                    print(self.json[i])

    def _style_parse_center(self):
        """ Parse the style and display the menu"""
        equaling_space = "         "
        if self.style == 11:
            for i in range(self.index_max):
                if i == self.index:
                    sep = equaling_space
                    print(Center.XCenter(self.color + sep + self.json[i] + Colors.ENDC))
                else:
                    print(Center.XCenter(self.json[i]))
        if self.style == 22:
            for i in range(self.index_max):
                if i == self.index:
                    # blank space for centering
                    sep = equaling_space + "> "
                    print(Center.XCenter(self.color + sep + self.json[i] + " <" + Colors.ENDC))
                else:
                    print(Center.XCenter(self.json[i]))
        if self.style == 33:
            for i in range(self.index_max):
                if i == self.index:
                    sep = equaling_space + "↳ "
                    print(Center.XCenter(self.color + sep + self.json[i] + Colors.ENDC))
                else:
                    print(Center.XCenter(self.json[i]))

    def _display(self):
        # Initialize index and selected values
        self.index = 0
        self.selected = None

        # Display the menu options with highlighting for the selected option
        while self.selected is None:
            if self.last_known_index != self.index:
                # Update the screen with the current menu state
                self.last_known_index = self.index
                self.cls()
                if self.pretext is not None:
                    if self.style in [11, 22, 33]:
                        print(Center.XCenter(self.pretext))
                        self._style_parse_center()
                    else:
                        print(self.pretext)
                        self._style_parse_non_center()
        # Set the selected value to the corresponding menu option
        self.selected = self.json[self.selected]
        self.selected_index = self.index

    def show_example(self):
        """Show an example of each menu style"""
        for example_style in [1, 2, 3, 11, 22, 33]:
            options = ["Option 1", "Option 2", "Option 3"]
            Menu(options=options, style=example_style).launch()

    @staticmethod
    def cls():
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'printf "\033c"')
