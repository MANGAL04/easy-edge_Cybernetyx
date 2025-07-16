from setuptools import setup, find_packages

setup(
    name="easy-edge",
    version="0.1.0",
    description="A simple Ollama-like tool for running LLMs locally",
    author="Easy Edge Team",
    packages=find_packages(),
    install_requires=[
        "llama-cpp-python==0.2.11",
        "requests==2.32.4",
        "tqdm==4.67.1",
        "click==8.1.7",
        "rich==13.7.0",
        "huggingface-hub==0.33.4",
    ],
    entry_points={
        "console_scripts": [
            "easy-edge=easy_edge:cli",
        ],
    },
    python_requires=">=3.11",
) 