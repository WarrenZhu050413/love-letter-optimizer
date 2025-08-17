#!/usr/bin/env python3
"""
Test the enhanced love letter evaluator on various quality letters
"""

import asyncio
import sys
import json
import logging
import time
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from evaluator import evaluate_love_letter_detailed, evaluate_love_letter_multiple
from test_letters import TEST_LETTERS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('evaluator_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def test_single_evaluation():
    """Test single evaluation on all test letters"""
    logger.info("=" * 60)
    logger.info("SINGLE EVALUATION TEST")
    logger.info("=" * 60)
    
    results = []
    
    for i, (name, letter, expected_range) in enumerate(TEST_LETTERS, 1):
        logger.info(f"\n[{i}/{len(TEST_LETTERS)}] Testing: {name} (Expected: {expected_range})")
        logger.info("-" * 40)
        
        start_time = time.time()
        
        try:
            logger.info(f"Starting evaluation for {name}...")
            evaluation = await evaluate_love_letter_detailed(letter)
            elapsed = time.time() - start_time
            
            if 'error' in evaluation:
                logger.error(f"ERROR: {evaluation['error']}")
                results.append({
                    'name': name,
                    'expected_range': expected_range,
                    'actual_score': 0,
                    'error': evaluation['error'],
                    'elapsed_time': elapsed
                })
                continue
                
            score = evaluation.get('overall_score', 0)
            logger.info(f"✓ {name} completed in {elapsed:.1f}s - Score: {score:.1f}")
            logger.info(f"  Emotional Authenticity: {evaluation.get('emotional_authenticity', 0):.1f}")
            logger.info(f"  Literary Craft: {evaluation.get('literary_craft', 0):.1f}")  
            logger.info(f"  Impact & Memorability: {evaluation.get('impact_memorability', 0):.1f}")
            logger.info(f"  Originality: {evaluation.get('originality', 0):.1f}")
            
            if 'strengths' in evaluation:
                logger.info(f"  Strengths: {evaluation['strengths'][:100]}...")
            if 'weaknesses' in evaluation:
                logger.info(f"  Weaknesses: {evaluation['weaknesses'][:100]}...")
                
            results.append({
                'name': name,
                'expected_range': expected_range,
                'actual_score': score,
                'evaluation': evaluation,
                'elapsed_time': elapsed
            })
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"ERROR evaluating {name} after {elapsed:.1f}s: {e}")
            results.append({
                'name': name,
                'expected_range': expected_range,
                'actual_score': 0,
                'error': str(e),
                'elapsed_time': elapsed
            })
    
    return results


async def test_multiple_evaluation():
    """Test multiple evaluation averaging on a few key letters"""
    print("\n" + "=" * 60)
    print("MULTIPLE EVALUATION TEST (3 evaluations each)")
    print("=" * 60)
    
    # Test on terrible, mediocre, excellent, and masterpiece
    test_subset = [TEST_LETTERS[0], TEST_LETTERS[2], TEST_LETTERS[4], TEST_LETTERS[5]]
    
    for name, letter, expected_range in test_subset:
        print(f"\nTesting: {name} (Expected: {expected_range})")
        print("-" * 40)
        
        try:
            evaluation = await evaluate_love_letter_multiple(letter, num_evaluations=3)
            
            if 'error' in evaluation:
                print(f"ERROR: {evaluation['error']}")
                continue
                
            avg_score = evaluation.get('overall_score', 0)
            variance = evaluation.get('score_variance', 0)
            
            print(f"Average Score: {avg_score:.1f}")
            print(f"Score Variance: {variance:.1f}")
            print(f"Individual Scores: {[round(e.get('overall_score', 0), 1) for e in evaluation.get('individual_evaluations', [])]}")
            
        except Exception as e:
            print(f"ERROR evaluating {name}: {e}")


def analyze_results(results):
    """Analyze the evaluation results"""
    print("\n" + "=" * 60)
    print("RESULTS ANALYSIS")
    print("=" * 60)
    
    print("\nScore Summary:")
    print("Letter Type".ljust(20) + "Expected".ljust(15) + "Actual".ljust(10) + "Status")
    print("-" * 55)
    
    for result in results:
        if 'error' in result:
            status = "ERROR"
        else:
            expected_min, expected_max = map(int, result['expected_range'].split('-'))
            actual = result['actual_score']
            
            if expected_min <= actual <= expected_max:
                status = "✓ PASS"
            elif actual < expected_min:
                status = "⬇ LOW"
            else:
                status = "⬆ HIGH"
        
        name = result['name'][:18]
        expected = result['expected_range']
        actual = f"{result['actual_score']:.1f}" if 'actual_score' in result else "ERROR"
        
        print(f"{name.ljust(20)}{expected.ljust(15)}{actual.ljust(10)}{status}")
    
    # Calculate discriminatory power
    valid_scores = [r['actual_score'] for r in results if 'actual_score' in r and r['actual_score'] > 0]
    if len(valid_scores) >= 2:
        score_range = max(valid_scores) - min(valid_scores)
        print(f"\nDiscriminatory Power:")
        print(f"Score Range: {score_range:.1f} points")
        print(f"Min Score: {min(valid_scores):.1f}")
        print(f"Max Score: {max(valid_scores):.1f}")
        
        if score_range >= 50:
            print("✓ Good discriminatory power (range ≥ 50)")
        elif score_range >= 30:
            print("⚠ Moderate discriminatory power (range 30-50)")
        else:
            print("⚠ Low discriminatory power (range < 30)")


async def main():
    """Run all evaluator tests"""
    start_time = datetime.now()
    logger.info("Love Letter Evaluator Testing Started")
    logger.info(f"Testing {len(TEST_LETTERS)} letters of varying quality...")
    logger.info(f"Start time: {start_time}")
    
    try:
        # Test single evaluations
        logger.info("Starting single evaluation tests...")
        results = await test_single_evaluation()
        
        # Test multiple evaluations (for consistency) - only if single tests work
        if results and not all('error' in r for r in results):
            logger.info("Starting multiple evaluation tests...")
            await test_multiple_evaluation()
        else:
            logger.warning("Skipping multiple evaluation tests due to errors in single tests")
        
        # Analyze results
        logger.info("Analyzing results...")
        analyze_results(results)
        
        # Save detailed results
        output_file = Path(__file__).parent / "evaluator_test_results.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        end_time = datetime.now()
        total_time = end_time - start_time
        logger.info(f"\nDetailed results saved to: {output_file}")
        logger.info(f"Total test time: {total_time}")
        logger.info("Testing completed successfully!")
        
    except Exception as e:
        logger.error(f"Testing failed with error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())