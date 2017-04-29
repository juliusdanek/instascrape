import re
from validate_email import validate_email


def emoji_remover(input_string):
    """
    Removes all emojis in a text
    From: http://stackoverflow.com/questions/26568722/remove-unicode-emoji-using-re-in-python
    """
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
                          u'\U0001F300-\U0001F64F'
                          u'\U0001F680-\U0001F6FF'
                          u'\u2600-\u26FF\u2700-\u27BF]+',
                          re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
                          u'\ud83c[\udf00-\udfff]|'
                          u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                          u'[\u2600-\u26FF\u2700-\u27BF])+',
                          re.UNICODE)
    # replacing with empty space here due to emojis often being connected to next character
    return(myre.sub(r' ', input_string))


def extract_email(input_string):
    """
    Extracts email from a string of characters
    """
    if not input_string:
        return
    # remove emojis from text
    remove_emojis = emoji_remover(input_string)
    # extract email
    email_regex_result = re.search(r'[\w\.-]+@[\w\.-]+', remove_emojis)
    if email_regex_result:
        return email_regex_result.group(0) if validate_email(email_regex_result.group(0)) else None
    return


def extract_hashtags(input_string):
    """
    Extracts hashtags from a string of characters
    """
    if not input_string:
        return
    removed_emojis = emoji_remover(input_string)
    hash_regex = re.compile(r'(^|\s)(#[a-z\d-]+)')
    possible_hashtags = hash_regex.findall(removed_emojis)
    if possible_hashtags:
        return [tag[1].replace('#', '') for tag in possible_hashtags]
    return


def remove_dot(input_string):
    if input_string[-1] != '.':
        return input_string
    else:
        return remove_dot(input_string[:-1])


def extract_mentions(input_string):
    """
    Extracts hashtags from a string of characters
    """
    if not input_string:
        return
    removed_emojis = emoji_remover(input_string.lower())
    mention_regex = re.compile(r'(^|\s)(@[^\s,!\')]+)')
    possible_mentions = mention_regex.findall(removed_emojis)
    if possible_mentions:
        return [remove_dot(tag[1].replace('@', '')) for tag in possible_mentions]
    return

caption = "Aloha Weekend! It's time for some new adventures. 💦🌴What are your plans ? - 📷 by @fashionismyfortee @hellofresh #kaptenandson #bekapten"
