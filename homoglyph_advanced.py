#!/usr/bin/env python3
"""
Advanced homoglyph transformer with comprehensive Unicode mappings.
Implements various strategies for evading AI text detectors.
"""

import random
import unicodedata
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum


class TransformStrategy(Enum):
    """Different strategies for homoglyph transformation."""
    RANDOM = "random"  # Random replacement
    SYSTEMATIC = "systematic"  # Replace all occurrences of specific characters
    WORD_BOUNDARY = "word_boundary"  # Focus on word boundaries
    HIGH_FREQUENCY = "high_frequency"  # Target high-frequency characters
    MIXED_SCRIPT = "mixed_script"  # Mix multiple scripts (Cyrillic, Greek, etc.)


class AdvancedHomoglyphTransformer:
    """Advanced transformer with comprehensive homoglyph mappings."""
    
    def __init__(self):
        # Extended homoglyph mappings from various Unicode blocks
        self.homoglyph_map = {
            # Latin uppercase to lookalikes
            'A': ['А', 'Α', 'Ａ', 'Ꭺ', '𝐀', '𝐴', '𝑨', '𝖠', '𝗔', '𝘈', '𝘼', '𝙰'],
            'B': ['В', 'Β', 'Ᏼ', 'ᗷ', 'Ｂ', '𝐁', '𝐵', '𝑩', '𝖡', '𝗕', '𝘉', '𝘽', '𝙱'],
            'C': ['С', 'Ϲ', 'Ⅽ', 'Ｃ', 'Ꮯ', 'ᑕ', '𝐂', '𝐶', '𝑪', '𝖢', '𝗖', '𝘊', '𝘾', '𝙲'],
            'D': ['Ⅾ', 'Ｄ', 'ᗞ', 'ᴰ', '𝐃', '𝐷', '𝑫', '𝖣', '𝗗', '𝘋', '𝘿', '𝙳'],
            'E': ['Е', 'Ε', 'Ｅ', 'ᴱ', '𝐄', '𝐸', '𝑬', '𝖤', '𝗘', '𝘌', '𝙀', '𝙴'],
            'F': ['Ϝ', 'Ｆ', 'ᖴ', '𝐅', '𝐹', '𝑭', '𝖥', '𝗙', '𝘍', '𝙁', '𝙵'],
            'G': ['Ԍ', 'Ꮐ', 'Ｇ', 'ᴳ', '𝐆', '𝐺', '𝑮', '𝖦', '𝗚', '𝘎', '𝙂', '𝙶'],
            'H': ['Н', 'Η', 'Ｈ', 'ᕼ', 'ᴴ', '𝐇', '𝐻', '𝑯', '𝖧', '𝗛', '𝘏', '𝙃', '𝙷'],
            'I': ['І', 'Ι', 'Ⅰ', 'Ｉ', 'ᴵ', '𝐈', '𝐼', '𝑰', '𝖨', '𝗜', '𝘐', '𝙄', '𝙸'],
            'J': ['Ј', 'Ꭻ', 'Ｊ', 'ᴶ', '𝐉', '𝐽', '𝑱', '𝖩', '𝗝', '𝘑', '𝙅', '𝙹'],
            'K': ['К', 'Κ', 'K', 'Ｋ', 'ᴷ', '𝐊', '𝐾', '𝑲', '𝖪', '𝗞', '𝘒', '𝙆', '𝙺'],
            'L': ['Ⅼ', 'Ｌ', 'ᴸ', 'ʟ', '𝐋', '𝐿', '𝑳', '𝖫', '𝗟', '𝘓', '𝙇', '𝙻'],
            'M': ['М', 'Μ', 'Ⅿ', 'Ｍ', 'ᴹ', '𝐌', '𝑀', '𝑴', '𝖬', '𝗠', '𝘔', '𝙈', '𝙼'],
            'N': ['Ν', 'Ｎ', 'ᴺ', '𝐍', '𝑁', '𝑵', '𝖭', '𝗡', '𝘕', '𝙉', '𝙽'],
            'O': ['О', 'Ο', 'O', 'Ｏ', 'ᴼ', '𝐎', '𝑂', '𝑶', '𝖮', '𝗢', '𝘖', '𝙊', '𝙾'],
            'P': ['Р', 'Ρ', 'Ｐ', 'ᴾ', '𝐏', '𝑃', '𝑷', '𝖯', '𝗣', '𝘗', '𝙋', '𝙿'],
            'Q': ['Ｑ', 'ℚ', '𝐐', '𝑄', '𝑸', '𝖰', '𝗤', '𝘘', '𝙌', '𝚀'],
            'R': ['Ʀ', 'Ｒ', 'ᖇ', 'ᴿ', '𝐑', '𝑅', '𝑹', '𝖱', '𝗥', '𝘙', '𝙍', '𝚁'],
            'S': ['Ѕ', 'Ꮪ', 'Ｓ', 'ˢ', '𝐒', '𝑆', '𝑺', '𝖲', '𝗦', '𝘚', '𝙎', '𝚂'],
            'T': ['Т', 'Τ', 'Ｔ', 'ᵀ', '𝐓', '𝑇', '𝑻', '𝖳', '𝗧', '𝘛', '𝙏', '𝚃'],
            'U': ['Ｕ', 'ᵁ', '𝐔', '𝑈', '𝑼', '𝖴', '𝗨', '𝘜', '𝙐', '𝚄'],
            'V': ['Ⅴ', 'Ｖ', 'ⱽ', '𝐕', '𝑉', '𝑽', '𝖵', '𝗩', '𝘝', '𝙑', '𝚅'],
            'W': ['Ｗ', 'ᵂ', '𝐖', '𝑊', '𝑾', '𝖶', '𝗪', '𝘞', '𝙒', '𝚆'],
            'X': ['Х', 'Χ', 'Ⅹ', 'Ｘ', 'ˣ', '𝐗', '𝑋', '𝑿', '𝖷', '𝗫', '𝘟', '𝙓', '𝚇'],
            'Y': ['У', 'Υ', 'Ｙ', 'ʸ', '𝐘', '𝑌', '𝒀', '𝖸', '𝗬', '𝘠', '𝙔', '𝚈'],
            'Z': ['Ζ', 'Ｚ', 'ᶻ', '𝐙', '𝑍', '𝒁', '𝖹', '𝗭', '𝘡', '𝙕', '𝚉'],
            
            # Latin lowercase to lookalikes
            'a': ['а', 'α', 'ａ', 'ɑ', '𝐚', '𝑎', '𝒂', '𝖺', '𝗮', '𝘢', '𝙖', '𝚊'],
            'b': ['Ь', 'ｂ', 'ᵇ', '𝐛', '𝑏', '𝒃', '𝖻', '𝗯', '𝘣', '𝙗', '𝚋'],
            'c': ['с', 'ϲ', 'ｃ', 'ᶜ', '𝐜', '𝑐', '𝒄', '𝖼', '𝗰', '𝘤', '𝙘', '𝚌'],
            'd': ['ԁ', 'ｄ', 'ᵈ', '𝐝', '𝑑', '𝒅', '𝖽', '𝗱', '𝘥', '𝙙', '𝚍'],
            'e': ['е', 'ε', 'ｅ', 'ᵉ', '𝐞', '𝑒', '𝒆', '𝖾', '𝗲', '𝘦', '𝙚', '𝚎'],
            'f': ['ｆ', 'ᶠ', '𝐟', '𝑓', '𝒇', '𝖿', '𝗳', '𝘧', '𝙛', '𝚏'],
            'g': ['ɡ', 'ｇ', 'ᵍ', '𝐠', '𝑔', '𝒈', '𝗀', '𝗴', '𝘨', '𝙜', '𝚐'],
            'h': ['һ', 'ｈ', 'ʰ', '𝐡', '𝒉', '𝗁', '𝗵', '𝘩', '𝙝', '𝚑'],
            'i': ['і', 'ι', 'ⅰ', 'ｉ', 'ⁱ', '𝐢', '𝑖', '𝒊', '𝗂', '𝗶', '𝘪', '𝙞', '𝚒'],
            'j': ['ј', 'ϳ', 'ｊ', 'ʲ', '𝐣', '𝑗', '𝒋', '𝗃', '𝗷', '𝘫', '𝙟', '𝚓'],
            'k': ['ｋ', 'ᵏ', '𝐤', '𝑘', '𝒌', '𝗄', '𝗸', '𝘬', '𝙠', '𝚔'],
            'l': ['ⅼ', 'ｌ', 'ˡ', '𝐥', '𝑙', '𝒍', '𝗅', '𝗹', '𝘭', '𝙡', '𝚕'],
            'm': ['ⅿ', 'ｍ', 'ᵐ', '𝐦', '𝑚', '𝒎', '𝗆', '𝗺', '𝘮', '𝙢', '𝚖'],
            'n': ['ｎ', 'ⁿ', '𝐧', '𝑛', '𝒏', '𝗇', '𝗻', '𝘯', '𝙣', '𝚗'],
            'o': ['о', 'ο', 'ｏ', 'ᵒ', '𝐨', '𝑜', '𝒐', '𝗈', '𝗼', '𝘰', '𝙤', '𝚘'],
            'p': ['р', 'ρ', 'ｐ', 'ᵖ', '𝐩', '𝑝', '𝒑', '𝗉', '𝗽', '𝘱', '𝙥', '𝚙'],
            'q': ['ｑ', '𝐪', '𝑞', '𝒒', '𝗊', '𝗾', '𝘲', '𝙦', '𝚚'],
            'r': ['г', 'ｒ', 'ʳ', '𝐫', '𝑟', '𝒓', '𝗋', '𝗿', '𝘳', '𝙧', '𝚛'],
            's': ['ѕ', 'ｓ', 'ˢ', '𝐬', '𝑠', '𝒔', '𝗌', '𝘀', '𝘴', '𝙨', '𝚜'],
            't': ['ｔ', 'ᵗ', '𝐭', '𝑡', '𝒕', '𝗍', '𝘁', '𝘵', '𝙩', '𝚝'],
            'u': ['ｕ', 'ᵘ', '𝐮', '𝑢', '𝒖', '𝗎', '𝘂', '𝘶', '𝙪', '𝚞'],
            'v': ['ν', 'ⅴ', 'ｖ', 'ᵛ', '𝐯', '𝑣', '𝒗', '𝗏', '𝘃', '𝘷', '𝙫', '𝚟'],
            'w': ['ｗ', 'ʷ', '𝐰', '𝑤', '𝒘', '𝗐', '𝘄', '𝘸', '𝙬', '𝚠'],
            'x': ['х', 'χ', 'ⅹ', 'ｘ', 'ˣ', '𝐱', '𝑥', '𝒙', '𝗑', '𝘅', '𝘹', '𝙭', '𝚡'],
            'y': ['у', 'ｙ', 'ʸ', '𝐲', '𝑦', '𝒚', '𝗒', '𝘆', '𝘺', '𝙮', '𝚢'],
            'z': ['ｚ', 'ᶻ', '𝐳', '𝑧', '𝒛', '𝗓', '𝘇', '𝘻', '𝙯', '𝚣'],
            
            # Numbers
            '0': ['О', 'о', 'Ο', 'ο', '০', '੦', '૦', '௦', '౦', '೦', '൦', '๐', '໐', '༠', '၀', '႐', '០', '᠐', '０'],
            '1': ['l', 'I', '|', '۱', '१', '১', '੧', '૧', '௧', '౧', '೧', '൧', '๑', '໑', '༡', '၁', '႑', '១', '᠑', '１'],
            '2': ['২', '੨', '૨', '௨', '౨', '೨', '൨', '๒', '໒', '༢', '၂', '႒', '២', '᠒', '２'],
            '3': ['З', 'з', 'Ʒ', 'ʒ', '੩', '૩', '௩', '౩', '೩', '൩', '๓', '໓', '༣', '၃', '႓', '៣', '᠓', '３'],
            '4': ['Ч', '੪', '૪', '௪', '౪', '೪', '൪', '๔', '໔', '༤', '၄', '႔', '៤', '᠔', '４'],
            '5': ['੫', '૫', '௫', '౫', '೫', '൫', '๕', '໕', '༥', '၅', '႕', '៥', '᠕', '５'],
            '6': ['੬', '૬', '௬', '౬', '೬', '൬', '๖', '໖', '༦', '၆', '႖', '៦', '᠖', '６'],
            '7': ['੭', '૭', '௭', '౭', '೭', '൭', '๗', '໗', '༧', '၇', '႗', '៧', '᠗', '７'],
            '8': ['੮', '૮', '௮', '౮', '೮', '൮', '๘', '໘', '༨', '၈', '႘', '៨', '᠘', '８'],
            '9': ['੯', '૯', '௯', '౯', '೯', '൯', '๙', '໙', '༩', '၉', '႙', '៩', '᠙', '９'],
        }
        
        # Create reverse mapping
        self.reverse_map = {}
        for latin_char, homoglyphs in self.homoglyph_map.items():
            for homoglyph in homoglyphs:
                self.reverse_map[homoglyph] = latin_char
        
        # High frequency characters in English
        self.high_frequency_chars = set('etaoinshrdlcumwfgypbvkjxqz')
        
    def transform_with_strategy(self, text: str, strategy: TransformStrategy, 
                               replacement_rate: float = 0.3,
                               random_seed: Optional[int] = None) -> Tuple[str, int]:
        """Transform text using specific strategy."""
        if random_seed is not None:
            random.seed(random_seed)
        
        if strategy == TransformStrategy.RANDOM:
            return self._transform_random(text, replacement_rate)
        elif strategy == TransformStrategy.SYSTEMATIC:
            return self._transform_systematic(text, replacement_rate)
        elif strategy == TransformStrategy.WORD_BOUNDARY:
            return self._transform_word_boundary(text, replacement_rate)
        elif strategy == TransformStrategy.HIGH_FREQUENCY:
            return self._transform_high_frequency(text, replacement_rate)
        elif strategy == TransformStrategy.MIXED_SCRIPT:
            return self._transform_mixed_script(text, replacement_rate)
        else:
            return self._transform_random(text, replacement_rate)
    
    def _transform_random(self, text: str, replacement_rate: float) -> Tuple[str, int]:
        """Random replacement strategy."""
        transformed_chars = []
        replacement_count = 0
        
        for char in text:
            if char in self.homoglyph_map and random.random() < replacement_rate:
                homoglyph = random.choice(self.homoglyph_map[char])
                transformed_chars.append(homoglyph)
                replacement_count += 1
            else:
                transformed_chars.append(char)
        
        return ''.join(transformed_chars), replacement_count
    
    def _transform_systematic(self, text: str, replacement_rate: float) -> Tuple[str, int]:
        """Replace all occurrences of randomly selected characters."""
        # Select characters to replace
        available_chars = [c for c in set(text) if c in self.homoglyph_map]
        num_to_replace = int(len(available_chars) * replacement_rate)
        chars_to_replace = random.sample(available_chars, min(num_to_replace, len(available_chars)))
        
        # Create replacement mapping
        replacement_mapping = {}
        for char in chars_to_replace:
            replacement_mapping[char] = random.choice(self.homoglyph_map[char])
        
        # Apply replacements
        transformed_chars = []
        replacement_count = 0
        
        for char in text:
            if char in replacement_mapping:
                transformed_chars.append(replacement_mapping[char])
                replacement_count += 1
            else:
                transformed_chars.append(char)
        
        return ''.join(transformed_chars), replacement_count
    
    def _transform_word_boundary(self, text: str, replacement_rate: float) -> Tuple[str, int]:
        """Focus replacements on first/last characters of words."""
        words = text.split()
        replacement_count = 0
        transformed_words = []
        
        for word in words:
            if not word:
                transformed_words.append(word)
                continue
            
            chars = list(word)
            
            # First character
            if len(chars) > 0 and chars[0] in self.homoglyph_map and random.random() < replacement_rate:
                chars[0] = random.choice(self.homoglyph_map[chars[0]])
                replacement_count += 1
            
            # Last character
            if len(chars) > 1 and chars[-1] in self.homoglyph_map and random.random() < replacement_rate:
                chars[-1] = random.choice(self.homoglyph_map[chars[-1]])
                replacement_count += 1
            
            transformed_words.append(''.join(chars))
        
        return ' '.join(transformed_words), replacement_count
    
    def _transform_high_frequency(self, text: str, replacement_rate: float) -> Tuple[str, int]:
        """Target high-frequency characters."""
        transformed_chars = []
        replacement_count = 0
        
        for char in text:
            lower_char = char.lower()
            if (lower_char in self.high_frequency_chars and 
                char in self.homoglyph_map and 
                random.random() < replacement_rate):
                homoglyph = random.choice(self.homoglyph_map[char])
                transformed_chars.append(homoglyph)
                replacement_count += 1
            else:
                transformed_chars.append(char)
        
        return ''.join(transformed_chars), replacement_count
    
    def _transform_mixed_script(self, text: str, replacement_rate: float) -> Tuple[str, int]:
        """Use homoglyphs from different scripts to maximize confusion."""
        transformed_chars = []
        replacement_count = 0
        
        # Track which scripts we've used
        scripts_used = set()
        
        for char in text:
            if char in self.homoglyph_map and random.random() < replacement_rate:
                # Try to use a homoglyph from a different script than previously used
                homoglyphs = self.homoglyph_map[char]
                
                # Sort homoglyphs by their Unicode block to prefer different scripts
                homoglyphs_sorted = sorted(homoglyphs, 
                                         key=lambda x: (unicodedata.category(x), ord(x)))
                
                # Select one that maximizes script diversity
                selected = random.choice(homoglyphs_sorted)
                transformed_chars.append(selected)
                replacement_count += 1
                
                # Track the script
                try:
                    script = unicodedata.name(selected).split()[0]
                    scripts_used.add(script)
                except:
                    pass
            else:
                transformed_chars.append(char)
        
        return ''.join(transformed_chars), replacement_count
    
    def analyze_unicode_blocks(self, text: str) -> Dict[str, int]:
        """Analyze which Unicode blocks are present in the text."""
        blocks = {}
        for char in text:
            try:
                name = unicodedata.name(char)
                block = name.split()[0] if name else "UNKNOWN"
                blocks[block] = blocks.get(block, 0) + 1
            except:
                blocks["UNKNOWN"] = blocks.get("UNKNOWN", 0) + 1
        return blocks


def demonstrate_advanced_strategies():
    """Demonstrate different transformation strategies."""
    transformer = AdvancedHomoglyphTransformer()
    
    # Test text
    test_text = """The quick brown fox jumps over the lazy dog. This pangram contains 
all letters of the English alphabet. AI-generated text often exhibits certain 
patterns that detection algorithms can identify. By using homoglyphs, we can 
potentially bypass these detection mechanisms."""
    
    print("ADVANCED HOMOGLYPH TRANSFORMATION STRATEGIES")
    print("=" * 60)
    print(f"\nOriginal text:\n{test_text}\n")
    print("=" * 60)
    
    # Test each strategy
    for strategy in TransformStrategy:
        print(f"\n\nStrategy: {strategy.value.upper()}")
        print("-" * 40)
        
        transformed, count = transformer.transform_with_strategy(
            test_text, strategy, replacement_rate=0.3, random_seed=42
        )
        
        print(f"Replacements: {count}")
        print(f"Sample: {transformed[:150]}...")
        
        # Analyze Unicode blocks
        blocks = transformer.analyze_unicode_blocks(transformed)
        print(f"Unicode blocks used: {', '.join(blocks.keys())}")


if __name__ == "__main__":
    demonstrate_advanced_strategies() 