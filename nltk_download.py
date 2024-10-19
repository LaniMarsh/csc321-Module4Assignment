import nltk
import ssl

try:
    _create_unverified_htts_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_htts_context

nltk.download('words')