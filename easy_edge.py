#!/usr/bin/env python3
"""
Easy Edge - A simple Ollama-like tool for running LLMs locally
"""

import os
import sys
import json
import click
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt
from rich.panel import Panel
from tqdm import tqdm
import huggingface_hub

# Try to import llama-cpp-python
try:
    from llama_cpp import Llama
except ImportError:
    print("Error: llama-cpp-python not installed. Run: pip install llama-cpp-python")
    sys.exit(1)

console = Console()

class EasyEdge:
    def __init__(self, models_dir: str = None):
        # Check for Homebrew installation
        if models_dir is None:
            homebrew_models = Path.home() / ".easy-edge-models"
            if homebrew_models.exists():
                models_dir = str(homebrew_models)
            else:
                models_dir = "models"
        
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.config_file = self.models_dir / "config.json"
        self.load_config()
        
    def load_config(self):
        """Load or create configuration file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "models": {},
                "default_model": None,
                "settings": {
                    "max_tokens": 2048,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_model_path(self, model_name: str) -> Optional[Path]:
        """Get the local path for a model"""
        if model_name in self.config["models"]:
            model_path = self.models_dir / self.config["models"][model_name]["filename"]
            if model_path.exists():
                return model_path
        return None
    
    def download_model(self, model_url: str) -> Path:
        """Download a model from URL using Hugging Face hub"""
        try:
            # Extract repo_id and filename from URL
            # URL format: https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-q4_0.gguf
            if "huggingface.co" in model_url:
                parts = model_url.split("/")
                repo_id = f"{parts[3]}/{parts[4]}"
                filename_in_repo = parts[-1]
                
                # Extract model name from repo_id (last part)
                model_name = repo_id.split("/")[-1]
                
                console.print(f"Detected Hugging Face repo: {repo_id}, file: {filename_in_repo}")
                console.print(f"Model name: {model_name}")
                
                filename = f"{model_name}.gguf"
                model_path = self.models_dir / filename
                
                if model_path.exists():
                    console.print(f"Model {model_name} already exists at {model_path}")
                    return model_path
                
                # Use Hugging Face download with progress
                with console.status(f"Downloading {model_name} from Hugging Face..."):
                    downloaded_path = huggingface_hub.hf_hub_download(
                        repo_id=repo_id,
                        filename=filename_in_repo,
                        local_dir=self.models_dir,
                        local_dir_use_symlinks=False
                    )
                
                # Rename to our standard format
                if Path(downloaded_path).exists():
                    Path(downloaded_path).rename(model_path)
                
                # Update config
                self.config["models"][model_name] = {
                    "filename": filename,
                    "repo_id": repo_id,
                    "original_filename": filename_in_repo,
                    "size": model_path.stat().st_size
                }
                self.save_config()
                
                console.print(f"✅ Model {model_name} downloaded successfully!")
                return model_path
            else:
                # For non-Hugging Face URLs, fall back to requests
                console.print("Non-Hugging Face URL detected, using direct download...")
                console.print("❌ Please provide a Hugging Face URL for automatic model name extraction")
                raise ValueError("Only Hugging Face URLs are supported for automatic model name extraction")
                
        except Exception as e:
            console.print(f"❌ Error downloading model: {e}")
            raise
    
    def download_from_huggingface(self, repo_id: str, filename: str) -> Path:
        """Download a model from Hugging Face"""
        # Extract model name from repo_id (last part)
        model_name = repo_id.split("/")[-1]
        
        local_filename = f"{model_name}.gguf"
        model_path = self.models_dir / local_filename
        
        if model_path.exists():
            console.print(f"Model {model_name} already exists at {model_path}")
            return model_path
        
        console.print(f"Downloading {model_name} from Hugging Face ({repo_id})...")
        
        try:
            with console.status(f"Downloading {model_name} from Hugging Face..."):
                huggingface_hub.hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    local_dir=self.models_dir,
                    local_dir_use_symlinks=False
                )
            
            # Rename to our standard format
            downloaded_path = self.models_dir / filename
            if downloaded_path.exists():
                downloaded_path.rename(model_path)
            
            # Update config
            self.config["models"][model_name] = {
                "filename": local_filename,
                "repo_id": repo_id,
                "original_filename": filename,
                "size": model_path.stat().st_size
            }
            self.save_config()
            
            console.print(f"✅ Model {model_name} downloaded successfully!")
            return model_path
            
        except Exception as e:
            console.print(f"❌ Error downloading model: {e}")
            raise
    
    def list_models(self):
        """List all available models"""
        if not self.config["models"]:
            console.print("No models installed. Use 'easy-edge pull <model>' to download a model.")
            return
        
        console.print("\n[bold]Installed Models:[/bold]")
        for name, info in self.config["models"].items():
            size_mb = info.get("size", 0) / (1024 * 1024)
            status = "✅" if (self.models_dir / info["filename"]).exists() else "❌"
            console.print(f"  {status} {name} ({size_mb:.1f} MB)")
    
    def run_model(self, model_name: str, prompt: str = None, interactive: bool = False):
        """Run a model for inference"""
        model_path = self.get_model_path(model_name)
        
        if not model_path:
            console.print(f"❌ Model '{model_name}' not found. Use 'easy-edge pull <model>' to download it.")
            return
        
        try:
            console.print(f"Loading model {model_name}...")
            llm = Llama(
                model_path=str(model_path),
                n_ctx=2048,
                n_threads=os.cpu_count()
            )
            
            if interactive:
                self.interactive_chat(llm, model_name)
            else:
                if not prompt:
                    prompt = Prompt.ask("Enter your prompt")
                
                response = llm(
                    prompt,
                    max_tokens=self.config["settings"]["max_tokens"],
                    temperature=self.config["settings"]["temperature"],
                    top_p=self.config["settings"]["top_p"],
                    stop=["User:", "\n\n"]
                )
                
                console.print(Panel(response["choices"][0]["text"], title="Response"))
                
        except Exception as e:
            console.print(f"❌ Error running model: {e}")
    
    def interactive_chat(self, llm, model_name: str):
        """Interactive chat mode"""
        console.print(f"\n[bold]Chat with {model_name}[/bold] (type 'quit' to exit)")
        console.print("=" * 50)
        
        while True:
            try:
                user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input.strip():
                    continue
                
                console.print("\n[bold green]Assistant[/bold green]")
                with console.status("Thinking..."):
                    response = llm(
                        user_input,
                        max_tokens=self.config["settings"]["max_tokens"],
                        temperature=self.config["settings"]["temperature"],
                        top_p=self.config["settings"]["top_p"],
                        stop=["User:", "\n\n"]
                    )
                
                console.print(response["choices"][0]["text"])
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"❌ Error: {e}")
        
        console.print("\nGoodbye!")

@click.group()
@click.option('--models-dir', default='models', help='Directory to store models')
@click.pass_context
def cli(ctx, models_dir):
    """Easy Edge - Run LLMs locally like Ollama"""
    ctx.ensure_object(dict)
    ctx.obj['easy_edge'] = EasyEdge(models_dir)

@cli.command()
@click.option('--url', help='Hugging Face URL to download the model')
@click.option('--repo-id', help='Hugging Face repository ID')
@click.option('--filename', help='Filename in the repository')
@click.pass_context
def pull(ctx, url, repo_id, filename):
    """Download a model (model name is automatically extracted)"""
    easy_edge = ctx.obj['easy_edge']
    
    if url:
        easy_edge.download_model(url)
    elif repo_id and filename:
        easy_edge.download_from_huggingface(repo_id, filename)
    else:
        console.print("❌ Please provide either --url or both --repo-id and --filename")
        console.print("\nExample:")
        console.print("  easy-edge pull --url https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-q4_0.gguf")
        console.print("  easy-edge pull --repo-id TheBloke/Llama-2-7B-Chat-GGUF --filename llama-2-7b-chat.Q4_K_M.gguf")

@cli.command()
@click.pass_context
def list(ctx):
    """List installed models"""
    easy_edge = ctx.obj['easy_edge']
    easy_edge.list_models()

@cli.command()
@click.argument('model_name')
@click.option('--prompt', '-p', help='Prompt to send to the model')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive chat mode')
@click.pass_context
def run(ctx, model_name, prompt, interactive):
    """Run a model"""
    easy_edge = ctx.obj['easy_edge']
    easy_edge.run_model(model_name, prompt, interactive)

@cli.command()
@click.argument('model_name')
@click.pass_context
def remove(ctx, model_name):
    """Remove a model"""
    easy_edge = ctx.obj['easy_edge']
    
    if model_name not in easy_edge.config["models"]:
        console.print(f"❌ Model '{model_name}' not found")
        return
    
    model_path = easy_edge.get_model_path(model_name)
    if model_path and model_path.exists():
        model_path.unlink()
        console.print(f"✅ Removed model file: {model_path}")
    
    del easy_edge.config["models"][model_name]
    easy_edge.save_config()
    console.print(f"✅ Removed model '{model_name}' from configuration")

if __name__ == '__main__':
    cli() 