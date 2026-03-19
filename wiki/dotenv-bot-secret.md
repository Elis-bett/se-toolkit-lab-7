# `.env.bot.secret`

<h2>Table of contents</h2>

- [About `.env.bot.secret`](#about-envbotsecret)
- [`BOT_TOKEN`](#bot_token)
- [LMS backend connection](#lms-backend-connection)
  - [`LMS_API_URL`](#lms_api_url)
  - [`LMS_API_KEY`](#lms_api_key)
- [LLM API](#llm-api)
  - [`LLM_API_KEY`](#llm_api_key)
  - [`LLM_API_BASE_URL`](#llm_api_base_url)
  - [`LLM_API_MODEL`](#llm_api_model)

## About `.env.bot.secret`

`.env.bot.secret` is a [`.env` file](./environments.md#env-file) that stores [environment variables](./environments.md#environment-variable) for the Telegram bot.

The values configure the bot token, the [LMS API](./lms-api.md#about-the-lms-api) connection, and the [LLM](./llm.md) that powers the bot.

Default values: [`.env.bot.example`](../.env.bot.example)

> [!NOTE]
> `.env.bot.secret` was added to [`.gitignore`](./git.md#gitignore) because you may specify there
> [secrets](./environments.md#secrets) such as the [`BOT_TOKEN`](#bot_token) or the [`LLM_API_KEY`](#llm_api_key).

## `BOT_TOKEN`

The Telegram bot token obtained from [`@BotFather`](https://core.telegram.org/bots#botfather).

Default: `your-telegram-bot-token-here`

## LMS backend connection

The bot calls these endpoints to communicate with the [LMS API](./lms-api.md#about-the-lms-api).

### `LMS_API_URL`

The base [URL](./computer-networks.md#url) of the [LMS API](./lms-api.md#about-the-lms-api).

See [LMS API base URL](./lms-api.md#lms-api-base-url).

Default: `http://localhost:42002`

### `LMS_API_KEY`

The [LMS API key](./lms-api.md#lms-api-key).

Its value must match the value of [`LMS_API_KEY`](./dotenv-docker-secret.md#lms_api_key) in [`.env.docker.secret`](./dotenv-docker-secret.md#what-is-envdockersecret).

Default: `my-secret-api-key`

## LLM API

Variables for the [LLM](./llm.md) that powers the bot.

### `LLM_API_KEY`

The [API key](./web-api.md#api-key) for your [LLM provider API](./llm.md#llm-provider-api).

- For the [`Qwen Code` API](./qwen-code-api.md#what-is-qwen-code-api):

  the value of [`QWEN_CODE_API_KEY`](./qwen-code-api-dotenv-secret.md#qwen_code_api_key) from [`qwen-code-api/.env.secret`](./qwen-code-api-dotenv-secret.md#about-qwen-code-apienvsecret).

- For the [`OpenRouter` API](./llm.md#openrouter-api):

  your `OpenRouter` API key.

Default: `my-secret-qwen-key`

### `LLM_API_BASE_URL`

The base URL of the [OpenAI-compatible API](./llm.md#openai-compatible-api) endpoint.

- For the [`Qwen Code` API](./qwen-code-api.md#what-is-qwen-code-api) on your VM:

  `<lms-api-url>/utils/qwen-code-api/v1`.

  See [`<lms-api-url>`](./lms-api.md#lms-api-base-url-placeholder).

- For the [`OpenRouter` API](./llm.md#openrouter-api):

  `https://openrouter.ai/api/v1`.

Default: `http://localhost:42005/v1`

### `LLM_API_MODEL`

The name of the [LLM model](./llm.md#model) to use via the [LLM provider API](./llm.md#llm-provider-api).

- For the [`Qwen Code` API](./qwen-code-api.md#what-is-qwen-code-api) on your VM:

  `coder-model`.

  See [View available models](./qwen-code.md#view-available-models).

- For the [`OpenRouter` API](./llm.md#openrouter-api):

  `meta-llama/llama-3.3-70b-instruct:free`.

Default: `coder-model`
