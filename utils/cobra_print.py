from lazyme.string import color_print


# Cobra Color Print
def cobra_print(text, color=None, bold=False, background=None, underline=False):
    if color == 'success':
        return color_print(text, color='green', bold=bold, highlighter=background, underline=underline)
    elif color == 'warning':
        return color_print(text, color='yellow', bold=bold, highlighter=background, underline=underline)
    elif color == 'error':
        return color_print(text, color='red', bold=bold, highlighter=background, underline=underline)
    else:
        return color_print(text, bold=bold, highlighter=background, underline=underline)
