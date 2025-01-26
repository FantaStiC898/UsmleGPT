import json
import gradio as gr
import random
from openai import OpenAI
import datetime
import time
import os
import re

def extract_json_content(json_str):
    """
    Extracts the JSON content from a string by finding the outermost {} pair.
    """
    try:
        # Find the first { and the last }
        match = re.search(r'\{.*\}', json_str, re.DOTALL)
        if match:
            # Return the content within the outermost {}
            return match.group(0)
        else:
            return None
    except Exception as e:
        print(f"Error extracting JSON content: {e}")
        return None

# Predefined options
discipline_options = [
    "Behavioral Sciences", "Pharmacology", "Biochemistry & Nutrition",
    "Immunology", "Genetics", "Histology & Cell Biology", "Pathology",
    "Gross Anatomy & Embryology", "Microbiology", "Physiology"
]

system_options = [
    "Reproductive & Endocrine Systems",
    "Social Sciences: Communication and Interpersonal Skills",
    "Human Development", "Cardiovascular System",
    "Respiratory & Renal/Urinary Systems",
    "Gastrointestinal System",
    "Behavioral Health & Nervous Systems/Special Senses",
    "Musculoskeletal, Skin & Subcutaneous Tissue",
    "Biostatistics & Epidemiology/Population Health",
    "Blood & Lymphoreticular/Immune Systems",
    "Multisystem Processes & Disorders"
]

competency_options = [
    "Patient Care: Diagnosis",
    "Practice–based Learning & Improvement",
    "Communication and Interpersonal Skills",
    "Medical Knowledge: Applying Foundational Science Concepts"
]

class AIModel:
    def __init__(self, model_name, api_key, base_url=None):
        if not api_key:
            raise ValueError("API key cannot be empty")
        if not model_name:
            raise ValueError("Model name cannot be empty")
            
        self.model_name = model_name
        try:
            if base_url:
                self.client = OpenAI(api_key=api_key, base_url=base_url)
            else:
                self.client = OpenAI(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")

class MCQDevelopmentSystem:
    def __init__(self, models_config):
        if not models_config:
            raise ValueError("Models configuration cannot be empty")
            
        self.models = []
        for config in models_config:
            try:
                if not config.get('api_key') or not config.get('model_name'):
                    continue
                self.models.append(AIModel(**config))
            except Exception as e:
                print(f"Failed to initialize model: {str(e)}")
                
        if not self.models:
            raise ValueError("No valid models could be initialized")
            
        self.history = []

    def select_model(self, role, specified_model=None):
        if not self.models:
            raise ValueError("No models configured")
            
        if specified_model:
            selected_model = next(
                (m for m in self.models if m.model_name == specified_model),
                None
            )
            if selected_model:
                return selected_model
                
        return random.choice(self.models)

    def call_ai_model(self, model, system_prompt, user_prompt):
        max_attempts = 5
        delay_seconds = 2
        
        for attempt in range(max_attempts):
            try:
                if not model or not model.client:
                    raise ValueError("Invalid model configuration")

                response = model.client.chat.completions.create(
                    model=model.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                if not response or not response.choices:
                    raise ValueError("Empty response from API")
                    
                return response.choices[0].message.content

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_attempts - 1:
                    time.sleep(delay_seconds)
                else:
                    return f"Error: Unable to get response after {max_attempts} attempts"

    def add_to_history(self, role, content, version):
        entry = {
            "timestamp": str(datetime.datetime.now()),
            "role": role,
            "content": content,
            "version": version
        }
        self.history.append(entry)
        return self.history

    def get_history(self):
        return self.history

    def get_history_as_text(self):
        if not self.history:
            return "No history available."

        text_history = []
        for entry in self.history:
            text_history.append(
                f"[{entry['timestamp']}] {entry['role']} (Version {entry['version']}):\n"
                f"{entry['content']}\n"
            )
        return "\n".join(text_history)


EXAMPLE_ITEMS = """
<example#1> A 27-year-old woman comes to the office for counseling prior to conception. She states that a friend recently delivered a newborn with a neural tube defect and she wants to decrease her risk for having a child with this condition. She has no history of major medical illness and takes no medications. Physical examination shows no abnormalities. It is most appropriate to recommend that this patient begin supplementation with a vitamin that is a cofactor in which of the following processes? (A) Biosynthesis of nucleotides (B) Protein gamma glutamate carboxylation (C) Scavenging of free radicals (D) Transketolation (E) Triglyceride lipolysis Correct Answer: A </example1>

<example#2> A 26-year-old woman comes to the physician with her husband for counseling prior to conception. Her mother and three of her five siblings have type 2 diabetes mellitus. She is 170 cm (5 ft 7 in) tall and weighs 82 kg (180 lb); BMI is 28 kg/m2. Her blood pressure is 148/84 mm Hg. Physical examination shows no other abnormalities. Her fasting serum glucose concentration is 110 mg/dL. Which of the following is the most appropriate initial statement by the physician?

(A) "Let's review ways you can optimize your own health before conceiving." (B) "We should test you for islet cell antibodies before you try to conceive." (C) "You can conceive right away since you are in good health." (D) "You should avoid gaining weight during pregnancy because you are already overweight and at risk for type 2 diabetes mellitus." (E) "You should have no problems with your pregnancy if you start insulin therapy." Correct Answer: A </example#2>

<example#3> {Patient Information: {Age: 6 years Gender: M, Race/Ethnicity: unspecified, Site of Care: office} } The patient is brought by his mother because of a 1-month history of bleeding gums after brushing his teeth, increasingly severe muscle and joint pain, fatigue, and easy bruising. His mother says he has lost six baby teeth and has been irritable during this time. Use of acetaminophen has provided minimal relief of his pain. He has autism spectrum disorder. He is not toilet-trained. He has a 10-word vocabulary. Vital signs and oxygen saturation on room air are within normal limits. The patient appears alert but does not speak or make eye contact. Skin is pale and coarse. Examination of the scalp shows erythematous hair follicles. Dentition is poor, and gingivae bleed easily to touch. Multiple ecchymoses and petechiae are noted over the trunk and all extremities. There is marked swelling and tenderness to palpation of the elbow, wrist, knee, and ankle joints. He moves all extremities in a limited, guarded manner. Deep tendon reflexes are absent throughout. It is most appropriate to obtain specific additional history regarding which of the following in this patient? (A) Diet (B) Evidence of pica (C) Herbal supplementations (D) Lead exposure (E) Self-injurious behaviors Correct Answer: A </example#3>
"""

def process_mcq(models_config, disciplines, systems, competencies, keywords, writer_model, reviewer_models, editor_model, summarizer_model):
    try:
        # Convert the DataFrame to a list of dictionaries
        models_config = models_config.to_dict(orient='records')
        mcq_system = MCQDevelopmentSystem(models_config)

        # Handle empty or None values for model selection
        writer_model = writer_model if writer_model else None
        reviewer_models = reviewer_models if reviewer_models else [None] * 3
        editor_model = editor_model if editor_model else None

        # Initial item writer prompt
        writer_system_prompt = """You are an experienced USMLE item writer. Create a high-quality MCQ item following USMLE guidelines."""

        writer_prompt = f"""Study these example items carefully:
{EXAMPLE_ITEMS}

Now, create a similar multiple choice question for:
Disciplines: {disciplines}
Systems: {systems}
Competencies: {competencies}
Additional elements incoporated into the MCQ: {keywords}

Follow the same format as the examples."""

        # Select model and generate initial draft
        writer_ai = mcq_system.select_model("writer", writer_model)
        initial_draft = mcq_system.call_ai_model(writer_ai, writer_system_prompt, writer_prompt)
        mcq_system.add_to_history("Item Writer", initial_draft, 1)

        # Reviewer prompts
        reviewer_prompts = [
            "As a medical expert serving as a reviewer for USMLE item development, please reviews the item. You are expected to see that if it conforms to the requested USMLE style and to ensure no information is missing. You also edit and annotate items for clarity, grammar and punctuation, uniformity of style and technical item flaws – particularly those that might otherwise benefit test-wise examinees or add irrelevant difficulty.  Please note that, if there is a clinical setting, most items are in the form of a patient vignette in which the first sentence provides the patient age, gender, site of care, presenting complaint and its duration. Subsequent sentences in the vignette provide additional patient history, physical findings, the results of diagnostic studies and/or response to initial treatment. Also, do focus more on scientific accuracy and clinical relevance.",
            "As a medical expert serving as a reviewer for USMLE item development, please reviews the item. You are expected to see that if it conforms to the requested USMLE style and to ensure no information is missing. You also edit and annotate items for clarity, grammar and punctuation, uniformity of style and technical item flaws – particularly those that might otherwise benefit test-wise examinees or add irrelevant difficulty.  Please note that, if there is a clinical setting, most items are in the form of a patient vignette in which the first sentence provides the patient age, gender, site of care, presenting complaint and its duration. Subsequent sentences in the vignette provide additional patient history, physical findings, the results of diagnostic studies and/or response to initial treatment. Also, do focus more on psychometric expert focusing on item construction and option quality.",
            "As a medical expert serving as a reviewer for USMLE item development, please reviews the item. You are expected to see that if it conforms to the requested USMLE style and to ensure no information is missing. You also edit and annotate items for clarity, grammar and punctuation, uniformity of style and technical item flaws – particularly those that might otherwise benefit test-wise examinees or add irrelevant difficulty.  Please note that, if there is a clinical setting, most items are in the form of a patient vignette in which the first sentence provides the patient age, gender, site of care, presenting complaint and its duration. Subsequent sentences in the vignette provide additional patient history, physical findings, the results of diagnostic studies and/or response to initial treatment. Also, do focus more on clarity, formatting, and style guidelines."
        ]

        # Get reviews using specified or random models
        reviews = []
        for i, prompt in enumerate(reviewer_prompts):
            reviewer_model = mcq_system.select_model("reviewer",
                reviewer_models[i] if i < len(reviewer_models) else None)
            review = mcq_system.call_ai_model(reviewer_model,
                "You are an experienced USMLE item reviewer.",
                f"{prompt}\n\nHistory:\n{mcq_system.get_history_as_text()}")
            reviews.append(review)
            mcq_system.add_to_history(f"Reviewer {i+1}", review, i+2)

        # Editorial staff synthesis
        editor_ai = mcq_system.select_model("editor", editor_model)
        editor_prompt = f"""Synthesize all reviews and provide a comprehensive summary for the item writer.

History:
{mcq_system.get_history_as_text()}"""

        editorial_summary = mcq_system.call_ai_model(editor_ai,
            "You are the editorial coordinator.",
            editor_prompt)
        mcq_system.add_to_history("Editorial Staff", editorial_summary, 5)

        # Author revision
        revision_prompt = f"""Now you are the author reviewing the item draft you developed as well as the comments/suggestions from three NBME editorial staff members. 

Please carefully review materials provided, respond to queries from the staff editor, verify the correct answer and classification codes, and confirm the appearance of any associated pictorials. Any disagreements about phrasing should be documented so that they can be presented to the editorial staff again.

Provide your revised version of the item and explain your responses to the feedback.

History:
{mcq_system.get_history_as_text()}"""

        revision = mcq_system.call_ai_model(writer_ai,
            "You are the original item writer reviewing feedback.",
            revision_prompt)
        mcq_system.add_to_history("Author Revision", revision, 6)

        # Final editorial decision
        final_decision_prompt = f"""As the editorial staff, make the final decision on this item.
Review the entire development process and either:
1. Accept the item as is
2. Request further revisions
3. Reject the item

History:
{mcq_system.get_history_as_text()}"""

        final_decision = mcq_system.call_ai_model(editor_ai,
            "You are the editorial coordinator making the final decision.",
            final_decision_prompt)
        mcq_system.add_to_history("Final Editorial Decision", final_decision, 7)

        return mcq_system.history

    except Exception as e:
        print(f"Error in process_mcq: {str(e)}")
        return [{"error": str(e)}]

def generate_mcq_json_summary(history):
    """ Generate a JSON summary of initial and final MCQ versions """
    if not history:
        return None

    try:
        # Find initial draft (first item writer entry)
        initial_version = next((entry for entry in history if entry['role'] == "Item Writer"), None)

        # Find final version (last substantive revision before final decision)
        final_version = next((entry for entry in reversed(history) 
                            if entry['role'] in ["Author Revision", "Editorial Staff"] 
                            and entry['role'] != "Final Editorial Decision"), None)

        if not initial_version or not final_version:
            return None

        summary = {
            "draft": {
                "version": "draft",
                "question": initial_version['content'],
                "options": [],  # These would need to be extracted from the content
                "correct_answer": ""  # This would need to be extracted from the content
            },
            "final": {
                "version": "final",
                "question": final_version['content'],
                "options": [],  # These would need to be extracted from the content
                "correct_answer": ""  # This would need to be extracted from the content
            }
        }

        return json.dumps(summary, indent=2)
    except Exception as e:
        print(f"Error in generate_mcq_json_summary: {str(e)}")
        return None

def generate_html_report(history):
    """ Convert the development history into a formatted HTML document """
    try:
        html_content = """
        <html>
        <head>
        <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .entry { margin-bottom: 30px; border-bottom: 1px solid #ccc; padding-bottom: 20px; }
        .timestamp { color: #666; font-size: 0.9em; }
        .role { font-weight: bold; color: #2c5282; }
        .version { color: #718096; }
        .content { margin-top: 10px; white-space: pre-wrap; }
        .header { background-color: #f7fafc; padding: 20px; margin-bottom: 30px; }
        </style>
        </head>
        <body>
        <div class="header">
            <h1>USMLE MCQ Development Process Record</h1>
            <p>Generated on: """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        </div>
        """

        for entry in history:
            html_content += f"""
            <div class="entry">
                <div class="timestamp">{entry['timestamp']}</div>
                <div class="role">
                    <span class="role">{entry['role']}</span>
                    <span class="version">(Version {entry['version']})</span>
                </div>
                <div class="content">{entry['content']}</div>
            </div>
            """

        html_content += """
        </body>
        </html>
        """
        
        # Save HTML file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mcq_development_history_{timestamp}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        return filename
    except Exception as e:
        print(f"Error in generate_html_report: {str(e)}")
        return None

def update_model_choices(df):
    try:
        if df is None or len(df) == 0:
            return [], [], [], []

        models = [row['model_name'] for row in df.to_dict(orient='records') if row['model_name']]
        return (
            gr.Dropdown.update(choices=models),
            gr.Dropdown.update(choices=models),
            gr.Dropdown.update(choices=models),
            gr.Dropdown.update(choices=models)
        )
    except Exception as e:
        print(f"Error in update_model_choices: {str(e)}")
        return [], [], [], []

def shuffle_models(df):
    try:
        if df is None or len(df) == 0:
            return None, None, None, None

        models = [row['model_name'] for row in df.to_dict(orient='records') if row['model_name']]
        if not models:
            return None, None, None, None

        return (
            random.choice(models),
            random.choice(models),
            random.choice(models),
            random.choice(models)
        )
    except Exception as e:
        print(f"Error in shuffle_models: {str(e)}")
        return None, None, None, None

def save_json_to_file(json_content):
    if not json_content:
        return None

    try:
        # Save JSON content to a file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mcq_versions_summary_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(json_content)

        print(f"JSON summary saved to {filename}")
        return filename
    except Exception as e:
        print(f"Error saving JSON to file: {e}")
        return None

def save_json_summary(history, models_config, summarizer_model):
    if not history:
        print("No history available.")
        return None

    try:
        # Initialize MCQ system
        mcq_system = MCQDevelopmentSystem(models_config.to_dict(orient='records'))
        summarizer_ai = mcq_system.select_model("summarizer", summarizer_model)

        # Convert history to text format
        history_text = ""
        for entry in history:
            history_text += f"[{entry['timestamp']}] {entry['role']} (Version {entry['version']}):\n{entry['content']}\n\n"

        # Create summarizer prompt
        summarizer_prompt = f"""Please see the entire history of an item's development, and extract information of the first draft and finalized version of the item that one can track the differences in between. Please following the following json format:
        {{
            "draft": {{
                "version": "draft",
                "question": "[full question stem]",
                "options": ["A) [option text]", "B) [option text]", "C) [option text]", "D) [option text]", "E) [option text]"],
                "correct_answer": "[letter A-E]"
            }},
            "final": {{
                "version": "final",
                "question": "[full question stem]",
                "options": ["A) [option text]", "B) [option text]", "C) [option text]", "D) [option text]", "E) [option text]"],
                "correct_answer": "[letter A-E]"
            }}
        }}

        Here is the complete development history:

        {history_text}"""

        # Print the summarizer prompt to the console for debugging
        print("Summarizer Prompt:")
        print(summarizer_prompt)

        # Get JSON summary from AI
        json_str = mcq_system.call_ai_model(
            summarizer_ai,
            "You are a technical summarizer. Extract the first and final versions of the MCQ from the history and output valid JSON only.",
            summarizer_prompt
        )

        # Print the raw JSON response for debugging
        print("Raw JSON Response:")
        print(json_str)

        # Extract the JSON content from the response
        json_content = extract_json_content(json_str)
        if not json_content:
            print("Failed to extract JSON content.")
            return None

        # Return the extracted JSON content as-is
        return json_content

    except Exception as e:
        print(f"Error in save_json_summary: {e}")
        return None

def process_json_summary(history, config, model):
    json_result = save_json_summary(history, config, model)
    return (
        json_result,  # JSON result
        "JSON generation completed, ready for download" if json_result else "Generation failed, please try again",  # Status message
        gr.Button.update(visible=True, interactive=True),  # Download button state
        gr.Button.update(interactive=True)  # Generate button state
    )

def create_interface():
    with gr.Blocks() as app:
        gr.Markdown("# USMLE MCQ Development System")

        # Administrator Mode Textbox
        admin_mode = gr.Textbox(
            label="Administrator Mode",
            placeholder="Enter password to enable administrator mode",
            lines=1,
            visible=True
        )

        # Function to handle administrator mode
        def handle_admin_mode(password):
            if password == "password":  #example
                return [
                    ["sk-abc123def456ghi789", "https://api.openai.com/v1", "model-alpha"],
                    ["sk-abc123def456ghi789", "https://api.openai.com/v1", "model-beta"],
                    ["sk-abc123def456ghi789", "https://api.openai.com/v1", "model-gamma"],
                    ["sk-abc123def456ghi789", "https://api.openai.com/v1", "model-delta"]
                ]
            else:
                return [["", "", ""]]

        # AI Models Configuration
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Openai API modules are available")
                models_config = gr.Dataframe(
                    headers=["api_key", "base_url", "model_name"],
                    datatype=["str", "str", "str"],
                    label="AI Models Configuration",
                    value=[["", "", ""]]
                )

        # Update models_config when admin_mode changes
        admin_mode.change(
            fn=handle_admin_mode,
            inputs=[admin_mode],
            outputs=[models_config]
        )

        with gr.Row():
            with gr.Column():
                writer_model = gr.Dropdown(
                    label="Specific Model for Writer",
                    choices=[],
                    value=None,
                    allow_custom_value=True
                )
                reviewer_models = gr.Dropdown(
                    label="Specific Models for Reviewers",
                    choices=[],
                    multiselect=True,
                    value=None,
                    allow_custom_value=True
                )
                editor_model = gr.Dropdown(
                    label="Specific Model for Editor",
                    choices=[],
                    value=None,
                    allow_custom_value=True
                )
                summarizer_model = gr.Dropdown(
                    label="Specific Model for Version Summarizer",
                    choices=[],
                    value=None,
                    allow_custom_value=True
                )

        with gr.Row():
            disciplines = gr.Dropdown(
                label="Disciplines",
                choices=discipline_options,
                multiselect=True
            )
            systems = gr.Dropdown(
                label="Systems",
                choices=system_options,
                multiselect=True
            )
            competencies = gr.Dropdown(
                label="Competencies",
                choices=competency_options,
                multiselect=True
            )
            keywords = gr.Textbox(label="Keywords")

        with gr.Row():
            submit_btn = gr.Button("Start MCQ Development Process")
            shuffle_btn = gr.Button("Shuffle Models")

        output = gr.JSON(label="Development Process History")
        json_summary_result = gr.Textbox(label="JSON Summary Result", visible=False)
        download_btn = gr.Button("Download Development History as HTML")
        
        with gr.Row():
            json_summary_btn = gr.Button("Generate JSON Summary", size="sm")
            download_json_btn = gr.Button("Download JSON Summary", size="sm", visible=False)
            status_text = gr.Text(label="Status", value="", visible=True)  # Add status text

        # Event handlers
        models_config.change(
            fn=update_model_choices,
            inputs=[models_config],
            outputs=[writer_model, reviewer_models, editor_model, summarizer_model]
        )

        shuffle_btn.click(
            fn=shuffle_models,
            inputs=[models_config],
            outputs=[writer_model, reviewer_models, editor_model, summarizer_model]
        )

        submit_btn.click(
            fn=process_mcq,
            inputs=[
                models_config,
                disciplines,
                systems,
                competencies,
                keywords,
                writer_model,
                reviewer_models,
                editor_model,
                summarizer_model
            ],
            outputs=[output]
        )

        download_btn.click(
            fn=generate_html_report,
            inputs=[output],
            outputs=[gr.File(label="Download HTML Report")]
        )

        # Display JSON summary in the UI
        json_summary_btn.click(
            fn=lambda: (None, "Generating JSON...", gr.Button.update(visible=False), gr.Button.update(interactive=False)),
            outputs=[json_summary_result, status_text, download_json_btn, json_summary_btn]
        ).then(
            fn=process_json_summary,
            inputs=[output, models_config, summarizer_model],
            outputs=[json_summary_result, status_text, download_json_btn, json_summary_btn]
        )

        # Download JSON summary as a file
        download_json_btn.click(
            fn=lambda json_content: save_json_to_file(json_content),
            inputs=[json_summary_result],
            outputs=[gr.File(label="Download JSON File")]
        )

    return app

if __name__ == "__main__":
    # Terminate the process occupying port 1210 before starting
    os.system("kill -9 $(lsof -t -i:1210)")
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=1210, show_error=True)