mkdir -p ~/.streamlit/

echo "[theme]
primaryColor = '#69FFB3'
backgroundColor = '#3037351F'
secondaryBackgroundColor = '#f37b05'
textColor= '#FFFFFF'
font = ‘sans serif’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml