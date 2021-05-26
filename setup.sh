mkdir -p ~/.streamlit/config.toml

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\

[theme]
base="dark"
primaryColor = '#69FFB3'
backgroundColor = '#3037351F'
secondaryBackgroundColor= '#f37b05'
textColor = '#FFFFFF'
font = "sans serif"
" > ~/.streamlit/config.toml