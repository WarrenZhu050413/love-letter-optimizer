#!/usr/bin/env python3
"""
Setup script for Love Letter Optimizer using Claude Code SDK
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"⚙️  {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Command: {cmd}")
        print(f"Error: {e.stderr}")
        return None


def main():
    print("🚀 Setting up Love Letter Optimizer with Claude Code SDK\n")
    
    # Check if we're in the right directory
    if not Path("openevolve").exists():
        print("❌ Error: Please run this script from the love-letter-optimizer directory")
        sys.exit(1)
    
    # Install Claude Code SDK
    print("📦 Installing Claude Code SDK...")
    run_command("pip install claude-code-sdk", "Claude Code SDK installation")
    
    # Install OpenEvolve dependencies
    print("📦 Installing OpenEvolve dependencies...")
    run_command("pip install -e .", "OpenEvolve installation")
    
    # Check if Claude CLI is available
    print("🔍 Checking Claude CLI availability...")
    result = run_command("which claude", "Claude CLI check")
    if result:
        print(f"✅ Claude CLI found at: {result.strip()}")
    else:
        print("⚠️  Claude CLI not found. You may need to install it:")
        print("   npm install -g @anthropic-ai/claude-code")
    
    # Create output directory
    output_dir = Path("love_letter_outputs")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Created output directory: {output_dir}")
    
    # Test the evaluator
    print("🧪 Testing love letter evaluator...")
    test_result = run_command(
        f"python love_letter_evaluator.py initial_love_letter.py",
        "Love letter evaluator test"
    )
    if test_result:
        print("✅ Evaluator test passed")
        print(f"Test result: {test_result}")
    
    print("\n🎉 Setup complete! You can now run the love letter optimizer:")
    print("\n🔥 To start evolution:")
    print("python openevolve-run.py initial_love_letter.py love_letter_evaluator.py --config love_letter_config.yaml --iterations 200")
    
    print("\n📊 Key files created:")
    print("  • initial_love_letter.py - Starting template")
    print("  • love_letter_evaluator.py - Claude-based scoring (1-100)")
    print("  • love_letter_config.yaml - Evolution configuration")
    print("  • openevolve/llm/claude_code.py - Claude Code SDK integration")
    
    print("\n💡 The system will evolve prompts to generate increasingly beautiful love letters!")
    print("   Best results will be saved in love_letter_outputs/")


if __name__ == "__main__":
    main()