# Shared Service

Common schemas, utilities, and shared code used across all FlipPilot services.

## What it does

- Defines Pydantic models and data schemas
- Provides shared utilities and helper functions
- Ensures consistent data structures across services
- Enables type safety and validation

## Usage

Import shared schemas and utilities in other services:

```python
from flippilot_shared.schemas import Item
from flippilot_shared.utils import some_helper_function
```

## Files

- `schemas.py` — Pydantic models and data schemas
- `utils.py` — Shared utility functions (to be added)

## Development

When adding new shared code:
1. Add schemas to `schemas.py`
2. Add utilities to `utils.py`
3. Update imports in consuming services
4. Ensure compatibility across all services
