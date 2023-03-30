# GPT UML Code Gen

In this proof of concept project we attempt to teach ChatGPT basic UML to generate code, consume the output and create actual files in a project. The idea is for developers to provide a `schema` of sorts and for ChatGPT to generate some boilerplate code to avoid set up time.

The goal is to go from this prompt

```
+ sign in fragment (SIF)
+ sign up fragment (SUF)
+ authentication viewmodel (AVM)
+ authentication repository (AR)
+ user repository (UR)
- navigation manager (NM)
+ authentication service (AS)
SIF --> AVM
SUF --> AVM
AVM --> AR
AVM --> UR
AVM --> NM
AR --> AS
```

to these files

![this](output.png)

# Setup

Project was tested with [python3](https://www.python.org/downloads/)

```console
pip install openai
pip install openai[datalib]
pip install tiktoken
pip install halo
```

Create/Get your ChatGPT api token [here](https://platform.openai.com/account/api-keys)
and use it here.

```python
openai.api_key = "<API_TOKEN>"
```

Run any script with python
```console
python chat-gpt-uml-kotlin.py
```

Follow the phases of prompt engineering to see how the output changes each time.

# Phase 1
Provide ChatGPT with code templates/samples for the classes that you want to generate. The key is to keep is very simple and avoid any proprietery code.

# Phase 2
Provide ChatGPT with simple UML definitions which should allow us to prompt what we want very quickly and concisenly.

# Phase 3
Change the templates/samples to also provide file names and paths. Ask ChatGPT to format the response to JSON. Consume the JSON output and generate real files using basic python methods.
