"""Stateless text views shared by E-commerce Stages 02–03.

Extracted unchanged from Stage 02; no fitted vocabulary, labels or resource downloads.
"""
from functools import wraps
import html
import re
import unicodedata

import pandas as pd

def preserve_missing(function):
    @wraps(function)
    def safe(value):
        if value is None or pd.isna(value): return pd.NA
        if not isinstance(value,str): raise TypeError("Expected a string or a missing scalar")
        return function(value)
    return safe

@preserve_missing
def unicode_nfkc(text): return unicodedata.normalize("NFKC",text)

@preserve_missing
def lowercase(text): return text.lower()

# Fixed common HTML tag names, followed by a tag boundary; quoted attributes are supported.
# No generic <.*?> deletion: <5, <10cm> and unknown tag-shaped strings survive this step.
HTML_TAG_RE=re.compile(
    r"<\s*/?\s*(?:a|abbr|b|blockquote|br|div|em|font|h[1-6]|hr|i|img|li|ol|p|s|small|span|strong|sub|sup|table|tbody|td|th|thead|tr|u|ul)"
    r"(?=[\s/>])(?:[^<>\"']|\"[^\"]*\"|'[^']*')*>",re.IGNORECASE)

@preserve_missing
def remove_html_tags(text): return HTML_TAG_RE.sub(" ",text)

@preserve_missing
def decode_entities(text): return html.unescape(text)

URL_RE=re.compile(r"\b(?:https?://|www\.)[^\s<>]+",re.IGNORECASE)
@preserve_missing
def remove_urls(text):
    def replace(match):
        value=match.group();trimmed=value.rstrip(".,;:!?)]}")
        return " "+value[len(trimmed):]  # Preserve candidate sentence-final punctuation.
    return URL_RE.sub(replace,text)

@preserve_missing
def remove_mentions(text): return re.sub(r"(?<!\w)@\w+"," ",text)

@preserve_missing
def remove_hashtag_marker(text): return re.sub(r"(?<!\w)#(?=\w)","",text)

# Keep identifier/measurement punctuation, rather than erasing all non-alphanumerics.
KEPT_SYMBOLS=set("'\"_-./+%<>=×°±")
SYMBOL_TRANSLATION=str.maketrans({"’":"'","‘":"'","“":'"',"”":'"',"–":"-","—":"-"})
@preserve_missing
def conditional_symbols(text):
    mapped=text.translate(SYMBOL_TRANSLATION)
    return "".join(c if c.isalnum() or c.isspace() or c in KEPT_SYMBOLS else " " for c in mapped)

@preserve_missing
def keep_numbers(text): return text

STANDALONE_NUMBER_RE=re.compile(r"(?<!\S)[+-]?\d+(?:[.,]\d+)*(?!\S)")
@preserve_missing
def drop_standalone_numbers(text): return STANDALONE_NUMBER_RE.sub(" ",text)

@preserve_missing
def normalize_whitespace(text): return " ".join(text.split())

LEXICAL_RE=re.compile(r"[^\W_]+(?:['’][^\W_]+)*",re.UNICODE)
def lexical_tokens(text): return LEXICAL_RE.findall(text.lower())

def light_input(text):
    # Shared benchmark view: leave case, punctuation, handles, URLs and numbers intact.
    for function in [unicode_nfkc,remove_html_tags,decode_entities,normalize_whitespace]:
        text=function(text)
    return text

def normalize_default(text):
    """Stage 02 default in the same order, preserving numeric content and missing scalars."""
    for function in [unicode_nfkc, lowercase, remove_html_tags, decode_entities, remove_urls,
                     remove_mentions, remove_hashtag_marker, conditional_symbols,
                     keep_numbers, normalize_whitespace]:
        text = function(text)
    return text
