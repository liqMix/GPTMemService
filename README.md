# GPT Mem Service

## Description

A Flask wrapper around HyperDB and OpenAI's ChatGPT chat completion API.
Allows multiple vector db instances identified by name.

Useful for using a single endpoint for referencing different memory instances.

## Requirements

Python 3.10+
OpenAPI Key

## Install

`pip install -r requirements.txt`

## Run

Edit `config.yaml`
`python main.py`

## Endpoints

`/ GET`
Retrieves details about the current memory

`/ POST`

```
{
  "name": <name of memory>,
  "prompt": <user prompt>
}
```

Generates a response from GPT using the memory by name. Returns text

`/memory GET`
Returns list of all the memory configurations

`/memory/<name> GET`
Retrieves the memory config by name

`/memory/name POST`

```
{
  "name": <name of memory>,
  "system_prompt": <the prompt to preface all queries by>,
  "short_memory_length": <number of lines of chat history to include in query>
}
```

Can be utilized to both create and update existing memory configurations

## TODO

AuthN, AuthZ for API and for specific memory access
Optimize memory swapping
Optimize token fitting
