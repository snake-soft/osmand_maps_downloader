import os
from argparse import ArgumentParser
from datetime import datetime
from urllib import request, parse
from pathlib import Path, PurePath
from bs4 import BeautifulSoup


class File:
    def __init__(self, row_data):
        self.row_data = row_data
        self.filename = row_data[0].get_text().strip()
        self.href = row_data[0].find('a')['href']
        self.date = datetime.strptime(row_data[1].get_text(), '%d.%m.%Y').date()
        self.size = row_data[2].get_text()  # MB
        self.name = row_data[3].get_text()
        self.url = parse.urljoin('https://osmand.net', self.href)

    def download(self, path):
        file_path = Path(PurePath(Path(path), Path(self.filename)))
        if file_path.is_dir():
            raise IsADirectoryError(file_path)
        if not self.is_valid(file_path):
            print('- Download {} ({}MB)'.format(self.filename, self.size))
            return request.urlretrieve(self.url, file_path)
        print('x Skip {}'.format(self.filename))

    def is_valid(self, file_path):
        if file_path.is_file():
            if not any((self.file_is_old(file_path),
                       self.file_is_incomplete(file_path))):
                return True
        return False

    def file_is_old(self, file_path):
        file_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        return self.date >= file_date.date()

    def file_is_incomplete(self, file_path):
        site = request.urlopen(self.url)
        meta = site.info()
        dl_size = int(meta.get('Content-Length'))
        file_size = os.path.getsize(file_path)
        return file_size != dl_size


class Parser:
    parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
    index_url = 'https://osmand.net/list.php'

    def __init__(self):
        resp = request.urlopen(self.index_url)
        soup = BeautifulSoup(
            resp, self.parser, from_encoding=resp.info().get_param('charset')
        )
        table = soup.find('table')
        self.rows = table.find_all('tr')

    def get_files(self):
        for row in self.rows[1:]:
            row_data = row.find_all('td')
            yield File(row_data)


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Download Osmand maps for local mirroring')
    arg_parser.add_argument('directory', help='Download target directory')
    args = arg_parser.parse_args()

    directory = Path(args.directory)
    directory.mkdir(parents=True, exist_ok=True)
    files = Parser().get_files()
    for file in files:
        file.download(directory)
