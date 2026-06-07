import os
import re

weeks_dir = r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks"

WEEK_BADGES = {
    1: "🧠 AGENTIC AWAKENING INTERFACE v1.0",
    2: "🧠 BLUEPRINT & VAULT INTERFACE v2.0",
    3: "🧠 DEEP AUTOENCODER ORACLE v3.0",
    4: "🧠 SILICON ASCENSION CONTROLLER v4.0",
    5: "🧠 FABRIC OF REALITY CONTROLLER v5.0",
    6: "🧠 CHAOS ENGINE SIMULATOR v6.0"
}

def insert_header_image(week):
    file_path = os.path.join(weeks_dir, f"week{week}", "problemset.html")
    if not os.path.exists(file_path):
        print(f"Skipping week {week}: file not found")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Check if image is already present to avoid duplicates
    if f"ams-ps-0{week}.jpg" in html or "Problem Set Header Image" in html:
        print(f"Week {week} already has a header image")
        return

    # Look for the download button link closing tag followed by its parent div closing tag
    # e.g.:
    #         </a>
    #     </div>
    
    pattern = r'(<a href="weeks/week\d+/problemset\.ipynb" download class="[^"]+">.*?</a>\s*</div>)'
    
    # We find the first match of this pattern
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        print(f"Error: Could not find header block end pattern in week {week}")
        return
        
    matched_text = match.group(1)
    
    badge = WEEK_BADGES[week]
    image_block = f"""
    <!-- Problem Set Header Image -->
    <div class="glass-card p-1.5 rounded-3xl border border-cyan-500/15 shadow-xl relative overflow-hidden w-full aspect-[2752/1536] max-h-64 my-6">
        <img 
            src="assets/images/ams-ps-0{week}.jpg" 
            alt="Problem Set {week} Banner" 
            class="w-full h-full object-cover rounded-2xl"
        >
        <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-950/25 to-transparent flex items-end p-6">
            <div class="font-mono text-xs text-cyan-400 font-bold bg-slate-950/65 px-3 py-1.5 rounded-lg border border-white/10 backdrop-blur-md select-none">
                {badge}
            </div>
        </div>
    </div>"""

    # Replace the match with itself followed by the new image block
    new_html = html.replace(matched_text, matched_text + "\n" + image_block)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"Successfully inserted header image for week {week}")

if __name__ == "__main__":
    for w in range(1, 7):
        insert_header_image(w)
    print("All image insertions completed!")
