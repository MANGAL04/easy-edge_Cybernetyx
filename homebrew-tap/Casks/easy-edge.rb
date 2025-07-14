cask "easy-edge" do
  version "1.0.0"
  sha256 "YOUR_BINARY_SHA256_HERE"  # You'll need to calculate this for the binary

  url "https://github.com/yourusername/easy-edge/releases/download/v#{version}/easy-edge-macos"
  name "Easy Edge"
  desc "A simple Ollama-like tool for running LLMs locally"
  homepage "https://github.com/yourusername/easy-edge"

  livecheck do
    url :url
    strategy :github_latest
  end

  binary "easy-edge-macos", target: "easy-edge"

  postflight do
    # Create models directory
    system_command "mkdir", args: ["-p", "#{ENV['HOME']}/.easy-edge-models"]
    
    # Create default config
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

  uninstall_postflight do
    # Clean up models directory (ask user first)
    models_dir = "#{ENV['HOME']}/.easy-edge-models"
    if Dir.exist?(models_dir)
      puts "Easy Edge models directory found at: #{models_dir}"
      puts "Do you want to remove it? (y/N)"
      response = STDIN.gets.chomp.downcase
      if response == 'y' || response == 'yes'
        system_command "rm", args: ["-rf", models_dir]
        puts "Models directory removed."
      else
        puts "Models directory preserved at: #{models_dir}"
      end
    end
  end

  caveats <<~EOS
    Easy Edge has been installed!
    
    Models will be stored in: ~/.easy-edge-models/
    
    Quick start:
      # Download a model
      easy-edge pull --url https://huggingface.co/google/gemma-3-1b-it-qat-q4_0-gguf/resolve/main/gemma-3-1b-it-qat-q4_0.gguf
      
      # Run interactive chat
      easy-edge run gemma-3-1b-it-qat-q4_0-gguf --interactive
      
    For more information, visit: https://github.com/yourusername/easy-edge
  EOS
end 