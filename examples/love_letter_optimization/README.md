# Love Letter Optimization

Evolutionary optimization of romantic love letters using OpenEvolve and Claude Code SDK.

## Overview

This example demonstrates using OpenEvolve to evolve increasingly beautiful and authentic love letters through iterative improvement. The system uses a sophisticated 4-criteria evaluation system that scores letters on emotional authenticity, literary craft, impact & memorability, and originality.

## Features

- **Enhanced discriminatory evaluator** with 4-criteria scoring system (0-100 scale)
- **Claude Code SDK integration** for high-quality language model evaluation
- **Quality benchmarks** from terrible to masterpiece level (including Johnny Cash benchmark)
- **Real-time progress monitoring** with comprehensive logging
- **MAP-Elites evolution** with island-based diversity preservation
- **Comprehensive testing suite** with 7 quality levels

## Quick Start

### Prerequisites

1. Ensure you have Claude Code SDK installed and configured
2. Install dependencies:
   ```bash
   pip install anthropic pyyaml asyncio
   ```

### Running Evolution

```bash
# Quick 5-iteration test (recommended first)
python run_quick_test.py

# Full 50-iteration evolution 
python run_full_evolution.py
```

### Testing the Evaluator

```bash
# Test evaluator on 7 quality levels (terrible to masterpiece)
python test_evaluator.py
```

## How It Works

### 1. Initial Program
The system starts with a basic love letter template in `initial_program.py` that generates romantic content.

### 2. Evaluation System
The `evaluator.py` uses Claude to score letters on 4 criteria:
- **Emotional Authenticity (35%)**: Genuine feeling vs. clichéd sentiment
- **Literary Craft (30%)**: Writing quality, imagery, style
- **Impact & Memorability (25%)**: Ability to move and stick with reader
- **Originality (10%)**: Fresh language and unique perspective

### 3. Evolution Process
OpenEvolve uses MAP-Elites algorithm to:
- Generate mutations of the love letter program
- Evaluate each variant using the Claude-based evaluator
- Preserve diversity across complexity and quality dimensions
- Iteratively improve toward more beautiful, authentic letters

### 4. Quality Benchmarks
The system is calibrated against famous love letters:
- **90-100**: Johnny Cash, Napoleon, Keats level mastery
- **80-89**: Professional romantic writing
- **60-79**: Competent with distinctive elements
- **40-59**: Generic but functional
- **20-39**: Clichéd and unoriginal
- **0-19**: Incoherent or offensive

## Files

- **`config.yaml`** - Evolution configuration (50 iterations, Claude model setup)
- **`evaluator.py`** - Enhanced 4-criteria love letter evaluator using Claude Code SDK
- **`initial_program.py`** - Starting love letter template for evolution
- **`test_letters.py`** - Quality test samples from terrible to masterpiece
- **`test_evaluator.py`** - Comprehensive evaluator testing suite
- **`run_quick_test.py`** - 5-iteration validation test
- **`run_full_evolution.py`** - Full 50-iteration evolution
- **`results/`** - Evolution outputs (best letters, logs, checkpoints)

## Results

The system has demonstrated:
- **Score improvements** from 73 → 87 in just 5 iterations
- **Quality evolution** from basic romantic language to sophisticated literary expression
- **Discriminatory evaluation** with 87-point scoring range across quality levels
- **Stable operation** with proper Claude Code SDK integration

Example evolved output achieves sophisticated metaphors like "cathedral of ordinary moments" and "grace breaking through winter clouds" - showing clear literary advancement over the initial template.

## Configuration

The `config.yaml` uses:
- **Single Claude model** (opus) for efficient compute usage
- **MAP-Elites** with complexity and diversity features
- **Island-based evolution** with 3 populations for diversity
- **Checkpointing** every 10 iterations for resumability

## Integration with OpenEvolve

This example showcases:
- **Claude Code SDK integration** in the main OpenEvolve framework
- **Custom evaluation** with sophisticated scoring systems
- **Quality benchmarking** against real-world standards
- **Professional example structure** following OpenEvolve patterns

The Claude Code SDK integration is available system-wide in `openevolve/llm/claude_code.py` for use by other examples.