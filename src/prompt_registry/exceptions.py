class PromptRegistryError(Exception):
    """Base exception for prompt-registry."""


class PromptValidationError(PromptRegistryError):
    """Raised when a prompt file is invalid."""


class PromptNotFoundError(PromptRegistryError):
    """Raised when a prompt reference cannot be resolved."""


class PromptRenderError(PromptRegistryError):
    """Raised when prompt rendering fails."""


class EvalError(PromptRegistryError):
    """Raised when an eval definition is invalid."""
