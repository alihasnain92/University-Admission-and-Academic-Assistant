# backend/admission_assistant/utils.py

def format_response(text):
    """Format response text with better spacing and structure"""
    lines = text.split('\n')
    formatted_lines = []
    current_section = None
    
    for line in lines:
        line = line.strip()
        if line:
            # Main heading
            if line.endswith(':'):
                if ':' in line and not line.startswith('•'):
                    formatted_lines.extend(['', line, ''])
                    current_section = line
                else:
                    formatted_lines.append(line)
            # Numbered sections
            elif any(line.startswith(f"{i}.") for i in range(1, 10)):
                formatted_lines.extend(['', line, ''])
            # Bullet points
            elif line.startswith('•'):
                formatted_lines.append(f"  {line}")
            # Normal text
            else:
                formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)