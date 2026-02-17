"""
LAMB API client for Evaluaitor.

Handles communication with LAMB's OpenAI-compatible completions API.
Stub for Phase 2 implementation.
"""

import logging
from typing import Dict, Any, List, Optional

import httpx

from config import LAMB_API_URL, LAMB_TIMEOUT

logger = logging.getLogger("evaluaitor")


class LAMBClient:
    """Client for LAMB's OpenAI-compatible completions API.

    This client communicates with LAMB's /v1/chat/completions endpoint
    to leverage AI assistants for evaluation tasks.
    """

    def __init__(self, base_url: str = None, timeout: int = None):
        self.base_url = base_url or LAMB_API_URL
        self.timeout = timeout or LAMB_TIMEOUT

    async def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        timeout: int = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """Call LAMB's /v1/chat/completions endpoint.

        Args:
            model: LAMB assistant ID (e.g., "lamb_assistant.eval_python_101")
            messages: Chat messages in OpenAI format
            timeout: Request timeout in seconds (overrides default)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            OpenAI-compatible completion response

        Raises:
            httpx.HTTPStatusError: On non-2xx response
            httpx.TimeoutException: On request timeout
        """
        timeout = timeout or self.timeout

        async with httpx.AsyncClient(timeout=timeout) as client:
            logger.info(
                "Calling LAMB completions API: model=%s, messages=%d",
                model, len(messages),
            )

            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                },
                headers={
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()

            result = response.json()
            logger.info(
                "LAMB API response received: tokens=%s",
                result.get("usage", {}).get("total_tokens", "N/A"),
            )
            return result

    async def health_check(self) -> bool:
        """Check if LAMB API is reachable.

        Returns:
            True if LAMB API responds, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except Exception:
            return False
