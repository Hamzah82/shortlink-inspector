import requests
from urllib.parse import urlparse
import urllib3
import sys
from time import sleep
import pyfiglet
from termcolor import colored
from tqdm import tqdm

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def display_banner():
    """Show cool ASCII art banner"""
    try:
        ascii_art = pyfiglet.figlet_format("URL ANALYZER", font="slant")
        print(colored(ascii_art, "cyan"))
    except:
        print(colored("URL ANALYZER", "cyan", attrs=["bold"]))
    
    print(colored("⎯" * 60, "blue"))
    print(colored("🔍 Track short URL redirects and analyze final destination", "yellow"))
    print(colored("⎯" * 60, "blue"))
    print(colored("v1.1", "yellow"))
    print()

def analyze_short_url(short_url):
    """Analyze the short URL with visual feedback"""
    try:
        # Show progress animation
        with tqdm(total=100, desc=colored("Analyzing URL", "cyan"), ncols=70, 
                 bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            for i in range(10):
                sleep(0.05)
                pbar.update(10)
        
        response = requests.head(short_url, allow_redirects=False, verify=False, timeout=10)
        
        redirect_chain = [short_url]
        final_url = short_url
        status_codes = []
        
        # Follow redirects with progress
        while response.is_redirect:
            redirect_url = response.headers['Location']
            redirect_chain.append(redirect_url)
            final_url = redirect_url
            status_codes.append(response.status_code)
            
            # Show redirect animation
            print(colored(" ↳ Redirecting...", "magenta"))
            with tqdm(total=50, desc=colored("Following redirect", "light_cyan"), 
                     leave=False, ncols=50) as redirect_bar:
                for i in range(50):
                    sleep(0.01)
                    redirect_bar.update(1)
            
            response = requests.head(redirect_url, allow_redirects=False, verify=False, timeout=10)
        
        status_codes.append(response.status_code)
        
        # Get final page info
        try:
            final_response = requests.get(final_url, verify=False, timeout=10)
            title = "Not found"
            if '<title>' in final_response.text:
                title = final_response.text.split('<title>')[1].split('</title>')[0]
        except:
            title = "Failed to retrieve title"
        
        return {
            'original_url': short_url,
            'final_url': final_url,
            'redirect_chain': redirect_chain,
            'status_codes': status_codes,
            'title': title,
            'is_redirected': len(redirect_chain) > 1,
            'error': None
        }
        
    except Exception as e:
        return {
            'original_url': short_url,
            'error': str(e)
        }

def display_results(result):
    """Display results with cool formatting"""
    print("\n" + colored("⎯" * 60, "blue"))
    print(colored("📊 ANALYSIS RESULTS", "green", attrs=["bold"]))
    print(colored("⎯" * 60, "blue"))
    
    print(colored("\n🔗 Original URL:", "yellow"), result['original_url'])
    
    if result.get('error'):
        print(colored("\n❌ Error:", "red"), result['error'])
        return
    
    print(colored("🎯 Final URL:", "yellow"), result['final_url'])
    print(colored("🔄 Was redirected?", "yellow"), 
          colored("Yes", "green") if result['is_redirected'] else colored("No", "red"))
    
    if result['is_redirected']:
        print(colored("\n🛣️ Redirect Path:", "yellow"))
        for i, (url, status) in enumerate(zip(result['redirect_chain'], result['status_codes'])):
            print(f"  {colored('➜', 'light_blue')} Step {i+1}: {url} {colored(f'[{status}]', 'light_magenta')}")
    
    print(colored("\n📝 Page Title:", "yellow"), result.get('title', 'N/A'))
    
    # Show domain info
    parsed = urlparse(result['final_url'])
    print(colored("\n🌐 Domain Information:", "yellow"))
    print(f"  {colored('•', 'green')} Domain: {parsed.netloc}")
    print(f"  {colored('•', 'green')} Path: {parsed.path or '/'}")
    print(f"  {colored('•', 'green')} Query: {parsed.query or 'None'}")
    print(f"  {colored('•', 'green')} Fragment: {parsed.fragment or 'None'}")
    
    # Show security info
    print(colored("\n🔒 Security:", "yellow"))
    scheme = colored("HTTPS", "green") if result['final_url'].startswith('https') else colored("HTTP", "red")
    print(f"  {colored('•', 'green')} Protocol: {scheme}")
    
    print(colored("\n" + "⎯" * 60, "blue"))

def main():
    display_banner()
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input(colored("Enter short URL to analyze: ", "light_blue"))
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    result = analyze_short_url(url)
    display_results(result)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n🚫 Operation cancelled by user", "red"))
    except Exception as e:
        print(colored(f"\n💥 Error: {str(e)}", "red"))
