"""
Documentation Cleanup Script

Consolidates 60+ markdown files into organized structure.
"""

import shutil
from pathlib import Path

# Files to KEEP in root
KEEP_IN_ROOT = {
    'README.md',
    'LICENSE',
    'ABSOLUTE_PERFECTION_ACHIEVED.md',
    'ALL_OUTPUTS_VALIDATED.md',
    'SCIENTIFIC_CORRECTNESS_REVIEW.md',
    'FINAL_EVALUATION_PERFECT_METRIC.md',
    'COMPREHENSIVE_REVIEW_AND_IMPROVEMENTS.md',
    'GITHUB_SETUP_INSTRUCTIONS.md',
}

# Files to move to docs/
MOVE_TO_DOCS = {
    'USAGE_EXAMPLE_COMPLETE.py',
    'COMPLETE_SCIENTIFIC_VALIDATION.py',
}

# Session summaries to docs/sessions/
SESSION_FILES = [
    'SESSION_SUMMARY_PROMPTS_1_2.md',
    'SESSION_SUMMARY_PROMPTS_3_4.md',
    'SESSION_SUMMARY_PROMPT_5_FINAL.md',
    'SESSION_COMPLETE_2025-10-31.md',
    'SESSION_FINALE_COMPLETE.md',
    'SESSION_PERFECTION_PROGRESS.md',
    'SESSION_THEORY_ALIGNMENT_COMPLETE.md',
]

# Progress files to docs/progress/
PROGRESS_FILES = [
    'PROGRESS_FAHRPLAN_1.md',
    'PROGRESS_FAHRPLAN_2_TASKS_4_5.md',
    'PROGRESS_REPORT.md',
    'PROGRESS_TAG1_VORMITTAG.md',
    'FAHRPLAN_1_MINIMAL.md',
    'FAHRPLAN_2_COMPLETE.md',
    'FAHRPLAN_2_ERWEITERT.md',
    'FAHRPLAN_3_PERFEKT.md',
    'FAHRPLAENE_UEBERSICHT.md',
]

# Everything else goes to docs/archive/
def main():
    print("="*70)
    print("DOCUMENTATION CLEANUP")
    print("="*70)
    print()
    
    # Create directories
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    (docs_dir / 'sessions').mkdir(exist_ok=True)
    (docs_dir / 'progress').mkdir(exist_ok=True)
    (docs_dir / 'archive').mkdir(exist_ok=True)
    (docs_dir / 'examples').mkdir(exist_ok=True)
    
    # Move session files
    print("[1/4] Moving session summaries...")
    for file in SESSION_FILES:
        src = Path(file)
        if src.exists():
            dst = docs_dir / 'sessions' / file
            shutil.move(str(src), str(dst))
            print(f"  -> {file}")
    
    # Move progress files
    print()
    print("[2/4] Moving progress files...")
    for file in PROGRESS_FILES:
        src = Path(file)
        if src.exists():
            dst = docs_dir / 'progress' / file
            shutil.move(str(src), str(dst))
            print(f"  -> {file}")
    
    # Move examples
    print()
    print("[3/4] Moving examples...")
    for file in MOVE_TO_DOCS:
        src = Path(file)
        if src.exists():
            dst = docs_dir / 'examples' / file
            shutil.move(str(src), str(dst))
            print(f"  -> {file}")
    
    # Archive everything else
    print()
    print("[4/4] Archiving old files...")
    for md_file in Path('.').glob('*.md'):
        if md_file.name not in KEEP_IN_ROOT:
            dst = docs_dir / 'archive' / md_file.name
            shutil.move(str(md_file), str(dst))
            print(f"  -> {md_file.name}")
    
    print()
    print("="*70)
    print("CLEANUP COMPLETE")
    print("="*70)
    print()
    
    # Summary
    print("Directory structure:")
    print("  docs/")
    print("    sessions/   - Session summaries")
    print("    progress/   - Progress tracking")
    print("    examples/   - Usage examples")
    print("    archive/    - Old analysis files")
    print()
    
    # Count files
    root_count = len(list(Path('.').glob('*.md')))
    session_count = len(list((docs_dir / 'sessions').glob('*.md')))
    progress_count = len(list((docs_dir / 'progress').glob('*.md')))
    archive_count = len(list((docs_dir / 'archive').glob('*.md')))
    
    print(f"Files in root:     {root_count}")
    print(f"Files in sessions: {session_count}")
    print(f"Files in progress: {progress_count}")
    print(f"Files in archive:  {archive_count}")
    print()
    print("[SUCCESS] Documentation organized!")

if __name__ == '__main__':
    main()
