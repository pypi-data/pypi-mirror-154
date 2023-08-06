from orpytlex.classes.downloader import Downloader


def main():
    downloader = Downloader()
    url = 'http://mirror-osd.de.bosch.com/ms-teams/dists/stable/main/binary-amd64/Packages.gz'
    downloader.configure(
        url=url,
        output_path='/tmp/Packages.gz',
    )
    print('Downloading file...')
    downloader.download()
    print('Done!')


if __name__ == '__main__':
    main()
