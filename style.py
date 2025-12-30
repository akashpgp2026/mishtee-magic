mishtee_css = """
/* Global Styles - High-End Minimalist */
body, .gradio-container {
    background-color: #FAF9F6 !important;
    color: #333333 !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* Typography - Spaced out Serif for Headings */
h1, h2, h3, .section-header {
    font-family: 'Playfair Display', 'Georgia', serif !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    margin-bottom: 1.5rem !important;
}

/* Button Styling - Sober Terracotta & Sharp Lines */
button.primary, .gr-button-lg {
    background-color: #C06C5C !important;
    color: #FAF9F6 !important;
    border: none !important;
    border-radius: 0px !important; /* Sharp corners */
    padding: 12px 24px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    letter-spacing: 0.1em !important;
    transition: opacity 0.3s ease !important;
}

button.primary:hover {
    opacity: 0.9 !important;
    box-shadow: none !important;
}

/* Tables - Lightweight Sans-Serif */
table, .gr-table {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    border-collapse: collapse !important;
}

/* Borders and Spacing */
.gr-box, .gr-input, .gr-block, .gr-form {
    border: 1px solid #333333 !important;
    border-radius: 0px !important; /* Remove bubbly corners */
    background: transparent !important;
    box-shadow: none !important; /* No shadows */
    margin: 20px 0px !important;
    padding: 30px !important; /* Significant whitespace */
}

/* Input Fields */
input, textarea {
    background-color: #FAF9F6 !important;
    border: 1px solid #333333 !important;
    border-radius: 0px !important;
}

/* Remove default Gradio accent colors */
:root {
    --primary-500: #C06C5C !important;
    --radius-lg: 0px !important;
    --block-shadow: none !important;
}
"""
