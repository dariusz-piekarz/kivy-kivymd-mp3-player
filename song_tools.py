from eyed3 import load


def get_metadata(path):
    audiofile = load(path)
    return {'Path': path,
            'Title': audiofile.tag.title,
            'Author': audiofile.tag.artist,
            'Album': audiofile.tag.album
            }


def convert_time(time):
    minutes, seconds = divmod(int(time), 60)
    return f"{minutes:02}:{seconds:02}"
