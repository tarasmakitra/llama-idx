from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register


def enable_debug_mode():
    tracer_provider = register()
    LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
