import time
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from src.memory_manager import MemoryManager
from src.gpt import ChatGPT
from src.memory_config import MemoryConfig

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)

# Create the objects required for the service
memory_manager = MemoryManager()
chatGPT = ChatGPT()


@app.route("/", methods=["GET"])
def get_details():
    try:
        # Returns the details of the service
        loaded_memory = []
        for m in memory_manager.loaded_memory:
            loaded_memory.append(
                {
                    "name": m.name,
                    "config": MemoryConfig(m.name).__dict__(),
                }
            )
        return jsonify(
            {
                "loaded_memory": loaded_memory,
                "max_loaded_memory": memory_manager.max_loaded,
            }
        )
    except Exception as e:
        return jsonify({"error": "Error getting details: " + str(e)}), 500


@app.route("/", methods=["POST"])
def create_completion():
    prompt = ""
    system_prompt = ""
    model = "gpt-3.5-turbo-16k"

    # Creates a completion
    try:
        data = request.get_json()

        if "prompt" in data:
            prompt = data["prompt"]
            chatGPT.check_moderation(prompt)

        if "system_prompt" in data:
            system_prompt = data["system_prompt"]
            chatGPT.check_moderation(system_prompt)

        if "name" not in data:
            if "model" in data:
                model = data["model"]
            response = chatGPT.get_no_mem_response(prompt, system_prompt, model)
            return jsonify(response)

        # Retrieve memory
        name = data["name"]
        config = MemoryConfig(name)
        memory = memory_manager.get_memory(name)

        response_time = time.time()

        # Generate response
        response = chatGPT.get_response(memory, config, prompt, system_prompt)

        # Add to memory
        memory.add_to_memory(prompt, response, config)
        config.process_completion(time.time() - response_time)

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": "Error generating response:" + str(e)}), 500


@app.route("/image", methods=["POST"])
def create_image():
    n = 1
    size = "256x256"
    response_format = "b64_json"

    try:
        data = request.get_json()
        if "prompt" not in data:
            raise Exception("Prompt not provided.")
        prompt = data["prompt"]

        if "n" in data:
            n = data["n"]
        if "size" in data:
            size = data["size"]
        if "response_format" in data:
            response_format = data["response_format"]

        chatGPT.check_moderation(prompt)
        image = chatGPT.get_image(prompt, n, size, response_format)
        return jsonify(image)
    except Exception as e:
        return jsonify({"error": "Error generating image:" + str(e)}), 500


@app.route("/memory", methods=["GET"])
def get_memories():
    # Returns the list of memory configs
    try:
        configs = MemoryConfig.get_configs()
        return jsonify(configs)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/memory/<name>", methods=["GET"])
def get_memory(name):
    # Returns the specified memory config
    try:
        configs = MemoryConfig.get_configs()
        config = next((c for c in configs if c["name"] == name), None)
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@app.route("/memory", methods=["POST"])
def update_memory() -> Response:
    # Creates or updates a memory config
    try:
        data = request.get_json()
        if "name" not in data:
            raise Exception("Memory name not provided.")
        config = MemoryConfig(data["name"])
        config.update(data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": "Error creating/updating memory: " + str(e)}), 500


if __name__ == "__main__":
    app.run()
