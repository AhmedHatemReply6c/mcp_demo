# MCP Demo

## Quickstart

* Put the model names you would like your client and server to use in `ollama/models.txt` like such, that they can be pre-pulled

```bash
qwen3:1.7b
```

* We took some more capable models for our demo:

```bash
qwen3:4b
mistral:7b
```

* In the docker compose file `docker-compose.yml`, change the environment variable MODEL_NAME for the client and the server to be the models you would like each of them them to use.
* Run the docker containers

```bash
docker compose up
```

* Wait for the ollama container to pull the models you specified. It will log "All models are ready" once it is done.
* Then run the client application by connection to a shell on the client container

```bash
docker exec -it mcp_demo-client-1 python3 client.py
```

* Now you should see an input fiels stating: `❓  Ask about MCP or request code (type 'exit' to quit):`
* If you now type `What is MCP about?` the model will answer accordingly:

```text
<think>
Okay, the user asked, "What is MCP about?" I need to explain the Model Context Protocol (MCP) based on the provided documentation.

First, I'll start by defining MCP and its purpose. The documentation mentions that MCP is an open protocol for integrating LLM applications with external data sources and tools. I should highlight that it enables sharing context, exposing tools, and building integrations.

Next, I'll outline the key features from the overview section. This includes using JSON-RPC 2.0, stateful connections, and the roles of hosts, clients, and servers. Also, mention the inspiration from the Language Server Protocol and the key details like resources, prompts, tools, and utilities like configuration and logging.

I should also touch on the security principles, such as user consent, data privacy, tool safety, and LLM sampling controls. It's important to note that implementors must address these considerations carefully.

Finally, I'll conclude by summarizing MCP's role in the AI ecosystem, emphasizing its standardized approach for integrating context and tools. Make sure the explanation is clear and covers the main points without getting too technical.
</think>

The Model Context Protocol (MCP) is an open protocol that enables seamless integration between large language models (LLMs) and external data sources, tools, and applications. It provides a standardized way for applications to:

1. **Share contextual information** with LLMs  
2. **Expose tools and capabilities** to AI systems  
3. **Build composable integrations** and workflows  

Key features include:  
- Use of JSON-RPC 2.0 for communication  
- Stateful connections between hosts, clients, and servers  
- Support for resources (data/context), prompts (templated workflows), and tools (functions for AI to execute)  
- Security principles requiring user consent, data privacy, and tool safety  

MCP takes inspiration from the Language Server Protocol and is designed to standardize how AI applications integrate with external systems, while emphasizing safety and user control.
```

* If you now type `Write an MCP server in Python for me!` the model will answer accordingly
* What the SLM *thinks* internally before calling the MCP Server

```text
<think>
Okay, the user wants me to write an MCP server in Python. Let me check the tools available. There's a function called generate_mcp_client_server_code that takes a natural-language specification and returns a Python file. So I need to use that.

First, I need to formulate the query for the function. The user asked for an MCP server, so the query should specify that. I should describe what the server needs to do. Maybe something like handling connections, processing messages, and sending responses.

I should make sure the query is clear enough for the function to generate the correct code. The parameters for the function require a "query" string. So I'll construct that string to indicate the server's requirements.

Once I call the function with this query, it should return the Python code. Then I can present that code to the user as the answer. I don't need to use any other tools since this function is designed for generating the code based on the specification.
</think>
Tool Calls:
  generate_mcp_client_server_code (3ef4b556-01f0-4b54-aba0-62df08c7a83f)
 Call ID: 3ef4b556-01f0-4b54-aba0-62df08c7a83f
  Args:
    query: Implement an MCP server that handles TCP connections, processes incoming messages, and sends responses back to clients.
```

* What the SLM returns finally (it's certainly not perfect - because the coding model is an SLM - but it's still demonstrating the capabilities)

````text
<think>
Okay, the user asked for an MCP server in Python, and I provided a Flask-based implementation. Let me check if there's anything else they might need. The code uses Flask and the mcp.server module, so they'll need to have those installed. Maybe I should mention the dependencies or provide instructions on how to run the server. Also, the response includes error handling for MCP errors and general exceptions. I think that's thorough. The user might also benefit from an example request, but since they didn't ask for that, maybe it's better to keep it concise. The answer seems complete as is.
</think>

I can answer without using any more tools. I'll use the user's language to answer.
Here's a simple MCP server implementation in Python using Flask:

```python
from flask import Flask, jsonify, request
from mcp.server import Server
from mcp.types import McpError
import json

app = Flask(__name__)
mcp_server = Server(app)

@app.route('/', methods=['POST'])
def handle_request():
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "Invalid request data"}), 400

        method = getattr(mcp_server, request_data['method'])
        response = method(request_data['params'])
        return jsonify(response), 200
    except McpError as e:
        return jsonify({"error": str(e)}), e.code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
```

This server listens on port 5000 by default and handles incoming requests using the Flask web framework. It forwards the request to the corresponding method in the `mcp_server` instance based on the `method` field in the JSON-RPC request. The server responds with a JSON object containing the result or an error message, depending on the outcome of the method execution.

````

## Limitations

* Note that smaller models like `qwen:1.7b` with *1.7b* as well as *4b* and *7b* models are very basic and limited in understanding and working on solutions
* The user experience with `qwen:1.7b` is pretty much bad when using it during a conversation - it's only for demoing purposes

## Devs

* If you change something in the code/container folders, otherwise content will be cached and not reflected

```bash
docker compose build
```

* While answers are generate you'll be able to see resource consumption of the ollama models

```bash
docker exec -it mcp_demo-ollama-1 ollama ps
NAME          ID              SIZE      PROCESSOR    UNTIL              
qwen3:1.7b    8f68893c685c    6.4 GB    100% CPU     3 minutes from now
```

## Sources

* `https://modelcontextprotocol.io/llms-full.txt`
* `https://langchain-ai.github.io/langgraph/agents/agents/`
