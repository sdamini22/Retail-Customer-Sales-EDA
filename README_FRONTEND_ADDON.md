## Run the interactive dashboard

The project includes an optional Streamlit frontend (`app.py`) for interactive exploration.

1. Install dependencies:
   `pip install -r requirements.txt`
2. Start the dashboard:
   `streamlit run app.py`
3. Open the local URL shown in the terminal.
4. Upload the original or cleaned retail sales CSV using the sidebar file uploader.

The dashboard automatically detects numeric, categorical, and likely date columns. It shows dataset metrics, missing-value and duplicate checks, previews, summaries, and suitable charts. It does not alter the uploaded source file.
