# UsmleGPT: An AI Application for Developing MCQs via Multi-agent System

## Overview

Driven by the trending multi-agent system (MAS) that harnesses collective intelligence from numerous large language models (LLMs), **UsmleGPT** is a Python-based application designed to elevate the quality of LLM-generated multiple-choice questions (MCQs) tailored for the USMLE Step 1 scenario. Specifically, the MAS aligns with the NBME‘s framework and procedures, recognized as the gold standard in medical test development, incorporating advanced prompt strategies to guide each LLM, or agent, through their respective tasks and specialties. This enables UsmleGPT to surpass conventional practices in automating item generation.

---

## Requirements

To use the USMLE MCQ Development System, ensure the following:

- **Python 3.8 or higher**
- Required Python packages:
  ```bash
  pip install gradio openai pandas regex
  ```
- **API Key**: Valid API key(s) for accessing LLM services (Supports both OpenAI’s official endpoints and compatible API providers).
- **Internet Access**: Required for API communications and model interactions.

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/FantaStiC898/UsmleGPT.git
   cd UsmleGPT
   ```

2. **Install Dependencies**:
   ```bash
   pip install gradio openai pandas regex
   ```

3. **(*Optional*) Configure administrator mode**:
   - Open `UsmleGPT.py` and modify the `handle_admin_mode` function to set a custom password:
     ```python
     def handle_admin_mode(password):
         if password == "your_custom_password_here":  # Change this line
             return [["your_api_key", "https://api.openai.com/v1", "your_model_name"]]
     ```

4. **Run the application**:
   ```bash
   python UsmleGPT.py
   ```

5. **Access the interface**:
   - Open your browser and navigate to `http://localhost:1210`
   - (*Optional*) Enter your administrator password to configure API keys and models

---

## Code Structure

### Key Modules

1. **`AIModel` Class**
   - **Purpose**: Handles model initialization and API configurations
   - **Key Methods**:
     - `__init__(self, model_name, api_key, base_url=None)`: Initializes model with API configurations

2. **`MCQDevelopmentSystem` Class**
   - **Purpose**: Multi-Agent refinement workflow (Writer → 3 Reviewers → Editor → Writer → Editor)
   - **Key Methods**:
     - `select_model(self, role, specified_model=None)`: Assigns models to roles
     - `call_ai_model(self, model, system_prompt, user_prompt)`: Handles API calls (Error handling with retry mechanisms, 5 attempts per API call)
     - `add_to_history(self, role, content, version)`: Maintains development history
     - `get_history_as_text(self)`: Formats the history entries as a text string with each entry‘s timestamp, role, version, and content

3. **Processing Functions**
   - `process_mcq()`: Main workflow controller
   - `generate_mcq_json_summary()`: Creates version comparison JSON
   - `generate_html_report()`: Produces visual timeline HTML
   - `extract_json_content()`: Regex-based JSON extraction

4. **Gradio Interface**
   - `create_interface()`: Builds web UI with:
     - Model configuration inputs
     - Development process controls
     - Output visualization components

### Key Features
- Multi-agent collaboration with role-specific prompts
- Configurable model assignments per task (Writer/Reviewer/Editor/Summarizer)
- Development history visualization (HTML timeline)
- Version comparison through structured JSON outputs
- Administrator mode for model configuration management

---


## User Guide

### Step 1: Configure Large Language Models
1. **Access the System**: You can choose either of the following methods to access the system:
   - **Local Deployment**:
     ```bash
     python UsmleGPT.py
     ```
     - Automatically kills processes on port 1210 before launching
     - Access via `http://localhost:1210`
   - **Web Access**: Visit [https://ibfarktknlia.sealoshzh.site/](https://ibfarktknlia.sealoshzh.site/)

2. **API Key and Model Configuration**:
   - Enter administrator password (default: "password" - change in code for production)
   - Configure models with:
     - Valid API keys
     - Base URLs (supports OpenAI-compatible endpoints)
     - Model identifiers (e.g., "gpt-4-turbo")

### Step 2: Assign Models to Roles
- **Manual Assignment**: Use dropdowns to select models for:
  - Writer
  - Reviewer
  - Editor
  - Summarizer
- **Automatic Assignment**: Click **"Shuffle Models"** for random role allocation

### Step 3: Select Question Attributes
- **Discipline**: Choose from options like Behavioral Sciences, Pharmacology, Biochemistry & Nutrition, etc.
- **System**: Specify the physiological system (e.g., Cardiovascular System, Respiratory & Renal/Urinary Systems).
- **Competency**: Define the competency being tested (e.g., Patient Care: Diagnosis, Communication and Interpersonal Skills).
- **Keywords**: Add optional keywords for specific content requests.

### Step 4: Initiate the Development Process
- Click the **“Start MCQ Development Process”** button to begin.
- Monitor the development process through the **“Development Process History”** section.
- The system will generate a draft question, which undergoes multiple stages of refinement.

### Step 5: Export and Finalize Outputs
- **Export Development History**: Download the development history as an **HTML report** or **JSON file**.
- **Submit Final Versions**: Summarize the initial and final versions of the MCQs for further use or revision.

---

## Data Structures

### Development History Entry
```python
{
    "timestamp": str(datetime.datetime.now()),
    "role": "Item Writer",  # or "Reviewer 1", "Editorial Staff", etc.
    "content": "Generated question text...",
    "version": 1  # Increments with each modification
}
```

### JSON Summary Format
```json
{
    "draft": {
        "version": "draft",
        "question": "Full question stem...",
        "options": ["A) Option 1", "B) Option 2", ...],
        "correct_answer": "A"
    },
    "final": {
        "version": "final",
        "question": "Revised question stem...",
        "options": ["A) Modified option 1", "B) Modified option 2", ...],
        "correct_answer": "B"
    }
}
```

---

## Security & Privacy

- **API Key Management**: Keys are never stored - only held in memory during session
- **Session Isolation**: No persistent user data storage

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 1210 conflicts | Manually terminate existing processes: `kill -9 $(lsof -t -i:1210)` |
| API errors | Verify base URLs and API keys in admin mode |
| JSON parsing failures | Check model outputs for valid JSON syntax using extract_json_content() |
| Gradio UI freeze | Ensure all model configurations are valid before starting process |

---

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you encounter any issues or have questions, please feel free to contact us.
