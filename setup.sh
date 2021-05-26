mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "[theme] "\
base="dark"
primaryColor = '#69FFB3'
backgroundColor = '#3037351F'
secondaryBackgroundColor= '#f37b05'
textColor = '#FFFFFF'

echo "\
[server]\n\
headless = true\n\
enableCORS=true\n\
port = $PORT\n\
" > ~/.streamlit/config.toml