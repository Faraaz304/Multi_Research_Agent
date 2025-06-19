# app_gradio.py

import gradio as gr
from dotenv import load_dotenv

# --- Import your existing workflow ---
from src.workflow import Workflow

# Load environment variables and initialize the workflow once
load_dotenv()
print("Initializing Agent Workflow...")
workflow = Workflow()
print("Workflow Initialized.")

def format_results_as_markdown(results):
    """
    Takes the final ResearchState object and formats it into a single
    Markdown string for display in Gradio.
    """
    if not results:
        return "No results to display."

    # --- Start building the Markdown output ---
    markdown_output = f"# 📊 Research Results for: {results.query}\n"

    # 1. AI Recommendation Section
    if results.analysis:
        markdown_output += "## 💡 AI Recommendation\n"
        markdown_output += f"> {results.analysis.replace('.', '. ')}\n\n" # Blockquote style
    
    # 2. Detailed Tool Analysis Section
    if results.companies:
        markdown_output += "## 🏢 Detailed Tool Analysis\n"
        markdown_output += "---\n"

        for i, company in enumerate(results.companies, 1):
            markdown_output += f"### {i}. {company.name}\n"
            
            if company.website:
                markdown_output += f"**🌐 Website:** [{company.website}]({company.website})\n"

            if company.description and company.description != "Failed":
                markdown_output += f"**📝 Description:** {company.description}\n"
            
            markdown_output += f"**💰 Pricing:** `{company.pricing_model}`\n"
            
            os_status = "Yes" if company.is_open_source else "No" if company.is_open_source is not None else "Unknown"
            markdown_output += f"**📖 Open Source:** `{os_status}`\n"

            api_status = "✅ Yes" if company.api_available else "❌ No" if company.api_available is not None else "❓ Unknown"
            markdown_output += f"**🔌 API Available:** {api_status}\n\n"

            if company.tech_stack:
                tech_tags = " ".join([f"`{tech}`" for tech in company.tech_stack[:4]])
                markdown_output += f"**🛠️ Tech:** {tech_tags}\n"
            
            if company.language_support:
                lang_tags = " ".join([f"`{lang}`" for lang in company.language_support[:4]])
                markdown_output += f"**💻 Languages:** {lang_tags}\n"

            if company.integration_capabilities:
                integ_tags = " ".join([f"`{integ}`" for integ in company.integration_capabilities[:4]])
                markdown_output += f"**🔗 Integrations:** {integ_tags}\n"
            
            markdown_output += "\n---\n" # Separator

    return markdown_output

def run_research_agent(query: str):
    """
    This is the main function that Gradio will call.
    It takes the user query, runs the workflow, and returns the formatted results.
    """
    if not query or not query.strip():
        return "Please enter a valid query."
    
    print(f"Received query: {query}")
    # The loading state is automatically handled by Gradio on the output component.
    try:
        results = workflow.run(query)
        return format_results_as_markdown(results)
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"## 💥 An Error Occurred\n\n**Details:**\n```\n{e}\n```"


# --- Gradio Interface Definition ---
with gr.Blocks(theme=gr.themes.Soft(), title="Developer Tools Research Agent") as demo:
    gr.Markdown(
        """
        # 🔬 Developer Tools Research Agent
        An AI-powered agent to analyze and compare developer tools using Firecrawl and LangGraph.
        """
    )

    with gr.Row():
        query_input = gr.Textbox(
            label="Enter a developer tool category to research",
            placeholder="e.g., 'vector databases', 'serverless platforms', 'CI/CD tools'",
            scale=4, # Make the textbox wider
        )
        submit_button = gr.Button("🚀 Start Research", variant="primary", scale=1)

    gr.Examples(
        examples=["vector databases", "open source logging tools", "javascript frameworks for backend"],
        inputs=query_input
    )

    results_output = gr.Markdown(label="Research Results")

    # Connect the button click to the function
    submit_button.click(
        fn=run_research_agent,
        inputs=[query_input],
        outputs=[results_output]
    )
    # Also allow submitting with the Enter key
    query_input.submit(
        fn=run_research_agent,
        inputs=[query_input],
        outputs=[results_output]
    )

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch()