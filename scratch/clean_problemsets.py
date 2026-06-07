import os
import re

weeks_dir = r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks"

# Emojis replacements using explicit unicode sequences
EMOJI_REPLACEMENTS = {
    "\u00f0\u009f\u0093\u0096": "📖",
    "\u00f0\u009f\u0096\u00a5\ufe0f": "🖥️",
    "\u00f0\u009f\u00a7\u00a0": "🧠",
    "\u00f0\u009f\u008e\u00ae": "🎮"
}

def clean_common_stuff(html):
    # Fix emojis
    for bad, good in EMOJI_REPLACEMENTS.items():
        html = html.replace(bad, good)
    
    # Fix empty/double asterisk paragraphs
    html = re.sub(r'<p class="text-sm text-slate-300 leading-relaxed">\*\*</p>', '', html)
    html = re.sub(r'<p class="text-sm text-slate-300 leading-relaxed">\s*\*\*\s*</p>', '', html)
    html = re.sub(r'<h4 class="text-lg font-bold text-white border-b border-slate-850 pb-2 mt-8 mb-4 flex items-center gap-2">\s*\*\*\s*</h4>', '', html)
    
    return html

def clean_week1():
    file_path = os.path.join(weeks_dir, "week1", "problemset.html")
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    html = clean_common_stuff(html)
    
    # Code block for gemini-cli
    bad_cli = '<p class="text-sm text-slate-300 leading-relaxed">Ask gemini-cli "In one sentence, what is the paradigm shift from classical block-diagram simulation to Agentic Engineering?"</p>'
    good_cli = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-bash">gemini-cli "In one sentence, what is the paradigm shift from classical block-diagram simulation to Agentic Engineering?"</code></pre>
</div>'''
    html = html.replace(bad_cli, good_cli)
    
    # Code block for Prompt Example
    bad_prompt = '<li class="leading-relaxed"><strong class="text-white">Prompt Example:</strong> *"Write a bash script that creates a modern Python project structure with directories src/, data/, agents/, and docs/. Inside src/, create an empty main.py. Output only the executable bash code."*</li>'
    good_prompt = '''<li class="leading-relaxed">
    <strong class="text-white">Prompt Example:</strong>
    <div class="my-3 max-w-2xl">
        <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-text">Write a bash script that creates a modern Python project structure with directories src/, data/, agents/, and docs/. Inside src/, create an empty main.py. Output only the executable bash code.</code></pre>
    </div>
</li>'''
    html = html.replace(bad_prompt, good_prompt)
    
    # End of file cleanup
    html = re.sub(r'</ol>\s*</div>\s*$', '</ol>\n</div>', html.strip())
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Cleaned Week 1 Problem Set")

def clean_week2():
    file_path = os.path.join(weeks_dir, "week2", "problemset.html")
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = clean_common_stuff(html)
    
    # macOS/Linux / Windows commands
    bad_installs = '''<ul class="list-disc pl-6 text-sm text-slate-350 space-y-2">
    <li class="leading-relaxed">*macOS/Linux:* curl -LsSf https://astral.sh/uv/install.sh | sh</li>
    <li class="leading-relaxed">*Windows:* powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"</li>
    <li class="leading-relaxed">You can also ask your coding Agent\\!</li>
</ul>'''
    good_installs = '''<div class="my-4 max-w-2xl space-y-4">
    <div>
        <div class="text-xs text-slate-400 font-mono mb-1">macOS / Linux:</div>
        <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-bash">curl -LsSf https://astral.sh/uv/install.sh | sh</code></pre>
    </div>
    <div>
        <div class="text-xs text-slate-400 font-mono mb-1">Windows:</div>
        <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-powershell">powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"</code></pre>
    </div>
    <p class="text-xs text-slate-400 font-sans italic">Note: You can also ask your coding agent to install it for you!</p>
</div>'''
    html = html.replace(bad_installs, good_installs)
    
    # uv init and cd
    bad_init = '<p class="text-sm text-slate-300 leading-relaxed">uv init genesis-oracle</p>\n<p class="text-sm text-slate-300 leading-relaxed">cd genesis-oracle</p>'
    good_init = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-bash">uv init genesis-oracle
cd genesis-oracle</code></pre>
</div>'''
    html = html.replace(bad_init, good_init)
    
    # Prompt Example
    bad_prompt = '<p class="text-sm text-slate-300 leading-relaxed">*"My remote URL is \\[YOUR_GITHUB_URL\\]. Please write the terminal commands to initialize git, stage all files respecting the* *.gitignore**, create a commit with the message \'Initial Genesis Vault setup\', and push it to the main branch."*</p>'
    good_prompt = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-text">My remote URL is [YOUR_GITHUB_URL]. Please write the terminal commands to initialize git, stage all files respecting the .gitignore, create a commit with the message 'Initial Genesis Vault setup', and push it to the main branch.</code></pre>
</div>'''
    html = html.replace(bad_prompt, good_prompt)
    
    # uv add
    bad_add = '<p class="text-sm text-slate-300 leading-relaxed">uv add "keras\\>=3.0.7" jax jaxlib numpy scipy matplotlib</p>'
    good_add = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-bash">uv add "keras&gt;=3.0.7" jax jaxlib numpy scipy matplotlib</code></pre>
</div>'''
    html = html.replace(bad_add, good_add)
    
    # uv run
    bad_run = '<p class="text-sm text-slate-300 leading-relaxed">uv run python src/oracle_setup.py</p>'
    good_run = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-bash">uv run python src/oracle_setup.py</code></pre>
</div>'''
    html = html.replace(bad_run, good_run)
    
    # Remove Bash paragraph header
    html = html.replace('<p class="text-sm text-slate-300 leading-relaxed">Bash</p>\n</ol>', '</ol>')
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Cleaned Week 2 Problem Set")

def clean_week3():
    file_path = os.path.join(weeks_dir, "week3", "problemset.html")
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = clean_common_stuff(html)
    
    # git clone / cd
    bad_clone = '<p class="text-sm text-slate-300 leading-relaxed">\\!git clone \\[YOUR_REPO_URL\\]</p>\n<p class="text-sm text-slate-300 leading-relaxed">%cd genesis-oracle</p>'
    good_clone = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-bash">!git clone [YOUR_REPO_URL]
%cd genesis-oracle</code></pre>
</div>'''
    html = html.replace(bad_clone, good_clone)
    
    # pip install / uv pip install
    bad_pip = '<p class="text-sm text-slate-300 leading-relaxed">\\!pip install uv</p>\n<p class="text-sm text-slate-300 leading-relaxed">\\!uv pip install --system -r pyproject.toml</p>'
    good_pip = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-bash">!pip install uv
!uv pip install --system -r pyproject.toml</code></pre>
</div>'''
    html = html.replace(bad_pip, good_pip)
    
    # Prompt Example
    bad_prompt = '<p class="text-sm text-slate-300 leading-relaxed">*"I have built this dense Autoencoder for time-series anomaly detection in Keras 3. To better capture the non-stationary, temporal nature of this physical signal, please rewrite my Encoder and Decoder classes to utilize 1D Convolutional Layers (<strong class="text-white">Conv1D* *and* *Conv1DTranspose</strong>). Explain how the tensor shapes change during the forward pass."*</p>'
    good_prompt = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-text">I have built this dense Autoencoder for time-series anomaly detection in Keras 3. To better capture the non-stationary, temporal nature of this physical signal, please rewrite my Encoder and Decoder classes to utilize 1D Convolutional Layers (Conv1D and Conv1DTranspose). Explain how the tensor shapes change during the forward pass.</code></pre>
</div>'''
    html = html.replace(bad_prompt, good_prompt)
    
    # Remove Bash paragraph header
    html = html.replace('<p class="text-sm text-slate-300 leading-relaxed">Bash</p>\n</ol>', '</ol>')
    html = html.replace('<p class="text-sm text-slate-300 leading-relaxed">Bash</p>', '')
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Cleaned Week 3 Problem Set")

def clean_week4():
    file_path = os.path.join(weeks_dir, "week4", "problemset.html")
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = clean_common_stuff(html)
    
    # Prompt Example
    bad_prompt = '<p class="text-sm text-slate-300 leading-relaxed">*"Observer-Prime, we are migrating our neural architecture to pure JAX. Please write a simple Python script using* *flax.linen* *to define a Multi-Layer Perceptron (MLP) module. More importantly, write a heavily commented execution block demonstrating how Flax explicitly separates model initialization (<strong class="text-white">model.init* *with a* *jax.random.PRNGKey</strong>) from the forward pass (<strong class="text-white">model.apply</strong>), highlighting its stateless nature compared to Keras."*</p>'
    good_prompt = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-text">Observer-Prime, we are migrating our neural architecture to pure JAX. Please write a simple Python script using flax.linen to define a Multi-Layer Perceptron (MLP) module. More importantly, write a heavily commented execution block demonstrating how Flax explicitly separates model initialization (model.init with a jax.random.PRNGKey) from the forward pass (model.apply), highlighting its stateless nature compared to Keras.</code></pre>
</div>'''
    html = html.replace(bad_prompt, good_prompt)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Cleaned Week 4 Problem Set")

def clean_week5():
    file_path = os.path.join(weeks_dir, "week5", "problemset.html")
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = clean_common_stuff(html)
    
    # Prompt 1
    bad_prompt1 = '<li class="leading-relaxed"><strong class="text-white">The Prompt (Architecture):</strong> Feed your Agent the following prompt (you may adjust it slightly, but the core instructions must remain):*"Observer-Prime, we are transcending classical grid-based solvers to build a PINN. Please write a pure JAX/Flax script using flax.linen that defines a Multi-Layer Perceptron named HeatSurrogate. It must take continuous 2D inputs (space x and time t) and predict a 1D scalar (temperature u). Use 4 hidden layers with 32 neurons each and tanh activation functions (since we need smooth, non-zero second derivatives for our physics constraints). Include an execution block demonstrating how to initialize the model\'s weights explicitly using jax.random.PRNGKey."*</li>'
    good_prompt1 = '''<li class="leading-relaxed">
    <strong class="text-white">The Prompt (Architecture):</strong> Feed your Agent the following prompt (you may adjust it slightly, but the core instructions must remain):
    <div class="my-3 max-w-3xl">
        <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-text">Observer-Prime, we are transcending classical grid-based solvers to build a PINN. Please write a pure JAX/Flax script using flax.linen that defines a Multi-Layer Perceptron named HeatSurrogate. It must take continuous 2D inputs (space x and time t) and predict a 1D scalar (temperature u). Use 4 hidden layers with 32 neurons each and tanh activation functions (since we need smooth, non-zero second derivatives for our physics constraints). Include an execution block demonstrating how to initialize the model's weights explicitly using jax.random.PRNGKey.</code></pre>
    </div>
</li>'''
    html = html.replace(bad_prompt1, good_prompt1)
    
    # Prompt 2
    bad_prompt2 = '<li class="leading-relaxed"><strong class="text-white">Agentic Pair-Programming (The Residual):</strong> Calculating the second derivative of a neural network output with respect to its inputs in pure JAX requires nesting jax.grad. This can be syntactically tricky. Ask Observer-Prime:*"Observer-Prime, I have a pure forward function predict_u(params, x, t) that returns a scalar temperature. How do I use jax.grad (or jax.hessian/jax.jacrev) to calculate the exact analytical first derivative with respect to t (* \(u_t\) *), and the second derivative with respect to x (* \(u_{xx}\) *)? Please write a physics_loss function that computes the Mean Squared Error of the PDE residual:*  \((u_t - \alpha u_{xx})^2\) *. Ensure it is vectorized using jax.vmap so it can evaluate all 5,000 collocation points in parallel."*</li>'
    good_prompt2 = '''<li class="leading-relaxed">
    <strong class="text-white">Agentic Pair-Programming (The Residual):</strong> Calculating the second derivative of a neural network output with respect to its inputs in pure JAX requires nesting jax.grad. This can be syntactically tricky. Ask Observer-Prime:
    <div class="my-3 max-w-3xl">
        <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-text">Observer-Prime, I have a pure forward function predict_u(params, x, t) that returns a scalar temperature. How do I use jax.grad (or jax.hessian/jax.jacrev) to calculate the exact analytical first derivative with respect to t (u_t), and the second derivative with respect to x (u_{xx})? Please write a physics_loss function that computes the Mean Squared Error of the PDE residual: (u_t - \alpha u_{xx})^2. Ensure it is vectorized using jax.vmap so it can evaluate all 5,000 collocation points in parallel.</code></pre>
    </div>
</li>'''
    html = html.replace(bad_prompt2, good_prompt2)
    
    # Prompt 3
    bad_prompt3 = '<li class="leading-relaxed"><strong class="text-white">The FNO Endgame:</strong> Your trained PINN is a masterpiece, but it has a critical flaw: it only knows how to solve the heat equation for the exact initial condition  \(u_{true}(x, 0) = -\\sin(\\pi x)\) . If the factory changes the starting temperature to a square wave, you must retrain the network from scratch. Return to your ADE and prompt Observer-Prime:*"Observer-Prime, our PINN is beautiful but limited to a single initial condition. Explain to me - in 3 concise bullet points - how a Fourier Neural Operator (FNO) solves this scalability problem. How does an FNO map functional spaces compared to a PINN, and why does doing convolutions in the frequency domain allow it to achieve \'Zero-Shot\' predictions for entirely new initial conditions?"*</li>'
    good_prompt3 = '''<li class="leading-relaxed">
    <strong class="text-white">The FNO Endgame:</strong> Your trained PINN is a masterpiece, but it has a critical flaw: it only knows how to solve the heat equation for the exact initial condition  \(u_{true}(x, 0) = -\\sin(\\pi x)\) . If the factory changes the starting temperature to a square wave, you must retrain the network from scratch. Return to your ADE and prompt Observer-Prime:
    <div class="my-3 max-w-3xl">
        <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-text">Observer-Prime, our PINN is beautiful but limited to a single initial condition. Explain to me - in 3 concise bullet points - how a Fourier Neural Operator (FNO) solves this scalability problem. How does an FNO map functional spaces compared to a PINN, and why does doing convolutions in the frequency domain allow it to achieve 'Zero-Shot' predictions for entirely new initial conditions?</code></pre>
    </div>
</li>'''
    html = html.replace(bad_prompt3, good_prompt3)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Cleaned Week 5 Problem Set")

def clean_week6():
    file_path = os.path.join(weeks_dir, "week6", "problemset.html")
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    html = clean_common_stuff(html)
    
    # python block for jax.random.split
    bad_code = '<p class="text-sm text-slate-300 leading-relaxed">import jax</p>\n<p class="text-sm text-slate-300 leading-relaxed">key = jax.random.PRNGKey(42)</p>\n<p class="text-sm text-slate-300 leading-relaxed">key_distribution, key_agent = jax.random.split(key, 2)</p>'
    good_code = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-python">import jax
key = jax.random.PRNGKey(42)
key_distribution, key_agent = jax.random.split(key, 2)</code></pre>
</div>'''
    html = html.replace(bad_code, good_code)
    
    # Swarm prompt block
    bad_swarm = '''"Observer-Prime, initiate an automated task sweep inside the Antigravity IDE sandbox. Utilize your filesystem and bash skills to evaluate our src/monte_carlo.py pipeline.
<ul class="list-disc pl-6 text-sm text-slate-350 space-y-2">
    <li class="leading-relaxed">Spawn <strong class="text-white">Subagent-Alpha (\'The Stress-Tester\')</strong>: This subagent must programmatically alter the variance parameters ( \\(\\sigma\\) ) of the Log-Normal asset cost distribution in src/monte_carlo.py to find the breaking point where the  \\(VaR_{95\\%}\\)  drops below zero.</li>
    <li class="leading-relaxed">Spawn <strong class="text-white">Subagent-Beta (\'The Profiler\')</strong>: This subagent must execute the script sequentially twice and extract execution times to profile the exact performance overhead of the initial JAX compilation trace versus the second warm execution pass.</li>
<p class="text-sm text-slate-300 leading-relaxed">Synthesize all agentic findings into a unified report named docs/Swarm_Stress_Report.md."</p>
</ul>'''
    good_swarm = '''<div class="my-3 max-w-3xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-text">Observer-Prime, initiate an automated task sweep inside the Antigravity IDE sandbox. Utilize your filesystem and bash skills to evaluate our src/monte_carlo.py pipeline.
- Spawn Subagent-Alpha ('The Stress-Tester'): This subagent must programmatically alter the variance parameters (sigma) of the Log-Normal asset cost distribution in src/monte_carlo.py to find the breaking point where the VaR_95% drops below zero.
- Spawn Subagent-Beta ('The Profiler'): This subagent must execute the script sequentially twice and extract execution times to profile the exact performance overhead of the initial JAX compilation trace versus the second warm execution pass.
Synthesize all agentic findings into a unified report named docs/Swarm_Stress_Report.md.</code></pre>
</div>'''
    html = html.replace(bad_swarm, good_swarm)
    
    # uv add
    bad_add = '<p class="text-sm text-slate-300 leading-relaxed">uv add plotly openpyxl matplotlib</p>'
    good_add = '''<div class="my-3 max-w-2xl">
    <pre class="bg-slate-950/85 border border-slate-850 rounded-xl p-4 font-mono text-xs text-slate-300 overflow-x-auto shadow-inner"><code class="language-bash">uv add plotly openpyxl matplotlib</code></pre>
</div>'''
    html = html.replace(bad_add, good_add)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Cleaned Week 6 Problem Set")

if __name__ == "__main__":
    clean_week1()
    clean_week2()
    clean_week3()
    clean_week4()
    clean_week5()
    clean_week6()
    print("All cleaning completed!")
