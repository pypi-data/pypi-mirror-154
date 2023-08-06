def capitalize_fullString(words):
    temp_name = ''
    space = ' '
    split_word = words.split()
    if len(split_word) > 1:
        for i in split_word:
            temp_name += i.capitalize()
            temp_name += space
        return temp_name.rstrip()
    elif len(split_word) == 1:
        return split_word[0].capitalize()
    else:
        return ''


