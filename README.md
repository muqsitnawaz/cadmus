# Cadmus

Cadmus provides a unified memory abstraction for AI Agents. It has a pluggable memory
module which makes retrieving the latest and most similar information super easy.

## Motivation

Current AI agents and their memory mechanism do not provide a unified way to store and
retrieve the latest and most similar messages which is often time needed when using the
APIs of LLMs providers e.g. OpenAI.

In a real-world AI product, it is generally not feasible to store all this information in
the LLM context. For example, in a chatbot, the conversation history can be range from months to years. Similarly,
the functions that the chatbot can perform will be in the hundreds or thousands.

Cadmus provides a pluggable memory module that can be easily used by other AI products.
It provides a **Cache** abstraction which at the backend connects to an **Embedding** store.
The Cache can be used to store different types of information e.g. Messages, Notes and
Functions.

1. **Messages** represent the ongoing conversation history between the user and the AI.

2. **Notes** represent the notes taken down by the AI which can range from summaries to
   action items.

3. **Functions** represent the functions that the AI can perform when asked by the user.

By utilizing these unified abstractions provided by Cadmus, you can offload the storage and retrieval
parts of your AI products.

## Usage

Cadmus makes it super easy to retrieve the latest and most similar information in order to be
passed to the LLM APIs.

```python
from cadmus import Cache

cache = Cache()  # or Cache(backend='https://weaviate-instance.com')

cache.add_message(...)

# Get a combination of top and similar messages
messages = cache.get_messages()

# Get the latest 10 messages
messages1 = cache.get_messages(latest=10, similar=0)

# Get top 10 messages similar to the latest message
messages2 = cache.get_messages(latest=1, similar=10)
```

In the above example, calling the .get_messages() method will return the top and similar messages
from the cache. The top messages are the ones that are the most recent messages and the similar
messages are the ones that are similar to the top messages.

## Installation

```bash
pip install zf-cadmus
```

```bash
# ~/.zshrc
export OPENAI_API_KEY=<your-openai-api-key>
```

You will need to spin up a Weaviate instance in order to use Cadmus. You can do so using
Docker in the following:

```yaml
# db.yml
version: '3.4'
services:
  weaviate:
    image: semitechnologies/weaviate:1.20.2
    restart: always
    command:
      - --host
      - 0.0.0.0
      - --port
      - '8080'
      - --scheme
      - http
    ports:
      - 8080:8080
    volumes:
      - /Users/<USER>/databases/weaviate:/Users/<USER>/databases/weaviate
    environment:
      CLUSTER_HOSTNAME: 'cadmus'
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: 'true'
      PERSISTENCE_DATA_PATH: '/Users/<USER>/databases/weaviate'
      DISK_USE_READONLY_PERCENTAGE: 95
      DEFAULT_VECTORIZER_MODULE: 'none'
```

```bash
docker compose -f db.yml up -d
```

# Appendix

Cadmus is inspired by the following papers:

### MemGPT

[MemGPT](https://arxiv.org/pdf/2310.08560.pdf) takes a step towards long-memory AI agents by
by introducing Main Context and External Context.

Main Context contains the Conversation History and Working Context.

External Context Contains the Recall Storage and Archival Storage.

Recall Storage (implemented as an Embedding Database) is used to offload the extra conversation
history that does not fit into the LLM Context, while Archival Storage is used to offload the
extra working context that does not fit into the LLM Context.

1. Conversation History -> Recall Storage
2. Working Context -> Archival Storage

However, MemGPT did not provide any useful abstractions that can be easily extended to or used
by other AI products.