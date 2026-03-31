import pytest

from prompt_registry import PromptRegistry
from prompt_registry.exceptions import PromptRenderError


def test_prompt_rendering_success():
    registry = PromptRegistry.from_path("prompts")
    prompt = registry.get("support/refund_request@1.1.0")
    rendered = prompt.render(
        customer_name="Taylor Smith",
        order_id="ORD-1042",
        message="My package arrived damaged and I want a refund.",
    )
    assert "Taylor Smith" in rendered.user
    assert "30 days" in rendered.user


def test_missing_required_variable_raises():
    registry = PromptRegistry.from_path("prompts")
    prompt = registry.get("support/refund_request@1.0.0")
    with pytest.raises(PromptRenderError):
        prompt.render(customer_name="Taylor Smith", order_id="ORD-1042")
