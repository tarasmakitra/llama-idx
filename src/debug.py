import logging
import sys

import llama_index.core


def enable_debug_mode():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
    llama_index.core.set_global_handler("simple")
