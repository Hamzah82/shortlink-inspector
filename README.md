# 🔗 URL Analyzer

A lightweight Python tool to analyze short URLs, trace redirect chains, and display useful metadata including the final destination, page title, and security protocol — all with colorful and interactive CLI output.

![URL Analyzer Banner](https://img.shields.io/badge/version-1.1-blue)
![Python](https://img.shields.io/badge/python-3.7+-yellow)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🚀 Features

- Follows and displays redirect chain step-by-step  
- Shows HTTP status codes of each redirect  
- Extracts and prints final URL and page title  
- Displays URL components (domain, path, query, etc.)  
- Visual CLI output with progress bars and colors  
- Supports both HTTP and HTTPS protocols  
- Built-in banner and friendly UX  

---

## 📦 Dependencies

- `requests`  
- `pyfiglet`  
- `termcolor`  
- `tqdm`  
- `urllib3`  

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠 Usage

```bash
python url_analyzer.py https://bit.ly/example
```

Or run and input manually:

```bash
python url_analyzer.py
```

---

## 🖥 Example Output

```
URL ANALYZER
------------------------------------------------------------
🔍 Track short URL redirects and analyze final destination
------------------------------------------------------------

Enter short URL to analyze: bit.ly/example

Analyzing URL: 100%
 ↳ Redirecting...
 ↳ Redirecting...

📊 ANALYSIS RESULTS
🔗 Original URL: bit.ly/example
🎯 Final URL: https://example.com/page
🔄 Was redirected? Yes

🛣️ Redirect Path:
 ➜ Step 1: http://bit.ly/example [301]
 ➜ Step 2: https://example.com/page [200]

📝 Page Title: Example Domain

🌐 Domain Information:
 • Domain: example.com
 • Path: /page
 • Query: None
 • Fragment: None

🔒 Security:
 • Protocol: HTTPS
```

---

## ❗ Warning

This tool disables SSL verification for testing short links that might not have valid certificates. **Use responsibly.**

---

## 📄 License

MIT License © Awangku Muhammad Hamzah
