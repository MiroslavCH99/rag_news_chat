from __future__ import annotations
import logging
from typing import List, Dict, Any

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from . import config

logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = (
    "<s>[INST] <<SYS>> Используй предоставленный контекст для ответа на вопрос как можно точнее. "
    "Если ответа нет, скажи: 'Не знаю'. <</SYS>>\n"
    "Вопрос: {question}\n\nКонтекст:\n{context}\n\nОтвет: [/INST]"
)


class AnswerGenerator:
    def __init__(self) -> None:
        logger.info("Loading LLM: %s", config.GEN_MODEL_NAME)
        tokenizer = AutoTokenizer.from_pretrained(config.GEN_MODEL_NAME, use_fast=True)
        model = AutoModelForCausalLM.from_pretrained(
            config.GEN_MODEL_NAME,
            device_map="auto",
            low_cpu_mem_usage=True,
            trust_remote_code=True,
        )
        self.pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=config.DEVICE,
            model_kwargs={"pad_token_id": tokenizer.eos_token_id},
        )

    @staticmethod
    def _make_prompt(question: str, docs: List[Dict[str, Any]]) -> str:
        ctx = "\n".join(f"[{i+1}] {d['text'].strip()}" for i, d in enumerate(docs))
        return PROMPT_TEMPLATE.format(question=question.strip(), context=ctx)

    def generate(self, question: str, docs: List[Dict[str, Any]]) -> str:
        prompt = self._make_prompt(question, docs)
        out = self.pipe(
            prompt,
            max_new_tokens=config.MAX_ANSWER_TOKENS,
            temperature=0.0,
            top_p=0.9,
            do_sample=False,
        )[0]["generated_text"]
        return out[len(prompt) :].strip()