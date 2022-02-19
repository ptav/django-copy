from html2text import html2text as h2t


def choices_as_string(choices, param, default="--"):
    return dict(choices).get(param, default)


def html2text(text):
    return h2t(text).replace('#','').replace('**','').replace('__','')

    