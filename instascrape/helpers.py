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
    # remove emojis from text
    remove_emojis = emoji_remover(input_string)
    # extract email
    email_regex_result = re.search(r'[\w\.-]+@[\w\.-]+', remove_emojis)
    if email_regex_result:
        return email_regex_result.group(0) if validate_email(email_regex_result.group(0)) else None
    return
