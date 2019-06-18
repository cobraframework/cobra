from colorama import Fore, Style


def console_log(text, _type=None, title=None, space=False, space_number=0):
    # Checking text instance is string
    if isinstance(text, str):
        if title is None:
            if _type == 'success':
                return print(Style.DIM + Fore.GREEN + '[SUCCESS]'
                             + Style.RESET_ALL + ' ' + text)
            elif _type == 'warning':
                return print(Style.DIM + Fore.YELLOW + '[WARNING]'
                             + Style.RESET_ALL + ' ' + text)
            elif _type == 'error':
                return print(Style.DIM + Fore.RED + '[ERROR]'
                             + Style.RESET_ALL + ' ' + text)
            else:
                return print(text)
        elif title is not None \
                and isinstance(title, str) and not space:
            if _type == 'success':
                return print(Style.DIM + Fore.GREEN + '[SUCCESS]'
                             + Style.RESET_ALL + ' ' + Fore.WHITE + title
                             + ': ' + Style.RESET_ALL + text)
            elif _type == 'warning':
                return print(Style.DIM + Fore.YELLOW + '[WARNING]'
                             + Style.RESET_ALL + ' ' + Fore.WHITE + title
                             + ': ' + Style.RESET_ALL + text)
            elif _type == 'error':
                return print(Style.DIM + Fore.RED + '[ERROR]'
                             + Style.RESET_ALL + ' ' + Fore.WHITE + title
                             + ': ' + Style.RESET_ALL + text)
            else:
                return print(Fore.WHITE + title
                             + ': ' + Style.RESET_ALL + text)
        elif title is not None \
                and isinstance(title, str) and space:
            if _type == 'success':
                return print(Style.DIM + Fore.GREEN + '         '
                             + Style.RESET_ALL + ' ' + Fore.WHITE + title
                             + ': ' + Style.RESET_ALL + text)
            elif _type == 'warning':
                return print(Style.DIM + Fore.YELLOW + '         '
                             + Style.RESET_ALL + ' ' + Fore.WHITE + title
                             + ': ' + Style.RESET_ALL + text)
            elif _type == 'error':
                return print(Style.DIM + Fore.RED + '      '
                             + Style.RESET_ALL + ' ' + Fore.WHITE + title
                             + ': ' + Style.RESET_ALL + text)
            else:
                if space_number is 0:
                    return print(Fore.WHITE + '' + title
                                 + ': ' + Style.RESET_ALL + text)
                else:
                    return print(Fore.WHITE + ' ' * space_number + title
                                 + ': ' + Style.RESET_ALL + text)
