import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup

def scrape_proxies():
    # URL of the website to scrape proxies from
    url = 'https://www.sslproxies.org/'

    try:
        # Send a GET request to the website
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the table that contains the proxy details
            proxy_table = soup.find('table', {'id': 'proxylisttable'})

            # Extract proxies from the table
            proxies = []
            for row in proxy_table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 8:
                    ip = cells[0].text
                    port = cells[1].text
                    proxy = f"{ip}:{port}"
                    proxies.append(proxy)

            # Update the "scrape_output" Text widget with the scraped proxies
            scrape_output.insert(tk.END, f"Scraped {len(proxies)} proxies:\n")
            for proxy in proxies:
                scrape_output.insert(tk.END, f"Proxy: {proxy}\n")
        else:
            scrape_output.insert(tk.END, f"Failed to fetch proxies. Status Code: {response.status_code}\n")
    except Exception as e:
        scrape_output.insert(tk.END, f"An error occurred: {e}\n")
        
def check_proxies():
    # Get the list of proxies from the "scrape_output" Text widget
    proxies = scrape_output.get("1.0", tk.END).strip().split("\n")
    
    # URL to check the proxies (replace with your target URL)
    target_url = 'https://www.google.com'
    
    try:
        working_proxies = []
        for proxy in proxies:
            # Create a proxy dictionary to be used by requests
            proxy_dict = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            
            try:
                # Send a test request using the proxy
                response = requests.get(target_url, proxies=proxy_dict, timeout=10)
                
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    working_proxies.append(proxy)
            except Exception as e:
                # If the request fails or times out, the proxy is likely not working
                continue
        
        # Update the "check_output" Text widget with the working proxies
        check_output.insert(tk.END, f"Working Proxies:\n")
        for proxy in working_proxies:
            check_output.insert(tk.END, f"Proxy: {proxy}\n")
        check_output.insert(tk.END, f"Total Working Proxies: {len(working_proxies)}\n")
    except Exception as e:
        check_output.insert(tk.END, f"An error occurred: {e}\n")

def save_results():
    # Get the content of the "scrape_output" and "check_output" Text widgets
    scrape_results = scrape_output.get("1.0", tk.END)
    check_results = check_output.get("1.0", tk.END)
    
    # Concatenate the results from both outputs
    all_results = scrape_results + "\n" + check_results
    
    try:
        # Prompt the user to select the file save location
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(all_results)
            
            # Inform the user that the results were saved successfully
            tk.messagebox.showinfo("Results Saved", "Scan results have been saved successfully.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while saving the results: {e}")
        
def load_ip_list():
    try:
        # Prompt the user to select the file containing IP addresses
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                # Read the content of the file
                ip_list = file.read()

            # Clear the existing content in the "scrape_output" Text widget
            scrape_output.delete("1.0", tk.END)
            
            # Insert the content of the file into the "scrape_output" Text widget
            scrape_output.insert(tk.END, ip_list)

            # Inform the user that the IP addresses have been loaded successfully
            tk.messagebox.showinfo("IP Addresses Loaded", "IP addresses have been loaded successfully.")
    except Exception as e:
        tk.messagebox.showerror("Error", f"An error occurred while loading IP addresses: {e}")


def clear_results():
    # Clear the content of the console output boxes
    scrape_output.delete("1.0", tk.END)
    check_output.delete("1.0", tk.END)

    # Add any additional clearing logic here for other data if needed

# Create the main application window
app = tk.Tk()
app.title("Proxy Scraper and Checker")

# Add buttons
scrape_button = tk.Button(app, text="Scrape Proxies", command=scrape_proxies)
scrape_button.pack()

check_button = tk.Button(app, text="Check Proxies", command=check_proxies)
check_button.pack()

save_button = tk.Button(app, text="Save Results", command=save_results)
save_button.pack()

load_button = tk.Button(app, text="Load IP List", command=load_ip_list)
load_button.pack()

# Add a "Clear" button to clear any scans and files in memory
clear_button = tk.Button(app, text="Clear", command=clear_results)
clear_button.pack()

# Add options here using Tkinter widgets (e.g., Checkbuttons, Entry, etc.)

# Add console output boxes for showing real-time progress with a 3px border
scrape_output = tk.Text(app, height=10, width=50, bd=3)
scrape_output.pack()

check_output = tk.Text(app, height=10, width=50, bd=3)
check_output.pack()

# Run the application
app.mainloop()
