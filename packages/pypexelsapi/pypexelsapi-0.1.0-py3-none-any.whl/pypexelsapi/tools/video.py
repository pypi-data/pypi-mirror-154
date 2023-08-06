from typing import Union

from .photographer import Photographer


class Video:
    def __init__(self, json):
        self.__video = json

    @property
    def id(self) -> int:
        return int(self.__video['id'])

    @property
    def width(self) -> int:
        return int(self.__video['width'])

    @property
    def height(self) -> int:
        return int(self.__video['height'])

    @property
    def image(self) -> str:
        return self.__video['image']

    @property
    def duration(self) -> int:
        return int(self.__video['duration'])

    @property
    def photographer(self) -> Photographer:
        return Photographer(self.__video['user']['name'],
                            self.__video['user']['url'],
                            int(self.__video['user']['id']))

    class Video_file:
        def __init__(self, id: int, quality: str, file_type: str, width: int, height: int, link: str):
            self.id = id
            self.quality = quality
            self.file_type = file_type
            self.width = width
            self.height = height
            self.link = link

    @property
    def video_files(self) -> list[Video_file]:
        return [self.Video_file(vf['id'], vf['quality'], vf['file_type'], vf['width'], vf['height'], vf['link'])
                for vf in self.__video['video_files']]

    class Video_picture:
        def __init__(self, id: int, picture: str, nr: int):
            self.id = id
            self.picture = picture,
            self.nr = nr

    @property
    def video_pictures(self) -> list[Video_picture]:
        return [self.Video_picture(vp['id'], vp['picture'], vp['nr']) for vp in self.__video['video_pictures']]


class Video_request:
    def __init__(self, request):
        self.__request = request

    @property
    def page(self) -> int:
        return int(self.__request['page'])

    @property
    def url(self) -> str:
        return self.__request['url']

    @property
    def per_page(self) -> int:
        return int(self.__request['per_page'])

    @property
    def total_results(self) -> int:
        return int(self.__request['total_results'])

    @property
    def prev_page(self) -> Union[int, None]:
        try:
            return int(self.__request['prev_page'])
        except:
            return None

    @property
    def next_page(self) -> Union[int, None]:
        try:
            return int(self.__request['next_page'])
        except:
            return None

    @property
    def videos(self) -> list[Video]:
        return [Video(video) for video in self.__request['videos']]
