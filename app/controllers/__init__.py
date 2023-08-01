def encrypt(tex):
    text = str(tex)
    key = "khvIUyiYVIUUCTCVKgy88yJGIUgdbaduGIbjkdfbKKbiuei383H"
    result = ""
    key_len = len(key)

    for i in range(len(text)):
        char = text[i]
        shift = key[i % key_len]

        if char.isupper():
            char = chr((ord(char) - ord('A') + ord(shift) - ord('A')) % 26 + ord('A'))
        elif char.islower():
            char = chr((ord(char) - ord('a') + ord(shift) - ord('a')) % 26 + ord('a'))

        result += char

    return result


def decrypt(tex):
    text = str(tex)
    key = "khvIUyiYVIUUCTCVKgy88yJGIUgdbaduGIbjkdfbKKbiuei383H"
    result = ""
    key_len = len(key)

    for i in range(len(text)):
        char = text[i]
        shift = key[i % key_len]

        if char.isupper():
            char = chr((ord(char) - ord('A') + 26 - (ord(shift) - ord('A'))) % 26 + ord('A'))
        elif char.islower():
            char = chr((ord(char) - ord('a') + 26 - (ord(shift) - ord('a'))) % 26 + ord('a'))

        result += char

    return result