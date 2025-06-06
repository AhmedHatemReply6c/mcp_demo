# MCP Demo
## Quickstart
* Download the following ollama models: `qwen3:1.7b`, `mistral:latest`
```bash
ollama pull qwen3:1.7b
ollama pull mistral:latest
```
* Run the client application 
```bash
uv run client.py
```

## How to get started
* Download and install Ollama from the [official website](https://ollama.com)
* Make sure it's running by testing it with a tiny model (92 MB)
```bash
ollama run smollm:135m Write a 'Hello World' program in python!
```
* Download some larger models necessary for the demo to run
```bash
ollama pull qwen3:1.7b # 1.4GB
ollama pull mistral:7b # 4.1GB
```
* Run the `client.py` which in turn runs the `server.py`
```bash
uv run client.py
```
* Now you should see an input fiels stating: `❓  Ask about MCP or request code (type 'exit' to quit):`
* If you now type `What is MCP about?` the model will answer accordingly:
```text
<think>
The Model Context Protocol (MCP) is an open protocol designed to enable seamless integration between large language models (LLMs) and external data sources or tools. It allows applications to share contextual information with LLMs, expose tools and capabilities, and build composable integrations and workflows. MCP uses JSON-RPC 2.0 messages to facilitate communication between hosts (LLM applications), clients (connectors within the host), and servers (services providing context and capabilities). It is inspired by the Language Server Protocol (LSP) and aims to standardize how AI applications can integrate with external tools and data.

The protocol includes key features such as resource sharing, prompt templating, and tool execution. Servers can offer resources, prompts, and tools, while clients can offer sampling and other features. Security is a critical aspect, with principles like user consent, data privacy, and tool safety requiring explicit user authorization and careful implementation.

An example of a simple MCP server is provided, which exposes a calculator tool and a greeting resource. This demonstrates how MCP can be used to integrate LLMs with external tools and data sources.
</think>

I can answer without using any more tools. I'll use the user's language to answer.

The Model Context Protocol (MCP) is an open protocol that enables seamless integration between large language models (LLMs) and external data sources or tools. It allows applications to share contextual information with LLMs, expose tools and capabilities, and build composable integrations and workflows. MCP uses JSON-RPC 2.0 messages to facilitate communication between hosts (LLM applications), clients (connectors within the host), and servers (services providing context and capabilities). It is inspired by the Language Server Protocol (LSP) and aims to standardize how AI applications can integrate with external tools and data sources. Key features include resource sharing, prompt templating, and tool execution, with a focus on security and user control.
```
* If you now type `Write an MCP server in Python for me!` the model will answer accordingly:
````text
<think>
Okay, the user asked for an MCP server in Python. I used the generate_mcp_server_code function with the query "A basic MCP server with a simple endpoint that responds to HTTP requests". The tool response provided the Python code.

Now, I need to present this code to the user. Let me check the code again to make sure it's correct. The code sets up a Flask app with a route that returns a greeting. It uses the MCP protocol, so the user should understand how it's structured. I'll explain that the server listens on port 5000 and responds to GET requests with a simple message. Also, mention that they can extend it by adding more routes or integrating with other services. Keep the explanation clear and helpful.
</think>

I'll provide the MCP server code. Here's the Python implementation:

```python
from flask import Flask
import json

app = Flask(__name__)

@app.route('/mcp', methods=['GET'])
def mcp_endpoint():
    return json.dumps({"status": "success", "message": "MCP server is running!"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

This server:
1. Listens on port 5000
2. Has a simple endpoint `/mcp` that returns a JSON response
3. Uses Flask for quick development
4. Can be extended by adding more routes or integrating with other MCP services

You can run this code and test the endpoint by visiting http://localhost:5000/mcp in your browser. Let me know if you want to add more features like authentication or advanced MCP protocol support!
````

## Sources
* `https://modelcontextprotocol.io/llms-full.txt`
* `https://docs.llamaindex.ai/en/stable/examples/agent/react_agent/`