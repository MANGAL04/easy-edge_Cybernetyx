class EasyEdge < Formula
  desc "A simple Ollama-like tool for running LLMs locally"
  homepage "https://github.com/yourusername/easy-edge"
  url "https://github.com/yourusername/easy-edge/archive/v1.0.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"
  license "MIT"

  depends_on "python@3.9"

  def install
    system "pip3", "install", "-r", "requirements.txt"
    bin.install "easy_edge.py" => "easy-edge"
  end

  test do
    system "#{bin}/easy-edge", "--help"
  end
end 