from prompt_registry import PromptRegistry, EvaluationSuite, evaluate_suite


def test_eval_suite_passes():
    registry = PromptRegistry.from_path("prompts")
    suite = EvaluationSuite.from_path("examples/evals/support_refund_request.yaml")
    results = evaluate_suite(registry, suite)
    assert results
    assert all(result.passed for result in results)
