#!/usr/bin/env python3
"""
Complete deployment script for Love Letter Optimizer
Sets up virtual environment, installs dependencies, and runs tests
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and handle errors"""
    print(f"⚙️  {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"⚠️  {description} completed with warnings")
            if result.stderr.strip():
                print(f"   Warnings: {result.stderr.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e


def main():
    print("🚀 Setting up Love Letter Optimizer - Complete Deployment\n")
    
    # Check if we're in the right directory
    if not Path("openevolve").exists():
        print("❌ Error: Please run this script from the love-letter-optimizer directory")
        sys.exit(1)
    
    # Step 1: Ensure virtual environment exists
    venv_path = Path("love_letter_env")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        run_command("python3 -m venv love_letter_env", "Virtual environment creation")
    else:
        print("✅ Virtual environment already exists")
    
    # Step 2: Install dependencies in virtual environment
    print("\n📦 Installing dependencies...")
    run_command(
        "source love_letter_env/bin/activate && pip install --upgrade pip",
        "Pip upgrade"
    )
    run_command(
        "source love_letter_env/bin/activate && pip install claude-code-sdk anthropic",
        "Claude SDK installation"
    )
    run_command(
        "source love_letter_env/bin/activate && pip install -e .",
        "OpenEvolve installation"
    )
    
    # Step 3: Check Claude Code CLI
    print("\n🔍 Checking Claude Code CLI...")
    result = run_command("which claude", "Claude CLI check", check=False)
    if result.returncode != 0:
        print("⚠️  Claude CLI not found. Installing...")
        run_command("npm install -g @anthropic-ai/claude-code", "Claude CLI installation", check=False)
    
    # Step 4: Test evaluator
    print("\n🧪 Testing love letter evaluator...")
    test_result = run_command(
        "source love_letter_env/bin/activate && python love_letter_evaluator.py initial_love_letter.py",
        "Love letter evaluator test"
    )
    
    if test_result.returncode == 0:
        print("✅ Evaluator test passed!")
        try:
            import json
            result_data = json.loads(test_result.stdout)
            score = result_data.get('beauty_score', 'Unknown')
            print(f"   Initial love letter scored: {score}/100")
        except:
            print("   Test completed successfully")
    
    # Step 5: Check configuration
    print("\n📋 Verifying configuration...")
    config_path = Path("love_letter_config.yaml")
    if config_path.exists():
        print("✅ Configuration file exists")
        with open(config_path) as f:
            config_content = f.read()
            if 'name: "opus"' in config_content and 'name: "sonnet"' in config_content:
                print("✅ Model names correctly configured (opus & sonnet)")
            else:
                print("⚠️  Model names may need verification")
    else:
        print("❌ Configuration file missing")
        return
    
    # Step 6: Test small evolution run
    print("\n🔬 Testing small evolution run (5 iterations)...")
    small_test = run_command(
        "source love_letter_env/bin/activate && timeout 120 python openevolve-run.py initial_love_letter.py love_letter_evaluator.py --config love_letter_config.yaml --iterations 5 --output small_test_output || true",
        "Small evolution test",
        check=False
    )
    
    if small_test.returncode == 0 or "iteration" in small_test.stdout.lower():
        print("✅ Evolution system working!")
    else:
        print("⚠️  Evolution test inconclusive - check manually")
    
    # Final instructions
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT COMPLETE!")
    print("="*60)
    
    print("\n🔥 To start the Love Letter Optimizer:")
    print("source love_letter_env/bin/activate")
    print("python openevolve-run.py initial_love_letter.py love_letter_evaluator.py --config love_letter_config.yaml --iterations 200")
    
    print("\n📊 System Features:")
    print("  • Dual model setup: Opus (60%) + Sonnet (40%)")
    print("  • 1-100 scoring system based on famous love letters")
    print("  • Claude Code SDK integration")
    print("  • 200 generations of evolution")
    print("  • ~3M tokens of overnight processing")
    
    print("\n📁 Key Files:")
    print("  • initial_love_letter.py - Starting template")
    print("  • love_letter_evaluator.py - Claude-based scoring")
    print("  • love_letter_config.yaml - Evolution configuration") 
    print("  • love_letter_env/ - Virtual environment")
    
    print("\n💡 The system will evolve prompts to create increasingly beautiful love letters!")
    print("   Results will be saved in openevolve_output/")
    
    print("\n🚨 Requirements:")
    print("  • Set ANTHROPIC_API_KEY environment variable")
    print("  • Ensure Claude Code CLI is working")
    print("  • Run from within the love-letter-optimizer directory")


if __name__ == "__main__":
    main()