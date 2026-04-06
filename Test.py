import time
from requests import get, RequestException

def open_file():
    s = []
    try:
        with open("urls.txt") as f:
            s = [line.strip() for line in f if line.strip() and line.startswith("http")]
    except FileNotFoundError:
        print("File not found")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    else:
        return s

def conn(url, count):
    try:
        response = get(url, timeout=10)
        if response.status_code == 200:
            with open(f"data_{count}.html", "w", encoding='utf-8') as file:
                file.write(response.text)
        else :
            print(f"Error: {response.status_code}")
            exit(1)
    except  RequestException as e:
        print(f"Error: {e}")
        exit(1)


def main():
    count = 0
    s = open_file()
    for url in s:
        conn(url, count)
        count += 1

print(time.strftime('%X'))
main()
print(time.strftime('%X'))






