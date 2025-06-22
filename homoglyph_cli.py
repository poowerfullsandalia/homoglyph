#!/usr/bin/env python3
"""
Command-line interface for homoglyph text transformation.
"""

import argparse
import sys
from pathlib import Path
from homoglyph_poc import HomoglyphTransformer
from homoglyph_advanced import AdvancedHomoglyphTransformer, TransformStrategy


def main():
    parser = argparse.ArgumentParser(
        description='Transform text using homoglyph substitution to evade AI detectors.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transform text from stdin
  echo "Hello world" | python homoglyph_cli.py
  
  # Transform a file
  python homoglyph_cli.py -i input.txt -o output.txt
  
  # Use advanced strategy
  python homoglyph_cli.py -i input.txt -s systematic -r 0.5
  
  # Analyze text for existing homoglyphs
  python homoglyph_cli.py -i suspicious.txt --analyze
  
  # Reverse transformation
  python homoglyph_cli.py -i transformed.txt --reverse
        """
    )
    
    # Input/Output options
    parser.add_argument('-i', '--input', type=str, 
                       help='Input file path (default: stdin)')
    parser.add_argument('-o', '--output', type=str,
                       help='Output file path (default: stdout)')
    
    # Transformation options
    parser.add_argument('-r', '--rate', type=float, default=0.3,
                       help='Replacement rate (0.0-1.0, default: 0.3)')
    parser.add_argument('-s', '--strategy', type=str, default='random',
                       choices=['random', 'systematic', 'word_boundary', 
                               'high_frequency', 'mixed_script'],
                       help='Transformation strategy (default: random)')
    parser.add_argument('--seed', type=int, 
                       help='Random seed for reproducible transformations')
    
    # Action options
    parser.add_argument('--analyze', action='store_true',
                       help='Analyze text for homoglyphs instead of transforming')
    parser.add_argument('--reverse', action='store_true',
                       help='Reverse homoglyph transformation')
    parser.add_argument('--advanced', action='store_true',
                       help='Use advanced transformer with more homoglyphs')
    
    # Display options
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed transformation information')
    parser.add_argument('--show-diff', action='store_true',
                       help='Show character-by-character differences')
    
    args = parser.parse_args()
    
    # Read input text
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    # Initialize transformer
    if args.advanced:
        transformer = AdvancedHomoglyphTransformer()
    else:
        transformer = HomoglyphTransformer()
    
    # Perform requested action
    if args.analyze:
        # Analyze text for homoglyphs
        analysis = transformer.analyze_text(text)
        
        print("HOMOGLYPH ANALYSIS")
        print("=" * 50)
        print(f"Total characters: {analysis['total_characters']}")
        print(f"Homoglyph characters: {analysis['homoglyph_count']} "
              f"({analysis['homoglyph_percentage']:.1f}%)")
        print(f"Latin characters: {analysis['latin_count']}")
        
        if analysis['homoglyph_positions'] and args.verbose:
            print("\nHomoglyphs found:")
            for pos, char, latin in analysis['homoglyph_positions'][:20]:
                print(f"  Position {pos}: '{char}' (U+{ord(char):04X}) "
                      f"→ Latin '{latin}'")
            if len(analysis['homoglyph_positions']) > 20:
                print(f"  ... and {len(analysis['homoglyph_positions']) - 20} more")
        
        if args.advanced and hasattr(transformer, 'analyze_unicode_blocks'):
            blocks = transformer.analyze_unicode_blocks(text)
            print(f"\nUnicode blocks: {', '.join(blocks.keys())}")
    
    elif args.reverse:
        # Reverse transformation
        reversed_text = transformer.reverse_transform(text)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(reversed_text)
        else:
            print(reversed_text, end='')
        
        if args.verbose:
            print(f"\nReversed {len([c for c in text if c != reversed_text[i] 
                                    for i, c in enumerate(text) if i < len(reversed_text)])} "
                  f"homoglyphs", file=sys.stderr)
    
    else:
        # Transform text
        if args.advanced and args.strategy != 'random':
            strategy = TransformStrategy[args.strategy.upper()]
            transformed, count = transformer.transform_with_strategy(
                text, strategy, args.rate, args.seed
            )
        else:
            transformed, count = transformer.transform(text, args.rate, args.seed)
        
        # Output transformed text
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(transformed)
        else:
            print(transformed, end='')
        
        # Show statistics if verbose
        if args.verbose:
            print(f"\n\nTransformation Statistics:", file=sys.stderr)
            print(f"  Strategy: {args.strategy}", file=sys.stderr)
            print(f"  Replacement rate: {args.rate:.1%}", file=sys.stderr)
            print(f"  Characters replaced: {count}", file=sys.stderr)
            print(f"  Total characters: {len(text)}", file=sys.stderr)
            print(f"  Actual replacement rate: {count/len(text):.1%}", file=sys.stderr)
        
        # Show differences if requested
        if args.show_diff and not args.output:
            print("\n\nCharacter differences:", file=sys.stderr)
            differences = 0
            for i, (orig, trans) in enumerate(zip(text[:100], transformed[:100])):
                if orig != trans:
                    print(f"  Position {i}: '{orig}' → '{trans}' "
                          f"(U+{ord(orig):04X} → U+{ord(trans):04X})", 
                          file=sys.stderr)
                    differences += 1
                    if differences >= 10:
                        print("  ... (showing first 10 differences)", file=sys.stderr)
                        break


if __name__ == "__main__":
    main() 