# SilverSpeak POC: Homoglyph-based Text Transformation

This is a proof-of-concept implementation of the homoglyph-based text transformation technique described in the paper ["SilverSpeak: Evading AI-Generated Text Detectors using Homoglyphs"](https://arxiv.org/abs/2406.11239).

## Overview

The SilverSpeak attack demonstrates how replacing Latin characters with visually identical characters from other Unicode blocks (primarily Cyrillic and Greek) can potentially bypass AI-generated text detectors. These "homoglyphs" look the same to human readers but have different Unicode values, which can confuse text analysis systems.

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd homoglyph

# Install dependencies
pip install -r requirements.txt

# Run basic demonstration
python homoglyph_poc.py

# Start web interface
python homoglyph_web_interface.py
# Then open http://localhost:5000 in your browser
```

## Features

### 1. Basic Homoglyph Transformer (`homoglyph_poc.py`)
- Core transformation functionality
- Character-by-character analysis
- Reverse transformation capabilities
- Visual comparison tools

### 2. Advanced Transformer (`homoglyph_advanced.py`)
- Multiple transformation strategies:
  - **Random**: Randomly replace characters
  - **Systematic**: Replace all occurrences of selected characters
  - **Word Boundary**: Focus on first/last characters of words
  - **High Frequency**: Target most common English letters
  - **Mixed Script**: Use multiple Unicode scripts for maximum confusion
- Extended homoglyph mappings from various Unicode blocks
- Unicode block analysis

### 3. Web Interface (`homoglyph_web_interface.py`)
- Interactive browser-based interface
- Real-time transformation with adjustable replacement rate
- Character-by-character comparison
- Visual and byte-level analysis

### 4. Command Line Interface (`homoglyph_cli.py`)
- Transform files or stdin input
- Multiple transformation strategies
- Analysis and reverse transformation modes
- Verbose output with statistics



## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run the basic demonstration:
```bash
python homoglyph_poc.py
```

Run advanced strategies demonstration:
```bash
python homoglyph_advanced.py
```



### CLI Tool Examples

Transform text from stdin:
```bash
echo "Hello world" | python homoglyph_cli.py

# With verbose output
echo "Hello world" | python homoglyph_cli.py -v

# With specific strategy
echo "Hello world" | python homoglyph_cli.py -s systematic -r 0.5
```

Transform a file:
```bash
python homoglyph_cli.py -i input.txt -o output.txt

# Analyze for existing homoglyphs
python homoglyph_cli.py -i suspicious.txt --analyze

# Reverse transformation
python homoglyph_cli.py -i transformed.txt --reverse
```

### Web Interface

Start the web server:
```bash
python homoglyph_web_interface.py
```

Then open your browser to `http://localhost:5000`

## How It Works

### Homoglyph Mapping
The transformer maintains mappings between Latin characters and their lookalikes:
- Latin 'A' (U+0041) → Cyrillic 'А' (U+0410)
- Latin 'e' (U+0065) → Cyrillic 'е' (U+0435)
- Latin 'o' (U+006F) → Greek 'ο' (U+03BF)

### Transformation Process
1. **Input**: Regular text (human or AI-generated)
2. **Processing**: Replace characters based on selected strategy and rate
3. **Output**: Visually identical text with different Unicode values

### Example Transformation
```
Original:    The quick brown fox
Transformed: Тhе quiсk brοwn fοx
             ^   ^   ^    ^    ^
             (Cyrillic/Greek replacements)
```

## Security & Ethical Considerations

This POC is for **educational and research purposes only**. The technique demonstrates a vulnerability in text detection systems that should be addressed through:

1. **Unicode normalization** before text analysis
2. **Homoglyph detection** algorithms
3. **Multi-layer detection** approaches

## Technical Details

### Supported Character Sets
- Latin alphabet (A-Z, a-z)
- Numbers (0-9)
- Lookalikes from:
  - Cyrillic script
  - Greek alphabet
  - Mathematical symbols
  - Fullwidth forms
  - Various Unicode blocks

### Detection Evasion Effectiveness
According to the paper, homoglyph attacks can reduce detector accuracy significantly:
- Average MCC (Matthews Correlation Coefficient) drops from 0.64 to -0.01
- Makes detectors classify all text as either AI-generated or human-written

## Files in this POC

- `homoglyph_poc.py` - Basic implementation with core functionality
- `homoglyph_advanced.py` - Advanced strategies and extended mappings
- `homoglyph_web_interface.py` - Flask-based web interface
- `homoglyph_cli.py` - Command-line tool for file processing
- `requirements.txt` - Python dependencies
- `README.md` - This documentation

## Limitations

1. **Font Support**: Some fonts may not render all Unicode characters identically
2. **Context**: Sophisticated detectors might use context beyond character analysis
3. **Detectability**: The technique itself can be detected through Unicode analysis

## References

- Paper: ["SilverSpeak: Evading AI-Generated Text Detectors using Homoglyphs"](https://arxiv.org/abs/2406.11239)
- Authors: Aldan Creo, Shushanta Pudasaini
- Conference: Workshop on Detecting AI Generated Content at COLING 2025

## License

This POC is provided as-is for educational purposes. Please refer to the original paper for academic citations. 