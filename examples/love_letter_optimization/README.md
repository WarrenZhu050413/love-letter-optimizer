# Love Letter Optimization

This example demonstrates using OpenEvolve to evolve increasingly beautiful and authentic love letters through iterative improvement with a sophisticated 4-criteria evaluation system.

## Problem Description

The task is to evolve a love letter generator that produces romantic content optimized for:

1. **Emotional Authenticity** (35%) - Genuine feeling vs. clichéd sentiment
2. **Literary Craft** (30%) - Writing quality, imagery, and style  
3. **Impact & Memorability** (25%) - Ability to move and resonate with readers
4. **Originality** (10%) - Fresh language and unique perspective

The evaluator uses Claude to score letters on a 0-100 scale, calibrated against famous love letters from Johnny Cash, Napoleon, and Keats.

## Getting Started

To run this example:

```bash
cd examples/love_letter_optimization
python ../../openevolve-run.py initial_program.py evaluator.py --config config.yaml --iterations 50
```

## Algorithm Evolution

### Initial Algorithm

The initial program uses a simple template-based approach to generate romantic content with basic personalization and emotional expression.

### Evolution Results

Through evolutionary optimization, the system has demonstrated:

- **Score improvements** from 73 → 87 in just 5 iterations
- **Quality evolution** from basic romantic language to sophisticated literary expression
- **Advanced metaphors** like "cathedral of ordinary moments" and "grace breaking through winter clouds"
- **Consistent discriminatory evaluation** with 87-point range across quality levels

## Key Innovations

This example showcases several OpenEvolve capabilities:

1. **Claude Code SDK Integration**: Custom LLM integration using Claude for sophisticated natural language evaluation
2. **Multi-criteria Optimization**: Weighted scoring system balancing multiple literary qualities
3. **Quality Benchmarking**: Calibrated against historical love letter masterpieces
4. **Domain-specific Evolution**: Specialized for creative writing and emotional expression

## Technical Implementation

The evaluator (`evaluator.py`) uses:
- Claude Code SDK for natural language assessment
- 4-criteria weighted scoring (35% + 30% + 25% + 10%)
- Quality benchmarks from terrible to masterpiece levels
- Detailed feedback on strengths and weaknesses

The configuration uses:
- Single Claude model (opus) for evaluation
- MAP-Elites algorithm with complexity and diversity features
- Island-based evolution for maintaining population diversity
- 50 iterations with checkpointing every 10 generations

## Results

The evolved algorithm produces love letters with:
- Sophisticated literary devices and metaphors
- Authentic emotional expression over generic sentiment
- Memorable imagery and personal details
- Original language avoiding common romantic clichés

This demonstrates OpenEvolve's ability to optimize creative and subjective domains through sophisticated evaluation systems.