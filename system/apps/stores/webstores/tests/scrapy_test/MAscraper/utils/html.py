import re


def cleanhtml(raw_html):

    cleanr = re.compile('<.*?>')

    if isinstance(raw_html, str):
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    if isinstance(raw_html, list):
        cleantext = [re.sub(cleanr, '', componente) for componente in raw_html]
        return cleantext

def html2list(raw_html):

    cleanr = re.compile('<.*?>')

    if isinstance(raw_html,str):
        cleantext = re.sub(cleanr, '\n', raw_html)
        return cleantext

    if isinstance(raw_html,list):
        cleantext = [re.sub(cleanr, '\n', componente) for componente in raw_html]
        return cleantext