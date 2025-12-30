import gradio as gr
import requests
import pandas as pd
from supabase import create_client

# --- 1. CONFIGURATION & ASSETS ---
SUPABASE_URL = "https://yrpeuerrazwpiwsfrlpb.supabase.co"
SUPABASE_KEY = "sb_publishable_jMyG1iBQ9a2SjBI0LNEjkQ_qTIeOLpb"
LOGO_URL = "https://raw.githubusercontent.com/akashpgp2026/mishtee-magic/refs/heads/main/Gemini_Generated_Image_dug351dug351dug3.png"
STYLE_PY_URL = "https://raw.githubusercontent.com/akashpgp2026/mishtee-magic/refs/heads/main/style.py"

# Initialize Supabase Client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_brand_assets():
    """Fetches the custom CSS from style.py on GitHub."""
    try:
        response = requests.get(STYLE_PY_URL)
        namespace = {}
        exec(response.text, namespace)
        return namespace.get('mishtee_css', "")
    except:
        return "" # Fallback to empty if connection fails

mishtee_css = get_brand_assets()

# --- 2. BACKEND FUNCTIONS ---

def get_customer_dashboard(phone_number):
    """Retrieves customer info and order history."""
    if not phone_number or not phone_number.startswith('9'):
        return "Please enter a valid 10-digit number starting with 9.", pd.DataFrame()

    # Fetch Customer Name
    cust_res = supabase.table("customers").select("full_name").eq("phone", phone_number).execute()
    
    if not cust_res.data:
        return "Namaste! We couldn't find your profile. Register to start your journey.", pd.DataFrame()
    
    name = cust_res.data[0]['full_name']
    greeting = f"## Namaste, {name} ji! \nGreat to see you again."

    # Fetch Orders with Product Join
    order_res = supabase.table("orders").select(
        "order_id, order_date, qty_kg, status, products(sweet_name)"
    ).eq("cust_phone", phone_number).execute()
    
    if order_res.data:
        df = pd.DataFrame(order_res.data)
        df['Sweet Name'] = df['products'].apply(lambda x: x['sweet_name'] if x else "N/A")
        df = df[['order_id', 'order_date', 'Sweet Name', 'qty_kg', 'status']]
        df.columns = ['Order ID', 'Date', 'Product', 'Weight (kg)', 'Status']
    else:
        df = pd.DataFrame(columns=['Order ID', 'Date', 'Product', 'Weight (kg)', 'Status'])

    return greeting, df

def get_trending_sweets():
    """Aggregates top 4 best sellers."""
    res = supabase.table("orders").select("qty_kg, products(sweet_name, variant_type)").execute()
    if not res.data:
        return pd.DataFrame()

    raw_df = pd.DataFrame(res.data)
    raw_df['Sweet Name'] = raw_df['products'].apply(lambda x: x['sweet_name'])
    raw_df['Variant'] = raw_df['products'].apply(lambda x: x['variant_type'])
    
    trending = raw_df.groupby(['Sweet Name', 'Variant'])['qty_kg'].sum().reset_index()
    trending = trending.sort_values(by='qty_kg', ascending=False).head(4)
    trending.columns = ['Sweet Name', 'Collection', 'Total Sold (kg)']
    return trending

# --- 3. GRADIO UI LAYOUT ---

with gr.Blocks(css=mishtee_css, title="MishTee-Magic") as demo:
    
    # Header Section
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML(f"""
                <div style="text-align: center; padding: 20px 0;">
                    <img src="{LOGO_URL}" alt="MishTee-Magic Logo" style="max-width: 200px; margin: auto;">
                    <h1 style="font-size: 1.5em; letter-spacing: 2px;">PURE A2 QUALITY. ORGANIC MAGIC.</h1>
                </div>
            """)

    # Welcome & Login Logic
    with gr.Row():
        with gr.Column(scale=1):
            with gr.Row():
                with gr.Column(scale=1): pass # Spacer
                with gr.Column(scale=2):
                    greeting_output = gr.Markdown("### Welcome to the World of MishTee-Magic")
                    phone_input = gr.Textbox(label="Enter Mobile Number", placeholder="9XXXXXXXXX")
                    login_btn = gr.Button("ENTER THE MAGIC", variant="primary")
                with gr.Column(scale=1): pass # Spacer

    gr.HTML("<hr style='border: 0; border-top: 1px solid #333; margin: 40px 0;'>")

    # Data Tables (Tabbed for Professional Minimalism)
    with gr.Tabs():
        with gr.TabItem("MY ORDER HISTORY"):
            history_table = gr.DataFrame(interactive=False)
            
        with gr.TabItem("TRENDING TODAY"):
            trending_table = gr.DataFrame(interactive=False)

    # Event Handlers
    def on_login(phone):
        greeting, orders = get_customer_dashboard(phone)
        trending = get_trending_sweets()
        return greeting, orders, trending

    login_btn.click(
        fn=on_login,
        inputs=phone_input,
        outputs=[greeting_output, history_table, trending_table]
    )

    # Footer
    gr.Markdown(
        "<div style='text-align: center; padding-top: 40px; font-size: 0.7em; color: #666;'>"
        "Handcrafted with Love in Ahmedabad | Low-Sugar | Low-Gluten | Organic"
        "</div>"
    )

if __name__ == "__main__":
    demo.launch()
