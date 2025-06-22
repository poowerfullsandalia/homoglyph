#!/usr/bin/env python3
"""
SilverSpeak POC: Homoglyph-based text transformation to evade AI text detectors

This implementation demonstrates how replacing Latin characters with visually identical
characters from other alphabets (primarily Cyrillic) can potentially bypass AI-generated
text detection systems.

Based on: "SilverSpeak: Evading AI-Generated Text Detectors using Homoglyphs"
arXiv:2406.11239
"""

import random
import unicodedata
from typing import Dict, Set, Tuple, Optional


class HomoglyphTransformer:
    """Transforms text using homoglyph substitution."""
    
    def __init__(self):
        # Mapping of Latin characters to their Cyrillic/Greek homoglyphs
        # These characters look identical or nearly identical visually
        self.homoglyph_map: Dict[str, list[str]] = {
            # Uppercase Latin to Cyrillic
            'A': ['А'],  # U+0041 -> U+0410 (Cyrillic)
            'B': ['В'],  # U+0042 -> U+0412 (Cyrillic)
            'C': ['С'],  # U+0043 -> U+0421 (Cyrillic)
            'E': ['Е'],  # U+0045 -> U+0415 (Cyrillic)
            'H': ['Н'],  # U+0048 -> U+041D (Cyrillic)
            'K': ['К'],  # U+004B -> U+041A (Cyrillic)
            'M': ['М'],  # U+004D -> U+041C (Cyrillic)
            'O': ['О', 'Ο'],  # U+004F -> U+041E (Cyrillic), U+039F (Greek)
            'P': ['Р'],  # U+0050 -> U+0420 (Cyrillic)
            'T': ['Т'],  # U+0054 -> U+0422 (Cyrillic)
            'X': ['Х'],  # U+0058 -> U+0425 (Cyrillic)
            'Y': ['У'],  # U+0059 -> U+0423 (Cyrillic)
            
            # Lowercase Latin to Cyrillic
            'a': ['а'],  # U+0061 -> U+0430 (Cyrillic)
            'c': ['с'],  # U+0063 -> U+0441 (Cyrillic)
            'e': ['е'],  # U+0065 -> U+0435 (Cyrillic)
            'o': ['о', 'ο'],  # U+006F -> U+043E (Cyrillic), U+03BF (Greek)
            'p': ['р'],  # U+0070 -> U+0440 (Cyrillic)
            'x': ['х'],  # U+0078 -> U+0445 (Cyrillic)
            'y': ['у'],  # U+0079 -> U+0443 (Cyrillic)
            
            # Additional homoglyphs from various scripts
            'i': ['і'],  # U+0069 -> U+0456 (Cyrillic)
            'j': ['ј'],  # U+006A -> U+0458 (Cyrillic)
            's': ['ѕ'],  # U+0073 -> U+0455 (Cyrillic)
            
            # Numbers
            '0': ['О', 'о'],  # Can use letter O
            '1': ['l', 'I'],  # Can use lowercase L or uppercase i
            '3': ['З'],  # U+0033 -> U+0417 (Cyrillic)
        }
        
        # Reverse mapping for decoding
        self.reverse_map: Dict[str, str] = {}
        for latin_char, homoglyphs in self.homoglyph_map.items():
            for homoglyph in homoglyphs:
                self.reverse_map[homoglyph] = latin_char
    
    def transform(self, text: str, replacement_rate: float = 0.3, 
                  random_seed: Optional[int] = None) -> Tuple[str, int]:
        """
        Transform text by replacing characters with homoglyphs.
        
        Args:
            text: Input text to transform
            replacement_rate: Fraction of eligible characters to replace (0.0-1.0)
            random_seed: Random seed for reproducible transformations
            
        Returns:
            Tuple of (transformed_text, number_of_replacements)
        """
        if random_seed is not None:
            random.seed(random_seed)
        
        transformed_chars = []
        replacement_count = 0
        
        for char in text:
            # Check if character has homoglyph alternatives
            if char in self.homoglyph_map and random.random() < replacement_rate:
                # Choose random homoglyph
                homoglyph = random.choice(self.homoglyph_map[char])
                transformed_chars.append(homoglyph)
                replacement_count += 1
            else:
                transformed_chars.append(char)
        
        return ''.join(transformed_chars), replacement_count
    
    def reverse_transform(self, text: str) -> str:
        """Convert homoglyphs back to their Latin equivalents."""
        result = []
        for char in text:
            if char in self.reverse_map:
                result.append(self.reverse_map[char])
            else:
                result.append(char)
        return ''.join(result)
    
    def analyze_text(self, text: str) -> Dict[str, any]:
        """Analyze text for homoglyph content."""
        total_chars = len(text)
        homoglyph_chars = 0
        latin_chars = 0
        homoglyph_positions = []
        
        for i, char in enumerate(text):
            if char in self.reverse_map:
                homoglyph_chars += 1
                homoglyph_positions.append((i, char, self.reverse_map[char]))
            elif ord('A') <= ord(char) <= ord('Z') or ord('a') <= ord(char) <= ord('z'):
                latin_chars += 1
        
        return {
            'total_characters': total_chars,
            'homoglyph_count': homoglyph_chars,
            'latin_count': latin_chars,
            'homoglyph_percentage': (homoglyph_chars / total_chars * 100) if total_chars > 0 else 0,
            'homoglyph_positions': homoglyph_positions
        }
    
    def visualize_comparison(self, original: str, transformed: str) -> None:
        """Print visual comparison of original and transformed text."""
        print("\n" + "="*60)
        print("VISUAL COMPARISON")
        print("="*60)
        print(f"Original:     {original}")
        print(f"Transformed:  {transformed}")
        print(f"Look same?    {original == transformed}")
        print(f"Are same?     {original.encode('utf-8') == transformed.encode('utf-8')}")
        print("\nCharacter-by-character comparison:")
        print("-"*60)
        
        max_len = max(len(original), len(transformed))
        for i in range(max_len):
            if i < len(original) and i < len(transformed):
                orig_char = original[i]
                trans_char = transformed[i]
                orig_unicode = f"U+{ord(orig_char):04X}"
                trans_unicode = f"U+{ord(trans_char):04X}"
                
                if orig_char != trans_char:
                    print(f"Position {i:3d}: '{orig_char}' ({orig_unicode}) -> "
                          f"'{trans_char}' ({trans_unicode}) [REPLACED]")


def demonstrate_homoglyph_attack():
    """Demonstrate the homoglyph attack with example text."""
    
    transformer = HomoglyphTransformer()
    
    # Example texts
    ai_generated_text = """The rapid advancement of artificial intelligence has revolutionized 
numerous industries. Machine learning algorithms now power recommendation systems, 
autonomous vehicles, and medical diagnostics. As we continue to develop these 
technologies, it's crucial to consider their ethical implications and ensure 
they benefit humanity as a whole."""
    
    human_text = """I woke up this morning feeling pretty tired. Had my usual coffee 
and checked my emails. The weather was nice, so I decided to take a walk in the 
park. Saw some dogs playing fetch, which made me smile. Sometimes it's the 
simple things that make a day better."""
    
    print("HOMOGLYPH-BASED TEXT TRANSFORMATION DEMONSTRATION")
    print("================================================\n")
    
    # Test different replacement rates
    replacement_rates = [0.1, 0.3, 0.5, 0.7, 1.0]
    
    for rate in replacement_rates:
        print(f"\n\nReplacement Rate: {rate*100:.0f}%")
        print("-" * 50)
        
        # Transform AI-generated text
        transformed_ai, count_ai = transformer.transform(ai_generated_text, rate, random_seed=42)
        analysis_ai = transformer.analyze_text(transformed_ai)
        
        print(f"AI-Generated Text:")
        print(f"  Replacements: {count_ai}")
        print(f"  Homoglyph %: {analysis_ai['homoglyph_percentage']:.1f}%")
        print(f"  Sample: {transformed_ai[:100]}...")
        
        # Transform human text
        transformed_human, count_human = transformer.transform(human_text, rate, random_seed=42)
        analysis_human = transformer.analyze_text(transformed_human)
        
        print(f"\nHuman Text:")
        print(f"  Replacements: {count_human}")
        print(f"  Homoglyph %: {analysis_human['homoglyph_percentage']:.1f}%")
        print(f"  Sample: {transformed_human[:100]}...")
    
    # Detailed comparison for one example
    print("\n\nDETAILED TRANSFORMATION EXAMPLE")
    sample_text = "The quick brown fox jumps over the lazy dog."
    transformed_sample, _ = transformer.transform(sample_text, 0.5, random_seed=42)
    transformer.visualize_comparison(sample_text, transformed_sample)
    
    # Show reverse transformation
    print("\n\nREVERSE TRANSFORMATION")
    print("-" * 50)
    reversed_text = transformer.reverse_transform(transformed_sample)
    print(f"Transformed:  {transformed_sample}")
    print(f"Reversed:     {reversed_text}")
    print(f"Matches original? {reversed_text == sample_text}")


if __name__ == "__main__":
    demonstrate_homoglyph_attack() 