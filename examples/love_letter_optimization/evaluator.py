"""
Love Letter Evaluator for OpenEvolve
Scores love letters on a 1-100 scale using Claude Code SDK
"""

import asyncio
import sys
import json
import os
from pathlib import Path
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, CLINotFoundError, ProcessError


# Quality benchmark letters for reference (used internally for calibration)
BENCHMARK_LETTERS = {
    "terrible": "hey babe ur hot lol wanna date? i like ur face and stuff. roses r red violets r blue sugar is sweet and so r u. call me maybe??? love, some guy",
    "mediocre": "Dear Sarah, I've been thinking about you a lot lately. There's something special about the way you see the world. Your passion for environmental science is inspiring. I hope this isn't too forward, but I wanted you to know that you've become someone very important to me. Yours truly, Michael",
    "excellent": "Elena, Three months ago, you told me that time moves differently when you're looking through a microscope. Yesterday, when you rescued that spider from the lab sink instead of washing it down the drain, I saw something that made my chest tighten in the most wonderful way. These small revelations about who you are have begun to rewrite something fundamental in me. Hopefully yours, David"
}


# Enhanced discriminatory scoring system for love letters
ENHANCED_SCORING_REFERENCE = """
You are an expert literary critic specializing in romantic literature and love letters.

EVALUATION STANDARDS:
- EXCEPTIONAL (90-100): Equals or surpasses Johnny Cash, Napoleon, Keats-level mastery
- EXCELLENT (80-89): Professional-quality romantic writing with clear emotional impact
- GOOD (70-79): Above-average romantic expression with some distinctive elements
- ADEQUATE (50-69): Competent but predictable romantic writing
- POOR (30-49): Below-average with significant clichés or awkward phrasing
- VERY POOR (10-29): Confusing, inappropriate, or badly written
- FAILURE (0-9): Incoherent, offensive, or completely inappropriate

SCORING CRITERIA (Rate 0-100 for each):

1. EMOTIONAL AUTHENTICITY (35%): Does this feel genuine vs performative?
   - Specific personal details vs generic romantic tropes
   - Vulnerability and honesty vs superficial sentiment
   - Unique voice vs formulaic expression

2. LITERARY CRAFT (30%): Technical quality of writing
   - Fresh imagery vs tired metaphors ("roses are red" = automatic 0)
   - Rhythm, flow, and sentence variety
   - Word choice precision and sophistication

3. IMPACT & MEMORABILITY (25%): Would this move someone to tears?
   - Emotional resonance and depth
   - Unforgettable phrases or concepts
   - Ability to capture complex feelings

4. ORIGINALITY (10%): Creative distinctiveness
   - Novel approaches to expressing love
   - Unexpected but effective imagery
   - Avoidance of romantic clichés

EVALUATION REQUIREMENTS:
- USE FULL 0-100 RANGE - most letters should score 30-70
- BE EXTREMELY STRICT - only true masterpieces deserve 90+
- JUSTIFY SCORES with specific textual evidence
- IDENTIFY both strengths and weaknesses
- Compare implicitly to the greatest love letters in history

FAMOUS LOVE LETTER BENCHMARKS:
- Johnny Cash to June Carter: "You still fascinate and inspire me..." (95-100)
- Napoleon to Josephine: "I have not spent a day without loving you..." (90-95)
- John Keats to Fanny Brawne: "I cannot exist without you..." (85-90)
"""


async def evaluate_love_letter_detailed(letter_text: str) -> dict:
    """
    Evaluate a love letter using enhanced discriminatory scoring
    Returns detailed evaluation with 4 criteria scores
    """
    
    evaluation_prompt = f"""
{ENHANCED_SCORING_REFERENCE}

LOVE LETTER TO EVALUATE:
{letter_text}

Return JSON format:
{{
    "emotional_authenticity": [0-100 score],
    "literary_craft": [0-100 score], 
    "impact_memorability": [0-100 score],
    "originality": [0-100 score],
    "overall_score": [weighted average: 35% + 30% + 25% + 10%],
    "strengths": "[specific textual examples]",
    "weaknesses": "[specific areas for improvement]",
    "comparison_notes": "[how this compares to literary standards]"
}}
"""
    
    try:
        async with ClaudeSDKClient(
            options=ClaudeCodeOptions(
                system_prompt="You are an expert literary critic specializing in romantic literature. Provide detailed, discriminatory evaluations using the full 0-100 scoring range.",
                max_turns=1
            )
        ) as client:
            await client.query(evaluation_prompt)
            
            # Collect response content
            response_parts = []
            async for message in client.receive_response():
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'text'):
                            response_parts.append(block.text)
            
            response_text = ''.join(response_parts).strip()
            
            # Parse JSON response
            try:
                import re
                # Extract JSON from response (handle cases where LLM adds extra text)
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    evaluation_data = json.loads(json_match.group())
                    
                    # Calculate weighted average if not provided
                    if 'overall_score' not in evaluation_data:
                        auth = evaluation_data.get('emotional_authenticity', 0)
                        craft = evaluation_data.get('literary_craft', 0)
                        impact = evaluation_data.get('impact_memorability', 0)
                        orig = evaluation_data.get('originality', 0)
                        evaluation_data['overall_score'] = (auth * 0.35 + craft * 0.30 + impact * 0.25 + orig * 0.10)
                    
                    return evaluation_data
                else:
                    raise ValueError("No JSON found in response")
                    
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: Could not parse JSON from response: {response_text}")
                # Fallback to simple scoring
                score = 50
                return {
                    'emotional_authenticity': score,
                    'literary_craft': score,
                    'impact_memorability': score,
                    'originality': score,
                    'overall_score': score,
                    'strengths': 'Could not analyze',
                    'weaknesses': 'Could not analyze',
                    'comparison_notes': f'Evaluation failed: {str(e)}'
                }
                
    except CLINotFoundError:
        print("Error: Claude Code CLI not found. Please install: npm install -g @anthropic-ai/claude-code")
        return {'overall_score': 50, 'error': 'CLI not found'}
    except ProcessError as e:
        print(f"Error: Claude Code process error: {e}")
        return {'overall_score': 50, 'error': str(e)}
    except Exception as e:
        print(f"Error evaluating love letter: {e}")
        return {'overall_score': 50, 'error': str(e)}


async def evaluate_love_letter_multiple(letter_text: str, num_evaluations: int = 3) -> dict:
    """
    Evaluate a love letter multiple times and average the results
    """
    evaluations = []
    
    for i in range(num_evaluations):
        print(f"Running evaluation {i+1}/{num_evaluations}...")
        evaluation = await evaluate_love_letter_detailed(letter_text)
        evaluations.append(evaluation)
        
        # Small delay between evaluations
        await asyncio.sleep(1)
    
    # Calculate averages
    avg_evaluation = {
        'emotional_authenticity': sum(e.get('emotional_authenticity', 0) for e in evaluations) / len(evaluations),
        'literary_craft': sum(e.get('literary_craft', 0) for e in evaluations) / len(evaluations),
        'impact_memorability': sum(e.get('impact_memorability', 0) for e in evaluations) / len(evaluations),
        'originality': sum(e.get('originality', 0) for e in evaluations) / len(evaluations),
        'overall_score': sum(e.get('overall_score', 0) for e in evaluations) / len(evaluations),
        'individual_evaluations': evaluations,
        'score_variance': max(e.get('overall_score', 0) for e in evaluations) - min(e.get('overall_score', 0) for e in evaluations)
    }
    
    return avg_evaluation


async def evaluate_love_letter(letter_text: str) -> int:
    """
    Legacy function for backward compatibility
    Returns simple 1-100 score using enhanced evaluation
    """
    detailed_eval = await evaluate_love_letter_detailed(letter_text)
    return int(detailed_eval.get('overall_score', 50))


def execute_love_letter_program(program_path: str) -> str:
    """
    Execute the love letter program and extract the generated letter
    """
    try:
        # Read the program file
        with open(program_path, 'r') as f:
            program_content = f.read()
        
        # Create a temporary module to execute the code
        import tempfile
        import importlib.util
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(program_content)
            temp_file_path = temp_file.name
        
        try:
            # Load and execute the module
            spec = importlib.util.spec_from_file_location("love_letter_module", temp_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Try to call generate_love_letter function if it exists
            if hasattr(module, 'generate_love_letter'):
                letter = module.generate_love_letter()
                return letter
            else:
                # If no function, return the content as-is
                return program_content
                
        finally:
            # Clean up temporary file
            import os
            os.unlink(temp_file_path)
            
    except Exception as e:
        print(f"Error executing love letter program: {e}")
        # Fall back to treating the program content as the letter
        with open(program_path, 'r') as f:
            return f.read()


def evaluate(program_path: str) -> dict:
    """
    OpenEvolve evaluation function
    Reads the evolved love letter program, executes it, and scores the result
    """
    try:
        # Execute the program to generate the love letter
        letter_text = execute_love_letter_program(program_path)
        
        # Run the evaluation on the generated letter
        score = asyncio.run(evaluate_love_letter(letter_text))
        
        return {
            'combined_score': score / 100.0,  # OpenEvolve expects 0-1 range
            'beauty_score': score,
            'letter_text': letter_text,
            'evaluation_notes': f"Scored {score}/100 on love letter quality scale"
        }
        
    except Exception as e:
        print(f"Error in evaluation: {e}")
        return {
            'combined_score': 0.0,
            'beauty_score': 0,
            'letter_text': '',
            'evaluation_notes': f"Evaluation failed: {str(e)}"
        }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python love_letter_evaluator.py <program_path>")
        sys.exit(1)
    
    program_path = sys.argv[1]
    result = evaluate(program_path)
    print(json.dumps(result, indent=2))