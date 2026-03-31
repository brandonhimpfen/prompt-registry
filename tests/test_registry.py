from prompt_registry import PromptRegistry


def test_registry_loads_prompts():
    registry = PromptRegistry.from_path("prompts")
    refs = registry.list_refs()
    assert "support/refund_request@1.0.0" in refs
    assert "support/refund_request@1.1.0" in refs


def test_latest_prompt_resolution():
    registry = PromptRegistry.from_path("prompts")
    prompt = registry.get("support/refund_request")
    assert prompt.version == "1.1.0"
