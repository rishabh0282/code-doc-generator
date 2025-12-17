"""
DocGenerator using LangChain + OpenAI (MVP wrapper).
"""
from typing import Dict, Any, List, Optional
import os
import logging

from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

logger = logging.getLogger(__name__)


class DocGenerator:
    def __init__(self, api_key: Optional[str] = None, temperature: float = 0.0):
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        self.llm = OpenAI(temperature=temperature)
        self.template = PromptTemplate(
            input_variables=["signature", "doc"],
            template="Write a concise docstring for the following function signature:\n\n{signature}\n\nContext:\n{doc}\n"
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.template)

    def generate_for_function(self, signature: str, doc_ctx: str = "") -> str:
        try:
            out = self.chain.run({"signature": signature, "doc": doc_ctx})
            return out.strip()
        except Exception:
            logger.exception("LLM generation failed, returning fallback")
            return f"Generated docstring for {signature}"