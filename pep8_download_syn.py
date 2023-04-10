import time
import requests


def download_pep(pep_number: int) -> bytes:
    url = f"https://www.python.org/dev/peps/pep-{pep_number}/"
    print(f"Begin downloading {url}")
    response = requests.get(url)
    print(f"Finished downloading {url}")
    return response.content


def write_to_file(pep_number: int, content: bytes) -> None:
    file_path = '/'.join(["test_pep", f"sync_pep{pep_number}.html"])
    with open(file_path, 'wb') as f:
        print(f"Begin writing to file {file_path}")
        f.write(content)
        print(f"Finished writing to file {file_path}")


if __name__ == '__main__':
    s = time.perf_counter()
    for i in range(8010, 8016):
        content = download_pep(i)
        write_to_file(i, content)
    elapsed = time.perf_counter()-s
    print(f"Execution {elapsed: 0.2f} seconds.")