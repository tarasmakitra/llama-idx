import logging
import sys

from llama_index.core import set_global_handler

from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register


def enable_debug_mode():
    tracer_provider = register()
    LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
    # set_global_handler("simple")
