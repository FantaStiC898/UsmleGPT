# UsmleGPT: An AI Application for Developing MCQs via Multi-agent System

## Overview

Driven by the trending multi-agent system (MAS) that harnesses collective intelligence from numerous large language models (LLMs), **UsmleGPT** is a Python-based application designed to elevate the quality of LLM-generated multiple-choice questions (MCQs) tailored for the USMLE Step 1 scenario. Specifically, the MAS aligns with the NBME's framework and procedures, recognized as the gold standard in medical test development, incorporating advanced prompt strategies to guide each LLM, or agent, through their respective tasks and specialties. This enables UsmleGPT to surpass conventional practices in automating item generation.

---

## Requirements

To use the USMLE MCQ Development System, ensure the following:

- **Python 3.8 or higher**
- Required Python packages:
  ```bash
  pip install gradio openai pandas
- **OpenAI API Key**: A valid API key is required to integrate with OpenAI models.
- **Internet Access**: The system requires internet access to interact with the OpenAI API.

---

## User Guide

### Step 1: Configure Language Models
1. **Access the System**: You can choose either of the following methods to access the system:
   - **Self-Hosting**: Deploy the system locally by cloning the repository and running the application.
   - **Access via Website**: Visit the interface at [https://ibfarktknlia.sealoshzh.site/](https://ibfarktknlia.sealoshzh.site/).
3. **API Key and Model Configuration**:
   - Enter the API key and base URL for each language model.
   - Configure multiple models to handle different tasks (e.g., writing, reviewing, editing).
   - **Privacy Statement**: Your API keys and sensitive data are kept secure and confidential.

### Step 2: Assign Models to Roles
- Use the drop-down menus to assign models to specific roles (e.g., Writer, Reviewer, Editor).
- Alternatively, use the **“Shuffle Models”** button to randomly assign models.

### Step 3: Select Question Attributes
- **Discipline**: Choose from options like Behavioral Sciences, Pharmacology, Biochemistry & Nutrition, etc.
- **System**: Specify the organ system (e.g., Cardiovascular System, Respiratory & Renal/Urinary Systems).
- **Competency**: Define the competency being tested (e.g., Patient Care: Diagnosis, Communication and Interpersonal Skills).
- **Keywords**: Add optional keywords for further customization.

### Step 4: Initiate the Development Process
- Click the **“Start MCQ Development Process”** button to begin.
- Monitor the development process through the **“Development Process History”** section.
- The system will generate a draft question, which undergoes multiple stages of refinement.

### Step 5: Export and Finalize Outputs
- **Export Development History**: Download the development history as an **HTML report** or **JSON file**.
- **Submit Final Versions**: Summarize the initial and final versions of the MCQs for further use or revision.

---

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you encounter any issues or have questions, please feel free to contact us.

---

### Troubleshooting and Tips
- **API Connectivity**: Ensure API keys and base URLs are correctly entered.
- **Model Assignment**: Use the shuffle function for quick model assignment but review manually for critical tasks.
- **Keywords**: Use the keywords field to introduce specific constraints or guide the question generation process.
- **Data Safety**: Regularly save development history to avoid data loss during prolonged sessions.


