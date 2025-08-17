#!/usr/bin/env python3
"""
Run 50-iteration evolution of love letter generator
Monitor progress and log results
"""

import subprocess
import sys
import time
import logging
import json
from datetime import datetime
from pathlib import Path

# Setup logging
log_filename = f"evolution_50_iter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def check_initial_setup():
    """Verify all files exist and evaluator works"""
    logger.info("Checking initial setup...")
    
    # Check required files
    required_files = [
        'initial_program.py',
        'evaluator.py', 
        'config.yaml'
    ]
    
    # Check in project root for openevolve-run.py
    project_root = Path(__file__).parent.parent.parent
    if not (project_root / 'openevolve-run.py').exists():
        logger.error("Required file missing: openevolve-run.py in project root")
        return False
    
    for file in required_files:
        if not Path(file).exists():
            logger.error(f"Required file missing: {file}")
            return False
    
    logger.info("✓ All required files present")
    
    # Quick evaluator test
    try:
        from evaluator import evaluate
        result = evaluate('initial_program.py')
        logger.info(f"✓ Evaluator working - Initial score: {result.get('beauty_score', 'N/A')}")
        return True
    except Exception as e:
        logger.error(f"Evaluator test failed: {e}")
        return False


def run_evolution():
    """Run the 50-iteration evolution"""
    logger.info("Starting 50-iteration love letter evolution...")
    logger.info(f"Configuration: config.yaml")
    logger.info(f"Initial program: initial_program.py")
    logger.info(f"Evaluator: evaluator.py")
    
    # Prepare command
    project_root = Path(__file__).parent.parent.parent
    cmd = [
        sys.executable, str(project_root / 'openevolve-run.py'),
        'initial_program.py',
        'evaluator.py',
        '--config', 'config.yaml',
        '--iterations', '50'
    ]
    
    logger.info(f"Command: {' '.join(cmd)}")
    
    start_time = time.time()
    
    try:
        # Change to example directory for relative paths
        example_dir = Path(__file__).parent
        
        # Run evolution with real-time output
        process = subprocess.Popen(
            cmd,
            cwd=example_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor output
        iteration_count = 0
        last_score = None
        
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if line:
                logger.info(f"OpenEvolve: {line}")
                
                # Track progress
                if 'Iteration' in line and 'completed' in line:
                    iteration_count += 1
                if 'Best score' in line or 'Score:' in line:
                    try:
                        # Extract score if possible
                        score_parts = line.split()
                        for i, part in enumerate(score_parts):
                            if 'score' in part.lower() and i + 1 < len(score_parts):
                                last_score = score_parts[i + 1]
                                break
                    except:
                        pass
        
        process.wait()
        
        elapsed_time = time.time() - start_time
        
        if process.returncode == 0:
            logger.info(f"✓ Evolution completed successfully!")
            logger.info(f"Total time: {elapsed_time/60:.1f} minutes")
            logger.info(f"Iterations completed: {iteration_count}")
            if last_score:
                logger.info(f"Final score: {last_score}")
            return True
        else:
            logger.error(f"Evolution failed with return code: {process.returncode}")
            return False
            
    except Exception as e:
        logger.error(f"Error running evolution: {e}")
        return False


def analyze_results():
    """Analyze evolution results"""
    logger.info("Analyzing evolution results...")
    
    # Check for output directory
    output_dir = Path('openevolve_output')
    if not output_dir.exists():
        logger.warning("No openevolve_output directory found")
        return
        
    # Look for best program
    best_dir = output_dir / 'best'
    if best_dir.exists():
        best_program = best_dir / 'best_program.py'
        best_info = best_dir / 'best_program_info.json'
        
        if best_program.exists():
            logger.info("✓ Best program found")
            
            # Test the best program
            try:
                from love_letter_evaluator import evaluate
                result = evaluate(str(best_program))
                logger.info(f"Final evaluation - Score: {result.get('beauty_score', 'N/A')}")
                
                # Show the generated letter
                from love_letter_evaluator import execute_love_letter_program
                final_letter = execute_love_letter_program(str(best_program))
                logger.info("Final evolved love letter:")
                logger.info("-" * 50)
                logger.info(final_letter)
                logger.info("-" * 50)
                
            except Exception as e:
                logger.error(f"Error evaluating final program: {e}")
        
        if best_info.exists():
            try:
                with open(best_info) as f:
                    info = json.load(f)
                    logger.info(f"Best program info: {info}")
            except Exception as e:
                logger.error(f"Error reading best program info: {e}")
    
    # Check for checkpoints
    checkpoints_dir = output_dir / 'checkpoints'
    if checkpoints_dir.exists():
        checkpoints = list(checkpoints_dir.glob('checkpoint_*'))
        logger.info(f"Found {len(checkpoints)} checkpoints")
        for cp in sorted(checkpoints)[-3:]:  # Show last 3
            logger.info(f"  {cp.name}")


def main():
    """Main execution function"""
    logger.info("=" * 60)
    logger.info("LOVE LETTER EVOLUTION - 50 ITERATIONS")
    logger.info("=" * 60)
    logger.info(f"Start time: {datetime.now()}")
    logger.info(f"Log file: {log_filename}")
    
    # Setup check
    if not check_initial_setup():
        logger.error("Setup check failed - aborting")
        return 1
    
    # Run evolution
    if not run_evolution():
        logger.error("Evolution failed - aborting")
        return 1
        
    # Analyze results
    analyze_results()
    
    logger.info("=" * 60)
    logger.info("EVOLUTION COMPLETED")
    logger.info("=" * 60)
    logger.info(f"End time: {datetime.now()}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())