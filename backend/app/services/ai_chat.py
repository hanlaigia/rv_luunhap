"""Trợ lý Rovva AI — gọi Groq API (OpenAI-compatible)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = (
    "Bạn là Trợ lý Rovva AI — nền tảng đặt phòng homestay và khách sạn tại Việt Nam. "
    "Trả lời ngắn gọn, thân thiện, bằng tiếng Việt. "
    "Hỗ trợ: tìm chỗ nghỉ, lên lịch trình, ưu đãi, hủy/đặt phòng, hướng dẫn Host. "
    "Nếu không chắc, gợi ý liên hệ hotline 1900 2005 hoặc mục Trợ giúp & Yêu cầu."
)

DEFAULT_MODEL = "llama-3.3-70b-versatile"


def _api_key() -> str | None:
    try:
        from flask import current_app

        key = current_app.config.get("GROQ_API_KEY")
        if key:
            return key
    except RuntimeError:
        pass
    return os.environ.get("GROQ_API_KEY")


def _model_name() -> str:
    try:
        from flask import current_app

        model = current_app.config.get("GROQ_MODEL")
        if model:
            return model
    except RuntimeError:
        pass
    return os.environ.get("GROQ_MODEL", DEFAULT_MODEL)


def chat_completion(messages: list[dict], *, model: str | None = None) -> str:
    """Gửi hội thoại tới Groq. `messages` dạng OpenAI: [{role, content}, ...]."""
    api_key = _api_key()
    if not api_key:
        raise RuntimeError(
            "Chưa cấu hình GROQ_API_KEY. Tạo file .env tại thư mục gốc project."
        )

    body = json.dumps(
        {
            "model": model or _model_name(),
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *messages],
            "temperature": 0.7,
            "max_tokens": 800,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        GROQ_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "Rovva-Platform/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Groq API lỗi {exc.code}: {err_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Không kết nối được Groq API: {exc.reason}") from exc

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Phản hồi Groq không hợp lệ.") from exc
