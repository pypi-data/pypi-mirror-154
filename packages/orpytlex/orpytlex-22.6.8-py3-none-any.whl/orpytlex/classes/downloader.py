from pathlib import Path
import requests


class Downloader:
    url: str
    output_path: Path

    def configure(self, url: str, output_path: Path):
        self.url = url
        self.output_path = Path(output_path)

    def download(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            self.output_path.write_bytes(response.content)
            # with open(output_path, 'wb') as f:
            #     f.write(response.content)
