#!/usr/bin/env python3
"""
Web interface for SilverSpeak POC homoglyph transformer.
Provides an interactive way to test homoglyph transformations.
"""

from flask import Flask, render_template, request, jsonify
from homoglyph_poc import HomoglyphTransformer
import json
import unicodedata  # Needed for script name checks

app = Flask(__name__)
transformer = HomoglyphTransformer()

@app.route('/')
def index():
    """Serve the main interface."""
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform_text():
    """Transform text using homoglyphs, honoring UI options."""
    data = request.json
    text = data.get('text', '')
    replacement_rate = float(data.get('replacement_rate', 0.3))
    
    # Option flags from UI
    subtle_only: bool = data.get('subtle', False)
    allow_cyrillic: bool = data.get('allow_cyrillic', True)
    allow_greek: bool = data.get('allow_greek', True)
    allow_numbers: bool = data.get('allow_numbers', True)

    # Build a transformer with a filtered homoglyph map according to the flags
    filtered_transformer = HomoglyphTransformer()

    # Create filtered mapping
    filtered_map = {}
    for latin, homoglyphs in filtered_transformer.homoglyph_map.items():
        if latin.isdigit() and not allow_numbers:
            continue  # Skip digit mappings completely

        allowed_list = []
        for h in homoglyphs:
            name = unicodedata.name(h, '')

            # Script filters
            if (not allow_cyrillic) and 'CYRILLIC' in name:
                continue
            if (not allow_greek) and 'GREEK' in name:
                continue

            # Subtle mode: keep only characters from Cyrillic script (visually closer)
            if subtle_only and 'CYRILLIC' not in name:
                continue

            allowed_list.append(h)

        if allowed_list:
            filtered_map[latin] = allowed_list

    # Replace maps inside the local transformer instance
    filtered_transformer.homoglyph_map = filtered_map
    filtered_transformer.reverse_map = {h: l for l, lst in filtered_map.items() for h in lst}

    # Perform transformation with the customized transformer
    transformed_text, replacement_count = filtered_transformer.transform(text, replacement_rate)

    # Analyze both texts using the same transformer instance (ensures reverse_map matches)
    original_analysis = filtered_transformer.analyze_text(text)
    transformed_analysis = filtered_transformer.analyze_text(transformed_text)
    
    # Get character comparison
    char_comparison = []
    for i, (orig_char, trans_char) in enumerate(zip(text, transformed_text)):
        if orig_char != trans_char:
            char_comparison.append({
                'position': i,
                'original': orig_char,
                'transformed': trans_char,
                'original_unicode': f'U+{ord(orig_char):04X}',
                'transformed_unicode': f'U+{ord(trans_char):04X}'
            })
    
    return jsonify({
        'original_text': text,
        'transformed_text': transformed_text,
        'replacement_count': replacement_count,
        'original_analysis': original_analysis,
        'transformed_analysis': transformed_analysis,
        'char_comparison': char_comparison,
        'visually_identical': text == transformed_text,
        'byte_identical': text.encode('utf-8') == transformed_text.encode('utf-8')
    })

@app.route('/reverse', methods=['POST'])
def reverse_transform():
    """Reverse homoglyph transformation."""
    data = request.json
    text = data.get('text', '')
    
    reversed_text = transformer.reverse_transform(text)
    
    return jsonify({
        'original_text': text,
        'reversed_text': reversed_text
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze text for homoglyphs."""
    data = request.json
    text = data.get('text', '')
    
    analysis = transformer.analyze_text(text)
    
    # Convert homoglyph_positions to a more JSON-friendly format
    positions = []
    for pos, char, latin in analysis['homoglyph_positions']:
        positions.append({
            'position': pos,
            'character': char,
            'latin_equivalent': latin,
            'unicode': f'U+{ord(char):04X}'
        })
    
    analysis['homoglyph_positions'] = positions
    
    return jsonify(analysis)

if __name__ == '__main__':
    # First create the templates directory and HTML file
    import os
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SilverSpeak POC - Homoglyph Transformer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .input-group {
            margin: 20px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        textarea {
            width: 100%;
            min-height: 150px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        .slider-container {
            margin: 20px 0;
        }
        input[type="range"] {
            width: 100%;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .results {
            margin-top: 30px;
            display: none;
        }
        .result-box {
            background-color: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .comparison-table th, .comparison-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .comparison-table th {
            background-color: #f2f2f2;
        }
        .identical {
            color: green;
        }
        .different {
            color: red;
        }
        .info-box {
            background-color: #e3f2fd;
            border: 1px solid #64b5f6;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SilverSpeak POC: Homoglyph Text Transformer</h1>
        
        <div class="info-box">
            <p><strong>About:</strong> This tool demonstrates homoglyph-based text transformation as described in the paper 
            "SilverSpeak: Evading AI-Generated Text Detectors using Homoglyphs" (arXiv:2406.11239).</p>
            <p>Homoglyphs are characters that look identical but have different Unicode values (e.g., Latin 'A' vs Cyrillic 'А').</p>
        </div>
        
        <div class="input-group">
            <label for="input-text">Input Text:</label>
            <textarea id="input-text" placeholder="Enter text to transform...">The rapid advancement of artificial intelligence has revolutionized numerous industries. Machine learning algorithms now power recommendation systems, autonomous vehicles, and medical diagnostics.</textarea>
        </div>
        
        <div class="slider-container">
            <label for="replacement-rate">Replacement Rate: <span id="rate-value">30%</span></label>
            <input type="range" id="replacement-rate" min="0" max="100" value="30" step="5">
        </div>
        
        <!-- New option controls -->
        <fieldset style="border:1px solid #ccc; padding:10px; margin-bottom:20px;">
            <legend><strong>Transformation Options</strong></legend>
            <label><input type="checkbox" id="subtle-only"> Use visually subtle homoglyphs only (Cyrillic)</label><br>
            <label><input type="checkbox" id="allow-cyrillic" checked> Enable Cyrillic homoglyphs</label><br>
            <label><input type="checkbox" id="allow-greek" checked> Enable Greek homoglyphs</label><br>
            <label><input type="checkbox" id="allow-numbers" checked> Replace numbers</label>
        </fieldset>
        
        <div>
            <button onclick="transformText()">Transform Text</button>
            <button onclick="analyzeText()">Analyze for Homoglyphs</button>
            <button onclick="reverseTransform()">Reverse Transform</button>
            <button onclick="clearAll()">Clear All</button>
        </div>
        
        <div id="results" class="results">
            <h2>Results</h2>
            
            <div class="result-box">
                <h3>Transformed Text</h3>
                <textarea id="transformed-text" readonly></textarea>
                <p>Replacements made: <span id="replacement-count">0</span></p>
                <p>Visual comparison: <span id="visual-comparison"></span></p>
                <p>Byte-level identical: <span id="byte-comparison"></span></p>
            </div>
            
            <div class="result-box">
                <h3>Character Analysis</h3>
                <div id="character-analysis"></div>
            </div>
            
            <div class="result-box">
                <h3>Detailed Character Comparison</h3>
                <table class="comparison-table" id="comparison-table">
                    <thead>
                        <tr>
                            <th>Position</th>
                            <th>Original</th>
                            <th>Transformed</th>
                            <th>Original Unicode</th>
                            <th>Transformed Unicode</th>
                        </tr>
                    </thead>
                    <tbody id="comparison-body"></tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        // Update slider value display
        document.getElementById('replacement-rate').addEventListener('input', function(e) {
            document.getElementById('rate-value').textContent = e.target.value + '%';
        });
        
        function transformText() {
            const text = document.getElementById('input-text').value;
            const rate = document.getElementById('replacement-rate').value / 100;
            
            // Read option flags
            const subtle = document.getElementById('subtle-only').checked;
            const allowCyrillic = document.getElementById('allow-cyrillic').checked;
            const allowGreek = document.getElementById('allow-greek').checked;
            const allowNumbers = document.getElementById('allow-numbers').checked;
            
            fetch('/transform', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    text: text,
                    replacement_rate: rate,
                    subtle: subtle,
                    allow_cyrillic: allowCyrillic,
                    allow_greek: allowGreek,
                    allow_numbers: allowNumbers
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('results').style.display = 'block';
                document.getElementById('transformed-text').value = data.transformed_text;
                document.getElementById('replacement-count').textContent = data.replacement_count;
                
                // Visual comparison
                const visualComp = document.getElementById('visual-comparison');
                visualComp.textContent = data.original_text === data.transformed_text ? 'Visually identical' : 'Visually different';
                visualComp.className = data.original_text === data.transformed_text ? 'identical' : 'different';
                
                // Byte comparison
                const byteComp = document.getElementById('byte-comparison');
                byteComp.textContent = data.byte_identical ? 'Yes' : 'No';
                byteComp.className = data.byte_identical ? 'identical' : 'different';
                
                // Character analysis
                const analysis = data.transformed_analysis;
                document.getElementById('character-analysis').innerHTML = `
                    <p>Total characters: ${analysis.total_characters}</p>
                    <p>Homoglyph characters: ${analysis.homoglyph_count} (${analysis.homoglyph_percentage.toFixed(1)}%)</p>
                    <p>Latin characters: ${analysis.latin_count}</p>
                `;
                
                // Character comparison table
                const tbody = document.getElementById('comparison-body');
                tbody.innerHTML = '';
                data.char_comparison.forEach(comp => {
                    const row = tbody.insertRow();
                    row.insertCell(0).textContent = comp.position;
                    row.insertCell(1).textContent = comp.original;
                    row.insertCell(2).textContent = comp.transformed;
                    row.insertCell(3).textContent = comp.original_unicode;
                    row.insertCell(4).textContent = comp.transformed_unicode;
                });
            });
        }
        
        function analyzeText() {
            const text = document.getElementById('input-text').value;
            
            fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('results').style.display = 'block';
                
                // Show analysis results
                let analysisHTML = `
                    <p>Total characters: ${data.total_characters}</p>
                    <p>Homoglyph characters found: ${data.homoglyph_count} (${data.homoglyph_percentage.toFixed(1)}%)</p>
                    <p>Latin characters: ${data.latin_count}</p>
                `;
                
                if (data.homoglyph_positions.length > 0) {
                    analysisHTML += '<h4>Homoglyphs found:</h4><ul>';
                    data.homoglyph_positions.forEach(pos => {
                        analysisHTML += `<li>Position ${pos.position}: '${pos.character}' (${pos.unicode}) → Latin '${pos.latin_equivalent}'</li>`;
                    });
                    analysisHTML += '</ul>';
                }
                
                document.getElementById('character-analysis').innerHTML = analysisHTML;
            });
        }
        
        function reverseTransform() {
            const text = document.getElementById('input-text').value;
            
            fetch('/reverse', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: text})
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('transformed-text').value = data.reversed_text;
                document.getElementById('results').style.display = 'block';
            });
        }
        
        function clearAll() {
            document.getElementById('input-text').value = '';
            document.getElementById('transformed-text').value = '';
            document.getElementById('results').style.display = 'none';
        }
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Starting web interface on http://localhost:5000")
    app.run(debug=True, port=5000) 