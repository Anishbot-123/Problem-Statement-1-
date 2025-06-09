import re
from collections import Counter

LOG_PATH = "access.log"  # Replace with your log file path

def parse_log(file_path):
    with open(file_path, 'r') as f:
        logs = f.readlines()

    ip_counter = Counter()
    url_counter = Counter()
    error_404_count = 0

    for line in logs:
        match = re.match(r'(\d+\.\d+\.\d+\.\d+) - - \[.*?\] "(GET|POST) (.*?) HTTP.*" (\d+)', line)
        if match:
            ip = match.group(1)
            url = match.group(3)
            status = match.group(4)

            ip_counter[ip] += 1
            url_counter[url] += 1

            if status == "404":
                error_404_count += 1

    return ip_counter, url_counter, error_404_count

def print_report(ip_counter, url_counter, error_404_count):
    print("====== Web Log Analysis Report ======")
    print(f"Total 404 Errors: {error_404_count}\n")

    print("Top 5 Requested URLs:")
    for url, count in url_counter.most_common(5):
        print(f"{url}: {count} times")

    print("\nTop 5 IPs by Request Count:")
    for ip, count in ip_counter.most_common(5):
        print(f"{ip}: {count} requests")

if __name__ == "__main__":
    ip_data, url_data, error_404s = parse_log(LOG_PATH)
    print_report(ip_data, url_data, error_404s)
