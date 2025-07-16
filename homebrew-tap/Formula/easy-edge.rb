class EasyEdge < Formula
  desc "A simple Ollama-like tool for running LLMs locally"
  homepage "https://github.com/criminact/easy-edge"
  url "https://github.com/criminact/easy-edge/archive/v1.0.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"  # You'll need to calculate this
  license "MIT"
  head "https://github.com/criminact/easy-edge.git", branch: "main"

  depends_on "python@3.11"

  def install
    # Create models directory
    (prefix/"models").mkpath
    
    # Install Python dependencies
    system "pip3", "install", "-r", "requirements.txt"
    
    # Install the main script
    bin.install "easy_edge.py" => "easy-edge"
    
    # Make it executable
    chmod 0755, bin/"easy-edge"
    
    # Create a symlink for the models directory in user's home
    # This allows users to access models from anywhere
    system "ln", "-sf", prefix/"models", "#{ENV['HOME']}/.easy-edge-models"
  end

  def post_install
    # Create a default config if it doesn't exist
    config_file = "#{ENV['HOME']}/.easy-edge-models/config.json"
    unless File.exist?(config_file)
      File.write(config_file, {
        models: {},
        default_model: nil,
        settings: {
          max_tokens: 2048,
          temperature: 0.7,
          top_p: 0.9
        }
      }.to_json)
    end
  end

  test do
    # Test that the help command works
    system "#{bin}/easy-edge", "--help"
    
    # Test that the list command works
    system "#{bin}/easy-edge", "list"
  end

  def caveats
    <<~EOS
      Easy Edge has been installed!
      
      Models will be stored in: ~/.easy-edge-models/
      
      Quick start:
        # Download a model
        easy-edge pull --url https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-qat-q4_0.gguf
        
        # Run interactive chat
        easy-edge run gemma-3-1b-it-qat-q4_0-gguf --interactive
        
      For more information, visit: https://github.com/criminact/easy-edge
    EOS
  end
end 