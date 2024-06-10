import requests
from bs4 import BeautifulSoup
import time

def read_sources_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def scrape_proxies(url):
    proxies = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Customize this based on the actual page structure of your proxy sources
        proxy_elements = soup.find_all('td', text=True)
        for element in proxy_elements:
            proxy = element.text.strip()
            proxies.append(proxy)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return proxies

def check_proxy(proxy):
    try:
        proxies = {
            'http': f'socks5://{proxy}',
            'https': f'socks5://{proxy}'
        }
        response = requests.get('http://example.com', proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except Exception as e:
        print(f"Error checking proxy {proxy}: {e}")
    return False

def main():
    source_file = 'sources.list'
    source_urls = read_sources_list(source_file)

    all_proxies = []
    for url in source_urls:
        all_proxies.extend(scrape_proxies(url))
        time.sleep(2)  # To prevent being blocked by the server
    
    live_proxies = []
    for proxy in all_proxies:
        if check_proxy(proxy):
            live_proxies.append(proxy)
    
    with open('live_proxies.txt', 'w') as f:
        for proxy in live_proxies:
            f.write(proxy + '\n')

if __name__ == "__main__":
    main()
