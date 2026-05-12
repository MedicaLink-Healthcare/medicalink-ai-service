import logging
from dataclasses import dataclass

import tiktoken

logger = logging.getLogger(__name__)


@dataclass(slots=True, kw_only=True)
class TokenBudgetManager:
    model_name: str
    reserve_tokens: int = 8000

    _encoding: tiktoken.Encoding | None = None

    def get_encoding(self) -> tiktoken.Encoding:
        if self._encoding is None:
            try:
                self._encoding = tiktoken.encoding_for_model(self.model_name)
            except KeyError:
                logger.warning(
                    f"Model {self.model_name} not found in tiktoken. Falling back to cl100k_base."
                )
                self._encoding = tiktoken.get_encoding("cl100k_base")
        return self._encoding

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        encoding = self.get_encoding()
        return len(encoding.encode(text))

    def token_aware_truncate(self, text: str, max_tokens: int) -> str:
        """Truncates text to ensure it does not exceed max_tokens, prioritizing sentence boundaries if possible."""
        if not text:
            return ""

        encoding = self.get_encoding()
        tokens = encoding.encode(text)

        if len(tokens) <= max_tokens:
            return text

        # Truncate tokens and decode back to string
        truncated_text = encoding.decode(tokens[:max_tokens])

        # Try to find a logical boundary (like a period or newline) in the last portion
        last_period = truncated_text.rfind(". ")
        last_newline = truncated_text.rfind("\n")

        boundary = max(last_period, last_newline)

        # If the boundary is reasonably close to the end (e.g., within the last 30%), cut there
        if boundary > len(truncated_text) * 0.7:
            return truncated_text[: boundary + 1].strip()

        # Fallback to word boundary
        last_space = truncated_text.rfind(" ")
        if last_space > 0:
            return truncated_text[:last_space].strip() + "..."

        return truncated_text.strip() + "..."
