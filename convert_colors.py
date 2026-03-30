#!/usr/bin/env python3
"""Convert Xcode .xccolortheme RGBA values (0-1 float) to hex colors."""

import xml.etree.ElementTree as ET
import json
import sys

def rgba_to_hex(rgba_str):
    """Convert '0.5 0.3 0.2 1' to '#804D33' (or '#804D33CC' if alpha < 1)."""
    parts = rgba_str.strip().split()
    r = round(float(parts[0]) * 255)
    g = round(float(parts[1]) * 255)
    b = round(float(parts[2]) * 255)
    a = float(parts[3])
    
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    if a >= 0.999:
        return f"#{r:02X}{g:02X}{b:02X}"
    else:
        a_int = max(0, min(255, round(a * 255)))
        return f"#{r:02X}{g:02X}{b:02X}{a_int:02X}"

def parse_xccolortheme(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    # The root dict
    main_dict = root.find('dict')
    keys = main_dict.findall('key')
    
    result = {}
    children = list(main_dict)
    
    i = 0
    while i < len(children):
        if children[i].tag == 'key':
            key_name = children[i].text
            value_elem = children[i + 1]
            
            if value_elem.tag == 'string' and key_name.startswith('DVT') and 'Font' not in key_name and 'Version' not in key_name:
                # Check if it looks like a color value (space-separated floats)
                text = value_elem.text.strip()
                parts = text.split()
                if len(parts) == 4:
                    try:
                        [float(p) for p in parts]
                        result[key_name] = {
                            'raw': text,
                            'hex': rgba_to_hex(text)
                        }
                    except ValueError:
                        pass
            elif value_elem.tag == 'dict':
                # Syntax colors dict
                sub_children = list(value_elem)
                j = 0
                while j < len(sub_children):
                    if sub_children[j].tag == 'key':
                        sub_key = sub_children[j].text
                        sub_val = sub_children[j + 1]
                        if sub_val.tag == 'string':
                            text = sub_val.text.strip()
                            parts = text.split()
                            if len(parts) == 4:
                                try:
                                    [float(p) for p in parts]
                                    full_key = f"{key_name}.{sub_key}"
                                    result[full_key] = {
                                        'raw': text,
                                        'hex': rgba_to_hex(text)
                                    }
                                except ValueError:
                                    pass
                        j += 2
                    else:
                        j += 1
            i += 2
        else:
            i += 1
    
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: convert_colors.py <path-to-.xccolortheme>", file=sys.stderr)
        sys.exit(1)
    filepath = sys.argv[1]
    colors = parse_xccolortheme(filepath)
    
    print(json.dumps(colors, indent=2))
