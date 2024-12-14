from InquirerPy import inquirer

def fuzzy_menu(message='message', choices=['test', 'test'], pointer='❯', style=None, vi_mode=False, qmark='', amark='?', instruction='instruction', long_instruction='long_instruction', multiselect=False, prompt='Szukaj: ', marker='❯', marker_pl=' ', border=True, info=True, match_exact=False, exact_symbol=' E', height=10, max_height=None, cycle=True, wrap_lines=True, raise_keyboard_interrupt=False, mandatory_message='Wybierz opcję!'):
    menu = inquirer.fuzzy(
        message=message,
        choices=choices,
        pointer=pointer,
        style=style,
        vi_mode=vi_mode,
        qmark=qmark,
        amark=amark,
        instruction=instruction,
        long_instruction=long_instruction,
        multiselect=multiselect,
        prompt=prompt,
        marker=marker,
        marker_pl=marker_pl,
        border=border,
        info=info,
        match_exact=match_exact,
        exact_symbol=exact_symbol,
        height=height,
        max_height=max_height,
        cycle=cycle,
        wrap_lines=wrap_lines,
        raise_keyboard_interrupt=raise_keyboard_interrupt,
        mandatory_message=mandatory_message
    ).execute()
