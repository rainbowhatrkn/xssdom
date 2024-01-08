import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import questionary
import os
import subprocess
import multiprocessing

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

def test_payload(url, payload, result_file):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        if payload_in_html(payload, str(soup)):
            print(Fore.GREEN + '[ XSS Found ✓ ]', '   ', f"{url} - Payload: {payload}" + Fore.RESET)
            with open(result_file, 'a') as result:
                print(f"[ XSS Found ✓ ] {url} - Payload: {payload}", file=result)
        else:
            print(Fore.YELLOW + '[ XSS NOT Found ]', '   ', f"{url} - Payload: {payload}" + Fore.RESET)

    except Exception as e:
        pass

def payload_in_html(payload, html_content):
    return payload in html_content

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

    domain_list = read_domain_list(file_path, encoding)

    if domain_list:
        payloads_file = 'payloads.txt'
        result_file = 'resultsdom.txt'
        payloads = open(payloads_file, 'r').readlines()

        with ThreadPoolExecutor(max_workers=10) as executor, multiprocessing.Pool() as pool:
            for domain in domain_list:
                print(f"{Fore.CYAN}Processing domain: {domain}{Fore.RESET}")
                urls_with_parameters = get_urls_with_parameters(domain)
                if not urls_with_parameters:
                    print(f"{Fore.YELLOW}No URLs with parameters found for {domain}{Fore.RESET}")
                    continue

                for url in urls_with_parameters:
                    for payload in payloads:
                        payload = payload.strip('\n')
                        pool.apply_async(test_payload, (url, payload, result_file))

        print(f"{Fore.CYAN}Results saved to {result_file}{Fore.RESET}")

        # Add a wait to prevent the script from terminating abruptly
        input("Press Enter to exit...")