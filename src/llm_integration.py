"""
llm_integration.py — LLM client for the Feature Launch Kit (WBS 5.1).

Two brains, zero point of failure (Risk #3 in project_structure.md):
OpenAI is primary, Cohere is the automatic fallback if OpenAI fails.
Keys and model names load from .env (never committed — see agents.md).
"""

from __future__ import annotations

import os
import logging
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str


class LLMError(RuntimeError):
    """Raised only when every configured provider has failed."""


class LLMClient:
    """
    Provider-agnostic text generator.

    Usage:
        client = LLMClient()
        result = client.generate(system="...", user="...")
        print(result.text)          # the content
        print(result.provider)      # which brain answered
    """

    def __init__(
        self,
        primary: str = "openai",
        fallback: str | None = "cohere",
        temperature: float = 0.7,
        max_tokens: int = 1500,
    ) -> None:
        self.primary = primary
        self.fallback = fallback
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Models configurable via .env so we can swap cheap<->quality without
        # touching code. Defaults kept budget-friendly (€5 cap).
        self.models = {
            "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            "cohere": os.getenv("COHERE_MODEL", "command-r-plus-08-2024"),
        }

    def generate(self, system: str, user: str) -> LLMResponse:
        """Try the primary provider, fall back to the second on any failure."""
        providers = [self.primary] + ([self.fallback] if self.fallback else [])
        last_error: Exception | None = None

        for provider in providers:
            try:
                logger.info("Calling %s (%s)...", provider, self.models[provider])
                text = self._dispatch(provider, system, user)
                return LLMResponse(text=text, provider=provider, model=self.models[provider])
            except Exception as exc:  # noqa: BLE001 — any failure should fall back
                logger.warning("Provider '%s' failed: %s", provider, exc)
                last_error = exc

        raise LLMError(f"All providers failed. Last error: {last_error}")

    def _dispatch(self, provider: str, system: str, user: str) -> str:
        if provider == "openai":
            return self._call_openai(system, user)
        if provider == "cohere":
            return self._call_cohere(system, user)
        raise ValueError(f"Unknown provider: {provider}")

    def _call_openai(self, system: str, user: str) -> str:
        from openai import OpenAI  # lazy import: SDK optional per provider

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        resp = client.chat.completions.create(
            model=self.models["openai"],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content

    def _call_cohere(self, system: str, user: str) -> str:
        import cohere  # lazy import

        client = cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])
        resp = client.chat(
            model=self.models["cohere"],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        # Cohere v2 returns content as a list of blocks
        return resp.message.content[0].text


if __name__ == "__main__":
    # Smoke test — run: python -m src.llm_integration
    client = LLMClient()
    result = client.generate(
        system="You are a concise assistant.",
        user="Reply with exactly: LLM client is working.",
    )
    print(f"[{result.provider} / {result.model}] {result.text}")