import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import questionary
import os
import subprocess
import multiprocessing

# Function to get URLs with parameters
def get_urls_with_parameters(domain):
    try:
        command = f"gau {domain}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        if error:
            print(f"{Fore.RED}Error running gau: {error}")
            return []

        urls = [url.strip() for url in output.split('\n') if '=' in url]
        return urls

    except Exception as e:
        print(f"{Fore.RED}Error retrieving URLs: {e}")
        return []

# Function to test payload
def test_payload(args):
    url, payload, result_file, proxy = args
    try:
        response = requests.get(url, proxies=proxy)
        soup = BeautifulSoup(response.text, 'html.parser')

        if payload_in_html(payload, str(soup)):
            print(Fore.GREEN + '[ XSS Found ✓ ]', '   ', f"{url} - Payload: {payload}" + Fore.RESET)
            with open(result_file, 'a') as result:
                print(f"[ XSS Found ✓ ] {url} - Payload: {payload}", file=result)
        else:
            print(Fore.YELLOW + '[ XSS NOT Found ]', '   ', f"{url} - Payload: {payload}" + Fore.RESET)

    except Exception as e:
        pass

# Function to check payload in HTML content
def payload_in_html(payload, html_content):
    return payload in html_content

# Function to read domain list from file
def read_domain_list(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read().splitlines()

    except UnicodeDecodeError:
        print(f"{Fore.RED}Erreur de décodage. Assurez-vous que le fichier utilise l'encodage correct.")
        return None

    except FileNotFoundError:
        print(f"{Fore.RED}Le fichier spécifié n'a pas été trouvé.")
        return None

if __name__ == "__main__":
    file_path = questionary.text("Entrez le chemin du fichier de domaines:").ask()
    encoding = questionary.text("Entrez l'encodage du fichier (ex: utf-8, iso-8859-1):").ask()

    # Prompt user for proxy input, defaulting to None
    proxy_input = questionary.text("Entrez l'adresse du proxy (laissez vide pour ne pas utiliser de proxy):", default="").ask()
    proxy = {'http': proxy_input, 'https': proxy_input} if proxy_input else None

    domain_list = read_domain_list(file_path, encoding)

    if domain_list:
        payloads_file = 'payloads.txt'
        result_file = 'resultsdom.txt'
        payloads = open(payloads_file, 'r').readlines()

        with ThreadPoolExecutor(max_workers=10) as executor, multiprocessing.Pool() as pool:
            args_list = []
            for domain in domain_list:
                print(f"{Fore.CYAN}Processing domain: {domain}{Fore.RESET}")
                urls_with_parameters = get_urls_with_parameters(domain)
                if not urls_with_parameters:
                    print(f"{Fore.YELLOW}No URLs with parameters found for {domain}{Fore.RESET}")
                    continue

                for url in urls_with_parameters:
                    for payload in payloads:
                        payload = payload.strip('\n')
                        args_list.append((url, payload, result_file, proxy))

            pool.map(test_payload, args_list)

        print(f"{Fore.CYAN}Results saved to {result_file}{Fore.RESET}")

        # Add a wait to prevent the script from terminating abruptly
        input("Press Enter to exit...")