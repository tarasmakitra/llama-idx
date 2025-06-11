from llama_index.core.llms.llm import LLM
from llama_index.core.tools.tool_spec.base import BaseToolSpec


class GeneralKnowledgeTool(BaseToolSpec):
    """General knowledge tool spec."""

    spec_functions = ["answer_question"]

    def __init__(self, llm: LLM):
        """Initialize the General knowledge tool."""
        self.llm = llm

    def answer_question(self, question: str) -> str:
        """
        Answer questions based on general knowledge unrelated to the candidate.
        Use this tool when other tools return no results.

        Args:
            question (str): the question to answer

        """

        prompt = "Answer the following question in 1-3 sentences:\n" f"{question}"
        response = self.llm.complete(prompt)
        return str(response)
