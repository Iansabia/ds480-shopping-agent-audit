from __future__ import annotations

from ..config import MODELS
from .base import Adapter


def make_adapter(model_key: str, tool_choice: str = "required", **kw) -> Adapter:
    s = MODELS[model_key]
    p = s["provider"]
    if p == "anthropic":
        from .anthropic_api import AnthropicAdapter
        return AnthropicAdapter(model_key, s, tool_choice=tool_choice)
    if p == "openai":
        from .openai_api import OpenAIAdapter
        return OpenAIAdapter(model_key, s, tool_choice=tool_choice, service_tier=kw.get("service_tier"))
    if p == "google":
        from .gemini_api import GeminiAdapter
        return GeminiAdapter(model_key, s, tool_choice=tool_choice)
    if p == "ollama":
        from .ollama_local import OllamaAdapter
        # Forced by the format schema, not by a tool_choice setting (PLAN D4).
        return OllamaAdapter(model_key, s, tool_choice="required")
    raise ValueError(p)
