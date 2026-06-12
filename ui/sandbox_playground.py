import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI

# Dictionary of code snippets for each experiment
CODE_TEMPLATES = {
    3: '''# Exp 3: Document Summarizer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader

# 1. Load document
loader = PyPDFLoader("document.pdf")
docs = loader.load()

# 2. Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

# 3. Load map-reduce summarization chain
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")

# 4. Generate summary
summary = summary_chain.run(docs)
print("Executive Summary:\\n", summary)
''',
    4: '''# Exp 4: PDF Structure & Table Parser
import pdfplumber
import pandas as pd

# 1. Open PDF with layout scanning
with pdfplumber.open("invoice_report.pdf") as pdf:
    # 2. Extract text from first page
    first_page = pdf.pages[0]
    raw_text = first_page.extract_text()
    
    # 3. Extract tables
    tables = first_page.extract_tables()
    for idx, table in enumerate(tables):
        df = pd.DataFrame(table[1:], columns=table[0])
        print(f"Table {idx + 1}:\\n", df)
''',
    5: '''# Exp 5: Text Similarity & Vector Embeddings
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Initialize sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Define text inputs
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "A swift auburn fox leaps across the inactive hound."
]

# 3. Compute vector embeddings
embeddings = model.encode(sentences)

# 4. Calculate cosine similarity
similarity = cosine_similarity([embeddings[0]], [embeddings[1]])
print(f"Cosine Similarity Score: {similarity[0][0]:.4f}")
''',
    6: '''# Exp 6: Named Entity Recognition (NER)
import spacy

# 1. Load English NLP engine
nlp = spacy.load("en_core_web_sm")

# 2. Process input text
text = "Apple Inc. was founded by Steve Jobs in Cupertino, California on April 1, 1976."
doc = nlp(text)

# 3. Extract and display entities
for ent in doc.ents:
    print(f"Entity: {ent.text:<25} | Label: {ent.label_:<10} | Meaning: {spacy.explain(ent.label_)}")
''',
    7: '''# Exp 7: Sentiment & Emotion Classifier
from transformers import pipeline

# 1. Initialize HuggingFace pipeline
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# 2. Classify input text
text = "I absolutely love the new user interface! It is extremely smooth."
result = classifier(text)[0]

# 3. Output predictions
print(f"Sentiment Label: {result['label']} | Confidence: {result['score']:.4f}")
''',
    8: '''# Exp 8: Text Classification & Intent Detection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# 1. Prepare training data
train_texts = ["Check bank balance", "Reset user password", "Transfer money", "Lock my account"]
train_labels = ["account_inquiry", "auth_reset", "transaction", "security_lock"]

# 2. Vectorize texts using TF-IDF
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)

# 3. Train Classifier
clf = LinearSVC()
clf.fit(X_train, train_labels)

# 4. Predict incoming intent
test_query = ["I want to change my passcode"]
X_test = vectorizer.transform(test_query)
print("Detected Intent:", clf.predict(X_test)[0])
''',
    9: '''# Exp 9: Keyword & Key-phrase Extractor
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Document corpus
text = ["Retrieval-Augmented Generation is an architectural pattern that improves LLM responses."]

# 2. Compute TF-IDF scores
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
tfidf_matrix = vectorizer.fit_transform(text)

# 3. Extract top terms
feature_names = vectorizer.get_feature_names_out()
scores = tfidf_matrix.toarray()[0]
sorted_indices = scores.argsort()[::-1]

print("Top Keyphrases:")
for idx in sorted_indices[:5]:
    print(f"- {feature_names[idx]} (Score: {scores[idx]:.4f})")
''',
    10: '''# Exp 10: SQL Database Explorer (SQL Agent)
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Connect to SQLite database
db = SQLDatabase.from_uri("sqlite:///company.db")

# 2. Set up LLM SQL agent
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
agent_executor = create_sql_agent(llm, db=db, verbose=True)

# 3. Query the database using Natural Language
response = agent_executor.run("Show the top 3 employees with highest salaries in marketing.")
print("Database Answer:", response)
''',
    11: '''# Exp 11: Web Search & Knowledge Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun

# 1. Setup search tool and LLM
search_tool = DuckDuckGoSearchRun()
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

# 2. Initialize ReAct Agent
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 3. Execute search prompt
response = agent.run("What are the latest announcements regarding NVIDIA's Blackwell GPUs?")
print("Agent Report:", response)
''',
    12: '''# Exp 12: Code Generator & Bug Fixer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# 1. Construct instruction template
prompt = PromptTemplate.from_template(
    "You are an expert compiler. Write efficient code to solve this task: {task}. "
    "Identify any bugs in user's logic and write unit tests."
)

# 2. Query code model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.1)
response = llm.invoke(prompt.format(task="Write a python function to perform binary search."))
print(response.content)
''',
    13: '''# Exp 13: Conversation Memory Playground
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Instantiate different memory components
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
buffer_memory = ConversationBufferMemory()
summary_memory = ConversationSummaryMemory(llm=llm)

# 2. Add sample interaction
buffer_memory.save_context({"input": "My name is Alex"}, {"output": "Nice to meet you, Alex!"})
summary_memory.save_context({"input": "My name is Alex"}, {"output": "Nice to meet you, Alex!"})

# 3. Inspect formats
print("Raw buffer history:", buffer_memory.load_memory_variables({}))
print("Summarized memory:", summary_memory.load_memory_variables({}))
''',
    14: '''# Exp 14: Creative Content Copywriter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

# 1. Build creative parameters prompt
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a professional copywriter. Write a persuasive {format} with an {tone} tone."),
    ("human", "Topic: {topic}")
])

# 2. Set higher temperature parameter for creativity
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.8)
chain = prompt_template | llm

# 3. Output copywriting
copy = chain.invoke({"format": "email newsletter", "tone": "energetic", "topic": "FocusFlow launch"})
print(copy.content)
''',
    15: '''# Exp 15: Image Caption Generator
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# 1. Initialize image captioning pipeline
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# 2. Process image input
raw_image = Image.open('sample_scene.jpg').convert('RGB')
inputs = processor(raw_image, return_tensors="pt")

# 3. Generate captions
out = model.generate(**inputs)
caption = processor.decode(out[0], skip_special_tokens=True)
print("Generated Caption:", caption)
''',
    16: '''# Exp 16: Visual Question Answering (VQA)
from PIL import Image
import google.generativeai as genai

# 1. Load multi-modal vision model
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Prepare visual and text query
img = Image.open('traffic_scene.jpg')
prompt = "What is the color of the car in the background and what does the sign say?"

# 3. Invoke multi-modal inference
response = model.generate_content([prompt, img])
print("VQA Answer:", response.text)
''',
    17: '''# Exp 17: Audio Transcription & Summarizer
import whisper

# 1. Load Whisper speech-recognition model
model = whisper.load_model("base")

# 2. Transcribe audio track
result = model.transcribe("meeting_recording.mp3")
raw_text = result["text"]
print("Raw Audio Transcript:\\n", raw_text)

# 3. (Optional) Run text summarizer over raw transcription output
# ...
''',
    18: '''# Exp 18: OCR & Form Data Extractor
import easyocr
import json

# 1. Initialize OCR Reader
reader = easyocr.Reader(['en'])

# 2. Run text detection
results = reader.readtext('receipt.png')

# 3. Print parsed bounding box coordinates and texts
print("OCR Detections:")
for bbox, text, prob in results:
    print(f"Detected: {text:<20} | Confidence: {prob:.4f}")
''',
    19: '''# Exp 19: RAG Triad Evaluation Lab
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevance, context_precision
from datasets import Dataset

# 1. Setup sample datasets
data_samples = {
    'question': ['How much vacation do I have?'],
    'answer': ['Employees get 15 days of PTO.'],
    'contexts': [['All employees get 15 days of PTO annually.']],
    'ground_truth': ['Employees are entitled to 15 days of PTO per year.']
}
dataset = Dataset.from_dict(data_samples)

# 2. Evaluate using Ragas
score = evaluate(dataset, metrics=[faithfulness, answer_relevance, context_precision])
print("RAG Triad Scores:")
print(score.to_pandas())
''',
    20: '''# Exp 20: Prompt Injection Defender
def validate_and_sanitize(user_input):
    # 1. Primary rule filters
    blacklisted_phrases = ["ignore all previous", "override system", "you are jailbroken"]
    for phrase in blacklisted_phrases:
        if phrase in user_input.lower():
            return False, "⚠️ Warning: Detected prompt injection signature."
            
    # 2. Perform second-stage guardrail check using a small classifier
    # ...
    return True, user_input
''',
    21: '''# Exp 21: LLM Latency & Cost Calculator
import time
import tiktoken
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. Setup latency tracker
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

t0 = time.time()
response = llm.invoke("Write a short sentence about coding.")
t1 = time.time()

# 2. Calculate statistics
elapsed = t1 - t0
input_tokens = len(encoding.encode("Write a short sentence about coding."))
output_tokens = len(encoding.encode(response.content))
estimated_cost = (input_tokens * 0.0000005) + (output_tokens * 0.0000015)

print(f"Latency: {elapsed:.2f} sec | Cost: ${estimated_cost:.7f}")
''',
    22: '''# Exp 22: Model Quantization Dashboard
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 1. Configure 4-bit Quantization (bitsandbytes)
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# 2. Load model with quantization mapping
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=quant_config,
    device_map="auto"
)
print("Quantized Model Loaded successfully onto GPU!")
'''
}

def render_sandbox_playground(exp_id, active_api_key, selected_model):
    """Renders the general dashboard and interactive simulation playground for Experiments 3-22."""
    
    # Initialize session state for custom description and objectives
    custom_desc_key = f"exp_desc_{exp_id}"
    custom_objectives_key = f"exp_objectives_{exp_id}"
    
    if custom_desc_key not in st.session_state:
        st.session_state[custom_desc_key] = ""
    if custom_objectives_key not in st.session_state:
        st.session_state[custom_objectives_key] = ""
        
    # 1. Render Header Card
    st.markdown(f"""
    <div class="exp-header-card">
        <div class="exp-meta-container">
            <span class="exp-badge status-template">Experiment Workspace</span>
        </div>
        <div class="exp-title">Exp{exp_id}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Render Custom Documentation Editor
    st.markdown("### 📝 Custom Experiment Documentation")
    st.markdown("<p style='color: #9ca3af; font-size: 0.85rem; margin-top: -10px; margin-bottom: 15px;'>Enter your custom description and learning objectives below. They will be used to simulate results.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        custom_desc = st.text_area(
            "Add Custom Description",
            value=st.session_state[custom_desc_key],
            placeholder="Explain what this experiment does in your own words...",
            height=120,
            key=custom_desc_key
        )
    with col2:
        custom_objectives_input = st.text_area(
            "Add Learning Objectives (One per line)",
            value=st.session_state[custom_objectives_key],
            placeholder="e.g.\nUnderstand key NLP concepts\nEvaluate performance metrics...",
            height=120,
            key=custom_objectives_key
        )
        
    # Parse objectives list
    objectives_list = [line.strip() for line in custom_objectives_input.split("\n") if line.strip()]
    
    # Render objectives grid if any exist
    if objectives_list:
        st.markdown("#### 🎓 Current Learning Objectives")
        st.markdown('<div class="learning-objectives-grid">', unsafe_allow_html=True)
        for idx, obj in enumerate(objectives_list):
            st.markdown(f"""
            <div class="objective-card">
                <div class="objective-number">{idx + 1}</div>
                <div class="objective-text">{obj}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Interactive Sandbox Interface
    st.markdown("### ⚙️ Interactive Laboratory Playground")
    st.markdown("<p style='color: #9ca3af; font-size: 0.85rem; margin-top: -10px; margin-bottom: 15px;'>Test input variables and simulate output results in the execution environment.</p>", unsafe_allow_html=True)
    
    with st.container():
        # Setup form input for sandbox
        user_input = st.text_area(
            "Configure Input Parameters / Text Input:",
            value="Enter sample text or parameters here...",
            height=120,
            key=f"sandbox_input_{exp_id}"
        )
        
        col_run, col_clear = st.columns([4, 1])
        with col_run:
            run_btn = st.button("🚀 Run Experiment Simulation", key=f"run_sandbox_btn_{exp_id}", use_container_width=True)
        with col_clear:
            clear_btn = st.button("🧹 Clear Logs", key=f"clear_sandbox_btn_{exp_id}", use_container_width=True)
            
        # Session state to store simulation output
        session_out_key = f"sandbox_output_history_{exp_id}"
        if session_out_key not in st.session_state or clear_btn:
            st.session_state[session_out_key] = None
            
        if run_btn:
            if not user_input.strip():
                st.error("❌ Please provide a valid input value to simulate the experiment.")
            else:
                with st.spinner("Initializing simulation environments and generating execution outputs..."):
                    # Simulation logic
                    if active_api_key:
                        try:
                            # Use Gemini to generate a highly realistic execution response
                            llm = ChatGoogleGenerativeAI(
                                model=selected_model or "gemini-1.5-flash",
                                temperature=0.3,
                                google_api_key=active_api_key
                            )
                            
                            desc_context = custom_desc if custom_desc.strip() else "A custom user-defined laboratory experiment."
                            objectives_context = ", ".join(objectives_list) if objectives_list else "None provided."
                            
                            system_prompt = (
                                f"You are simulating the execution of a college laboratory experiment: 'Exp{exp_id}'.\n"
                                f"Description: {desc_context}\n"
                                f"Learning Objectives: {objectives_context}\n\n"
                                "The student user has run this experiment sandbox with the following input parameters/text:\n"
                                f"\"\"\"\n{user_input}\n\"\"\"\n\n"
                                "Your goal is to output a realistic experiment report in the following structured format:\n"
                                "1. EXECUTION LOGS: A short mock console log showing imports, device allocations (CPU/GPU/TPU), model loading steps, inference metrics, and execution time (ms).\n"
                                "2. RESULTS AND METRICS: The final mock result formatted beautifully (e.g. classification tables, extracted keywords, similarity heatmap matrices, generated code, or OCR json tables).\n"
                                "3. ACADEMIC ANALYSIS: A brief, professional explanation of the result, what underlying NLP/AI mechanisms were triggered, and a key observation.\n\n"
                                "Make the output look extremely premium and academic. Use rich markdown tables, emojis, and styling grids."
                            )
                            
                            sim_response = llm.invoke(system_prompt).content
                            st.session_state[session_out_key] = sim_response
                        except Exception as e:
                            st.error(f"❌ Error invoking AI simulation: {str(e)}")
                            # Set fallback mock response
                            st.session_state[session_out_key] = generate_fallback_mock(exp_id, user_input)
                    else:
                        # Fallback mock response when API key is missing
                        st.info("ℹ️ Gemini API key is missing. Displaying simulated local mock response. Enter your API key in the sidebar for live model simulations.")
                        time.sleep(1.5)  # Simulate execution lag
                        st.session_state[session_out_key] = generate_fallback_mock(exp_id, user_input)
                        
        # Display output results if available
        if st.session_state[session_out_key]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style='background-color: rgba(99, 102, 241, 0.05); padding: 16px 20px; border-radius: 12px; border: 1px solid rgba(99,102,241,0.15); margin-bottom: 20px;'>
                <h4 style='margin: 0; color: #a5b4fc; font-size: 1.05rem;'>💻 Simulation Output Console</h4>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state[session_out_key])
            
    # 4. Source Code Implementation Guide Accordion
    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
    with st.expander("📄 Core Code Implementation Guide", expanded=False):
        st.markdown(f"""
        <p style='color: #9ca3af; font-size: 0.85rem; line-height: 1.4;'>
            To write this laboratory experiment in your codebase, you can adapt the python snippet below. 
            It outlines the package dependencies, initialization steps, and execution pipelines.
        </p>
        """, unsafe_allow_html=True)
        
        template_code = CODE_TEMPLATES.get(exp_id, "# Code template coming soon...")
        st.code(template_code, language="python")


def generate_fallback_mock(exp_id, user_input):
    """Generates realistic offline mock reports for each experiment when API key is not provided."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    logs = f"""### 💻 Execution Logs (`{timestamp}`)
```
[INFO] Importing required ML packages...
[INFO] Scanning CPU cores: 8 cores detected. Allocating system threads.
[INFO] Model loaded successfully in memory.
[INFO] Running evaluation pipeline on user parameters.
[INFO] Inference completed in 143ms. Memory usage delta: +12.4 MB.
```
"""
    
    if exp_id == 5: # Text Similarity
        return logs + """
### 📊 Results and Metrics
| Metric | Sentence Comparison | Cosine Similarity Score |
| :--- | :--- | :--- |
| **Cosine Similarity** | Sentence A ↔ Sentence B | **0.8432 (High Correlation)** |
| **Euclidean Distance** | Sentence A ↔ Sentence B | **0.3129** |

### 📚 Academic Analysis
The embedding vectors were generated using a Sentence-Transformer model. The resulting cosine similarity of `0.8432` signifies that although the sentence phrasing and vocabulary differ slightly (e.g. "jumps" vs "leaps", "dog" vs "hound"), the contextual meaning remains extremely close.
"""
    elif exp_id == 7: # Sentiment
        return logs + f"""
### 📊 Results and Metrics
**Analyzed Text:** `"{user_input[:80]}..."`

| Sentiment Class | Confidence Score | Visual Distribution |
| :--- | :--- | :--- |
| **POSITIVE** | **89.4%** | `██████████████████░░` |
| **NEUTRAL** | **8.1%** | `█░░░░░░░░░░░░░░░░░░░` |
| **NEGATIVE** | **2.5%** | `░░░░░░░░░░░░░░░░░░░░` |

### 📚 Academic Analysis
The Transformer-based classification classifier detected a highly positive polarity driven primarily by strong emotional tokens (such as "love", "smooth", "responsive"). The negative weight was slightly stimulated by the token "bug", but it was heavily outweighed by the positive sentiment terms.
"""
    else:
        # Generic fallback mock template
        return logs + f"""
### 📊 Results and Metrics
**Simulated Input Parameters:** `"{user_input[:100]}"`

| Parameter | Type | Status |
| :--- | :--- | :--- |
| **Inference Mode** | Offline Simulation | SUCCESS |
| **Resource State** | Idle | READY |

#### Simulated Output Payload:
```json
{{
  "experiment_id": {exp_id},
  "status": "COMPLETED",
  "data_processed": true,
  "simulated_timestamp": "{timestamp}",
  "simulated_output": "Dynamic playground output generated for parameter value: {user_input[:40]}"
}}
```

### 📚 Academic Analysis
The experiment successfully completed its offline local test-suite path. The input parameters were successfully mapped to our mockup execution registry. If you configure your **Google Gemini API Key** in the settings sidebar, this playground will execute live neural queries on Google's cloud server endpoints.
"""
