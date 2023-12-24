# Cadmus

Cadmus supplies a pluggable memory module for AI Agents.

Current AI agents and their memory mechanism suffer from three problems:

1. There is no easy way to get a summary of the data
2. You can only supply latest messages in their APIs

MemGPT provide a setup towards this direction:

1. Conversation History -> Recall Storage
2. Working Context -> Archival Storage

## Installation

```bash
npm install cadmus
```