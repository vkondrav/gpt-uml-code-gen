import openai
import json
import tiktoken
import os
from halo import Halo
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--package", type = str, required = True, help = "package to create")
parser.add_argument("-s", "--samples", type = str, default = "samples", help = "path to sample files directory")
parser.add_argument("-dm", "--diagram", type = str, default = "diagram", help = "path to diagram")
parser.add_argument("-d", "--debug", action = "store_true", help = "enable debug mode")

args = parser.parse_args()

package = args.package
diagram_path = args.diagram
samples_path = args.samples
debug_mode = args.debug

openai.api_key = os.getenv("OPEN_AI_KEY")

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(diagram_path, "r") as file:
    diagram = file.read()

def get_sample_set(dir_path, rel_path = "", files_info = ""):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isdir(file_path):
            files_info = get_sample_set(file_path, os.path.join(rel_path, filename), files_info)
        elif os.path.isfile(file_path):
            with open(file_path, "r") as file:
                file_path = os.path.join(rel_path, filename).replace(filename, "")
                files_info += f"//file_name: {filename}\n//file_path: {file_path}\n{file.read()}\n\n"
    return files_info

sample_set = get_sample_set(samples_path).replace("sample-package", package)

rules = """
/**
Rules

Every class must be created with its test suite.
If not one of fragment, viewmodel or repository create a sample class.
Assume a class has no dependencies unless explicitly stated.

UML

() denotes a shorthand. 
Example: sampleRepository (SR) means SR now refers to sampleRepository.

--> denotes a dependency. 
Example: sampleViewModel --> sampleRepository means sampleViewModel dependends on sampleRepository. 
Example: sampleFragment --> sampleViewModel means sampleFragment uses sampleViewModel.

+ denotes create command.
Example: + sample repository means create a sample repository.

- denotes that a class aleady exists and does not need to be created. it can however be a dependency.

Format

Format the response into a JSON array with a structure [{"file_name": "file_name.kt", "file_path": "file_path", "content": "sample_content"}].
The whole response should only be a valid JSON array and nothing else.
Do not create sample classes.
**/

"""

prompt = "//Kotlin\n\n" + sample_set + rules + "Create classes from the following diagram\n\n" + diagram

def num_tokens_from_string(string: str, model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

model = "text-davinci-003"
max_request_tokens = 4097

num_tokens = num_tokens_from_string(prompt, model)
max_tokens = max_request_tokens - num_tokens

if debug_mode:
    print(f"MAX TOKENS: {max_tokens}")
    print("\n")

if debug_mode:
    print("PROMPT")
    print("-------------------")
    print(prompt)
    print("\n")

spinner = Halo(text = "Generating Code", spinner = "dots")
spinner.start()

response = openai.Completion.create(
    model = model, 
    prompt = prompt,
    temperature = 0,
    max_tokens = max_tokens
)

spinner.stop()

if debug_mode:
    print("RESPONSE")
    print("-------------------")
    print(response)
    print("\n")

code_gen = json.loads(response["choices"][0]["text"])

if debug_mode:
    print("FORMATTED RESPONSE")
    print("-------------------")
    print(json.dumps(code_gen, indent = 4))

for file in code_gen:

    path = file["file_path"]
    name = file["file_name"]

    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + "/" + name, 'w+') as f:
        print(file["content"], file = f)