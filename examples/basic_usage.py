from prompt_registry import PromptRegistry

registry = PromptRegistry.from_path("prompts")
prompt = registry.get("support/refund_request")
rendered = prompt.render(
    customer_name="Taylor Smith",
    order_id="ORD-1042",
    message="My package arrived damaged and I want a refund.",
)

print(rendered.system)
print("---")
print(rendered.user)
