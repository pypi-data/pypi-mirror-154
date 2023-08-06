import time


def type_out_slowly(text: str, delay: float):
    for c in _merge_control_chars(text):
        print(c, end="", flush=True)
        time.sleep(delay)


def _merge_control_chars(text: str):
    chars = []
    in_control_char = False
    for c in text:
        if c == "\x1b":
            in_control_char = True
        if in_control_char:
            if len(chars) == 0:
                chars.append("")
            chars[0] += c
        else:
            chars.append(c)
        if c == "m" and in_control_char:
            in_control_char = False
    return chars
