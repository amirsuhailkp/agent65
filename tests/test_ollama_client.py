"""Tests for OllamaClient's option passthrough (context_window, num_gpu,
keep_alive). These matter because a 2026-08-16 config fix (context_window
lowered from 8192 to fit 4GB VRAM) and the num_gpu/keep_alive additions
directly addressed the multi-week 10-20min-per-call latency problem — a
regression here would silently reintroduce it.
"""
from unittest.mock import MagicMock, patch

from src.reasoning.ollama_client import OllamaClient


def _client_with_fake_ollama(**kwargs):
    """Build an OllamaClient with ollama.Client replaced by a MagicMock,
    returning (agent_client, fake_ollama_client) so options passed to
    fake_ollama_client.chat() can be inspected.
    """
    with patch("src.reasoning.ollama_client.ollama.Client") as MockClient:
        fake = MagicMock()
        fake.chat.return_value = {"message": {"content": "ok"}}
        MockClient.return_value = fake
        client = OllamaClient(host="http://x", model="qwen3:4b", **kwargs)
    return client, fake


def test_context_window_passed_as_num_ctx():
    client, fake = _client_with_fake_ollama(context_window=3072)
    client.chat([{"role": "user", "content": "hi"}])
    assert fake.chat.call_args.kwargs["options"]["num_ctx"] == 3072


def test_num_gpu_passed_through_when_set():
    client, fake = _client_with_fake_ollama(num_gpu=99)
    client.chat([{"role": "user", "content": "hi"}])
    assert fake.chat.call_args.kwargs["options"]["num_gpu"] == 99


def test_num_gpu_omitted_from_options_when_unset():
    # None (the default) must NOT appear as a literal "num_gpu": None in
    # options — that would override Ollama's own auto-detection with an
    # invalid value instead of leaving it alone.
    client, fake = _client_with_fake_ollama()
    client.chat([{"role": "user", "content": "hi"}])
    assert "num_gpu" not in fake.chat.call_args.kwargs["options"]


def test_keep_alive_defaults_to_30m():
    # Regression: Ollama's own factory default is 5m, too short for this
    # agent's multi-minute gaps between calls within a cycle (tool
    # dispatch, verification, etc.) — a too-short keep_alive causes the
    # model to unload and pay a full reload cost on the next call.
    client, fake = _client_with_fake_ollama()
    client.chat([{"role": "user", "content": "hi"}])
    assert fake.chat.call_args.kwargs["keep_alive"] == "30m"


def test_keep_alive_override_respected():
    client, fake = _client_with_fake_ollama(keep_alive="5m")
    client.chat([{"role": "user", "content": "hi"}])
    assert fake.chat.call_args.kwargs["keep_alive"] == "5m"