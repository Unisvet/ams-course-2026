import os
import re
import json
import urllib.parse

# Define paths
scratch_dir = r"C:\Users\SvetlanaMeissner\.gemini\antigravity\brain\30db38af-b878-4670-8a03-3980fe6af772\scratch"
weeks_dir = r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks"

def clean_latex(latex):
    # URL decode
    latex = urllib.parse.unquote(latex)
    
    # Strip trailing #0 or #
    if latex.endswith('#0'):
        latex = latex[:-2]
    elif latex.endswith('#'):
        latex = latex[:-1]
        
    # Clean up escaped underscores and parentheses
    latex = latex.replace(r'\(', '(').replace(r'\)', ')')
    latex = latex.replace(r'\_', '_')
    # Clean up multiple backslashes preceding a command letter or brace (e.g. \\omega -> \omega)
    # but preserve \\ for newlines (e.g. in matrices)
    latex = re.sub(r'\\{2,}([a-zA-Z\{\}])', r'\\\1', latex)
    return latex.strip()

def preprocess_markdown(text):
    # 1. Replace CodeCogs links with a robust nested parenthesis scanner
    start_str = "[](https://www.codecogs.com/eqnedit.php?latex="
    while True:
        idx = text.find(start_str)
        if idx == -1:
            break
            
        paren_start = idx + 2 # This is the opening '(' of the markdown link
        
        # Scan to find the matching closing parenthesis of the markdown link
        balance = 0
        paren_end = -1
        for j in range(paren_start, len(text)):
            char = text[j]
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance == 0:
                    paren_end = j
                    break
        
        if paren_end == -1:
            # Parse error, replace the start string to avoid infinite loop
            text = text.replace(start_str, "STRAY_COGS_LINK", 1)
            continue
            
        # The URL is from paren_start + 1 to paren_end
        # The latex parameter starts after "https://www.codecogs.com/eqnedit.php?latex="
        latex_start_offset = len("https://www.codecogs.com/eqnedit.php?latex=")
        latex_url = text[paren_start + 1 + latex_start_offset : paren_end]
        
        latex = clean_latex(latex_url)
        
        # Replace the entire link block `[](https://...latex=...)` with the LaTeX string
        text = text[:idx] + f" \\({latex}\\) " + text[paren_end+1:]
        
    # Also clean up any placeholder replacements
    text = text.replace("STRAY_COGS_LINK", " ")

    # 2. Replace quadruple-dollar equations in Part 2: $$$$equation$$$$
    def replace_quad_dollars(match):
        latex = match.group(1)
        latex = clean_latex(latex)
        return f" \\({latex}\\) "
    
    text = re.sub(r'\$\$\$\$(.*?)\$\$\$\$', replace_quad_dollars, text)
    
    # 3. Replace double-dollar equations: $$equation$$
    def replace_double_dollars(match):
        latex = match.group(1)
        latex = clean_latex(latex)
        return f" \\({latex}\\) "
        
    text = re.sub(r'\$\$(.*?)\$\$', replace_double_dollars, text)
    
    # 4. Clean up stray markdown escapes in formulas in the whole text
    text = re.sub(r'\\{2,}([a-zA-Z\{\}])', r'\\\1', text)
    text = text.replace(r'\_', '_')
    
    return text

def render_table_html(table_rows):
    html_chunk = []
    html_chunk.append('<div class="overflow-x-auto my-4 border border-slate-800 rounded-xl">')
    html_chunk.append('    <table class="min-w-full divide-y divide-slate-800 text-sm">')
    
    headers_parsed = False
    for r_idx, row in enumerate(table_rows):
        cells = [c.strip() for c in row.split('|')[1:-1]]
        if not cells:
            continue
        # If it's a separator line like |:---:|:---:|
        if all(re.match(r'^:?-+:?$', c) for c in cells):
            continue
        
        if not headers_parsed:
            html_chunk.append('        <thead class="bg-slate-900/30">')
            html_chunk.append('            <tr>')
            for cell in cells:
                html_chunk.append(f'                <th class="px-4 py-3 text-left text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">{cell}</th>')
            html_chunk.append('            </tr>')
            html_chunk.append('        </thead>')
            html_chunk.append('        <tbody class="divide-y divide-slate-850 bg-slate-950/10">')
            headers_parsed = True
        else:
            html_chunk.append('            <tr class="hover:bg-slate-900/20 transition-colors">')
            for cell in cells:
                cell_clean = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', cell)
                html_chunk.append(f'                <td class="px-4 py-3 text-slate-300 font-mono text-xs">{cell_clean}</td>')
            html_chunk.append('            </tr>')
    if headers_parsed:
        html_chunk.append('        </tbody>')
    html_chunk.append('    </table>')
    html_chunk.append('</div>')
    return html_chunk

def markdown_to_html(md_text, week_id):
    lines = md_text.split('\n')
    html_lines = []
    
    in_list = False
    in_ordered_list = False
    in_code_block = False
    code_block_lines = []
    in_table = False
    table_rows = []
    
    # Title and metadata info
    title = f"Problem Set {week_id}"
    weight = "40% of module grade"
    if week_id == 1:
        title = "Problem Set 1: Project Genesis – The Agentic Awakening"
        weight = "20% of Module 1 grade (4 Points)"
    elif week_id == 2:
        title = "Problem Set 2: Project Genesis – The Blueprint & The Vault"
        weight = "40% of Module 1 grade (4 Points)"
    elif week_id == 3:
        title = "Problem Set 3: Project Genesis – The Oracle Awakens"
        weight = "40% of Module 1 grade (4 Points)"
    elif week_id == 4:
        title = "Problem Set 4: Project Genesis – The Silicon Ascension"
        weight = "40% of Module 2 grade (4 Points)"
    elif week_id == 5:
        title = "Problem Set 5: Project Genesis – The Fabric of Reality"
        weight = "40% of Module 2 grade (4 Points)"
    elif week_id == 6:
        title = "Problem Set 6: Project Genesis – The Chaos Engine"
        weight = "40% of Module 2 grade (4 Points)"
    elif week_id == 7:
        title = "Problem Set 7: The Cerebral Nexus – Awakening Cognitive Control"
        weight = "40% of Module 3 grade (4 Points)"

    html_lines.append('<div class="space-y-8">')
    html_lines.append('    <!-- Header Block -->')
    html_lines.append('    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-900 pb-6">')
    html_lines.append('        <div>')
    html_lines.append('            <span class="px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-400 text-xs font-mono font-bold uppercase tracking-wider border border-slate-750">Programming Assignment</span>')
    html_lines.append(f'            <h3 class="text-2xl font-black text-white mt-2">{title}</h3>')
    html_lines.append(f'            <p class="text-sm text-slate-455 mt-1">Deadline: TBA | Weight: {weight} | Quiz: 1 Point</p>')
    html_lines.append('        </div>')
    html_lines.append(f'        <a href="weeks/week{week_id}/problemset.ipynb" download class="px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-cyan-500/50 hover:bg-cyan-500/5 text-xs font-mono font-bold text-cyan-400 flex items-center gap-2 transition-all duration-200 hover:scale-105 active:scale-95 shadow-lg shadow-cyan-500/5">')
    html_lines.append('            <span>📥</span> Download Jupyter Notebook')
    html_lines.append('        </a>')
    html_lines.append('    </div>')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Skip top level titles
        if stripped.startswith('# **PS-') or (stripped.startswith('# **Problem Set') and week_id == int(stripped.split('Set')[1].split(':')[0].strip() if 'Set' in stripped and ':' in stripped else week_id)):
            i += 1
            continue
            
        if stripped.startswith('# **Problem Set'):
            i += 1
            continue

        # Code block handling
        if stripped.startswith('```'):
            if in_code_block:
                in_code_block = False
                code_content = '\n'.join(code_block_lines)
                code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                html_lines.append(f'<pre class="bg-slate-950 p-4 rounded-xl border border-slate-850 overflow-x-auto text-xs font-mono text-cyan-400"><code class="language-python">{code_content}</code></pre>')
                code_block_lines = []
            else:
                in_code_block = True
            i += 1
            continue
            
        if in_code_block:
            code_block_lines.append(line)
            i += 1
            continue

        # Table ending check
        if in_table and not stripped.startswith('|'):
            in_table = False
            html_lines.extend(render_table_html(table_rows))
            table_rows = []
            continue

        # Markdown tables handling
        if stripped.startswith('|') and not in_code_block:
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(stripped)
            i += 1
            continue

        # Empty lines
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            i += 1
            continue

        # Section headers
        is_story = "The Story" in stripped or "Theoretical Deep Dive" in stripped or "System Requirements" in stripped
        is_submission = "Submission" in stripped or "Deliverables" in stripped or "Choose Your Weapon" in stripped or "Gamified Rules" in stripped

        if stripped.startswith('###') or stripped.startswith('##') or stripped.startswith('####'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
                
            header_text = stripped.lstrip('#').strip()
            header_text = re.sub(r'\*\*(.*?)\*\*', r'\1', header_text)
            
            div_count = sum(1 for line in html_lines if '<div' in line) - sum(1 for line in html_lines if '</div' in line)
            while div_count > 1:
                html_lines.append('</div>')
                div_count -= 1
                
            if is_story:
                html_lines.append(f'<div class="p-6 glass-card rounded-2xl border-l-4 border-cyan-500 bg-cyan-950/5 space-y-3 my-6">')
                html_lines.append(f'    <h4 class="text-cyan-400 font-bold text-lg flex items-center gap-2">')
                html_lines.append(f'        {header_text}')
                html_lines.append(f'    </h4>')
            elif is_submission:
                html_lines.append(f'<div class="p-6 glass-card rounded-2xl border-l-4 border-amber-500 bg-amber-500/5 space-y-3 my-6">')
                html_lines.append(f'    <h4 class="text-amber-400 font-mono text-sm font-bold uppercase tracking-wider flex items-center gap-2">')
                html_lines.append(f'        {header_text}')
                html_lines.append(f'    </h4>')
            else:
                html_lines.append(f'<h4 class="text-lg font-bold text-white border-b border-slate-850 pb-2 mt-8 mb-4 flex items-center gap-2">')
                if "Exercise" in header_text:
                    html_lines.append(f'    <span class="text-cyan-400">⚡</span> {header_text}')
                else:
                    html_lines.append(f'    {header_text}')
                html_lines.append(f'</h4>')
            i += 1
            continue

        if stripped == '----' or stripped == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
                
            div_count = sum(1 for line in html_lines if '<div' in line) - sum(1 for line in html_lines if '</div' in line)
            while div_count > 1:
                html_lines.append('</div>')
                div_count -= 1
                
            html_lines.append('<hr class="border-slate-900 my-8">')
            i += 1
            continue

        # Ordered lists
        ordered_match = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if ordered_match and not in_code_block:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if not in_ordered_list:
                html_lines.append('<ol class="list-decimal pl-6 text-sm text-slate-300 space-y-3">')
                in_ordered_list = True
                
            item_text = ordered_match.group(2)
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', item_text)
            item_text = re.sub(r'`(.*?)`', r'<code class="text-cyan-400 font-mono bg-slate-900/60 px-1.5 py-0.5 rounded text-xs">\1</code>', item_text)
            html_lines.append(f'    <li class="leading-relaxed">{item_text}</li>')
            i += 1
            continue

        # Bullet lists
        bullet_match = re.match(r'^[-*]\s+(.*)$', stripped)
        if bullet_match and not in_code_block:
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            if not in_list:
                html_lines.append('<ul class="list-disc pl-6 text-sm text-slate-350 space-y-2">')
                in_list = True
                
            item_text = bullet_match.group(1)
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', item_text)
            item_text = re.sub(r'`(.*?)`', r'<code class="text-cyan-400 font-mono bg-slate-900/60 px-1.5 py-0.5 rounded text-xs">\1</code>', item_text)
            html_lines.append(f'    <li class="leading-relaxed">{item_text}</li>')
            i += 1
            continue

        # Standard text paragraphs
        p_text = stripped
        p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', p_text)
        p_text = re.sub(r'`(.*?)`', r'<code class="text-cyan-400 font-mono bg-slate-900/60 px-1.5 py-0.5 rounded text-xs">\1</code>', p_text)
        p_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-cyan-400 hover:underline" target="_blank">\1</a>', p_text)
        
        html_lines.append(f'<p class="text-sm text-slate-300 leading-relaxed">{p_text}</p>')
        i += 1

    # End of file cleanup
    if in_table:
        html_lines.extend(render_table_html(table_rows))
    if in_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')
        
    div_count = sum(1 for line in html_lines if '<div' in line) - sum(1 for line in html_lines if '</div' in line)
    while div_count > 0:
        html_lines.append('</div>')
        div_count -= 1
        
    return '\n'.join(html_lines)


def generate_ipynb(md_text, week_id):
    cells = []
    parts = re.split(r'(```python.*?```)', md_text, flags=re.DOTALL)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        if part.startswith('```python'):
            code_lines = part.replace('```python', '').replace('```', '').strip().split('\n')
            code_lines = [line + '\n' for line in code_lines]
            if code_lines:
                code_lines[-1] = code_lines[-1].rstrip('\n')
                
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code_lines
            })
        else:
            # Convert LaTeX format to standard Jupyter notebook format ($...$ and $$...$$)
            jupyter_md = part
            jupyter_md = jupyter_md.replace('\\(', '$').replace('\\)', '$')
            jupyter_md = jupyter_md.replace('\\[', '$$').replace('\\]', '$$')
            
            md_lines = jupyter_md.split('\n')
            md_lines = [line + '\n' for line in md_lines]
            if md_lines:
                md_lines[-1] = md_lines[-1].rstrip('\n')
                
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": md_lines
            })
            
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3 (ipykernel)",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    return notebook

# Main runner loop
for week in range(1, 8):
    file_path = os.path.join(scratch_dir, f"part_{week}.md")
    if not os.path.exists(file_path):
        print(f"Skipping week {week}: part file not found")
        continue
        
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
        
    # Preprocess equations and LaTeX elements
    clean_md = preprocess_markdown(raw_content)
    
    # 1. Generate HTML
    html_content = markdown_to_html(clean_md, week)
    
    # Make sure folder exists
    week_folder = os.path.join(weeks_dir, f"week{week}")
    os.makedirs(week_folder, exist_ok=True)
    
    html_out_path = os.path.join(week_folder, "problemset.html")
    with open(html_out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(html_content)
    print(f"Generated HTML for week {week} -> {html_out_path}")
    
    # 2. Generate Jupyter Notebook (.ipynb)
    ipynb_data = generate_ipynb(clean_md, week)
    ipynb_out_path = os.path.join(week_folder, "problemset.ipynb")
    with open(ipynb_out_path, 'w', encoding='utf-8') as out_f:
        json.dump(ipynb_data, out_f, indent=1)
    print(f"Generated Notebook for week {week} -> {ipynb_out_path}")
