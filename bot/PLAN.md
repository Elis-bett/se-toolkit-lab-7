# Development Plan for SE Toolkit Bot

## Architecture Overview

The bot follows a clean separation of concerns:

- **Handlers**: Pure functions that take input and return text (no Telegram dependency)
- **Config**: Centralized environment variable management
- **Entry Point**: Two modes (Telegram polling and CLI test mode)

## Implementation Phases

1. **Scaffolding** (Task 1): Create directory structure, config, placeholder handlers, test mode.
2. **Backend Integration** (Task 2): Connect to LMS API for real data in `/health` and `/scores`.
3. **Intent Routing** (Task 3): Use LLM to handle natural language queries like "what labs are available".
4. **Deployment** (Task 4): Run bot as a systemd service on the VM with automatic restart.

## Testing Strategy

- Local: `--test` mode to verify handlers without Telegram
- Remote: Deploy to VM, check Telegram responses
- Integration: Mock API responses for LMS and LLM in CI

## Key Decisions

- Use `uv` for dependency management (fast, reliable)
- Keep handlers stateless for easy testing
- Separate bot logic from transport layer (Telegram)
- Use environment files for secrets, never commit them
