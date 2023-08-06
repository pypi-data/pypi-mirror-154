from typing import Union
from .photographer import Photographer


class Photo:
    def __init__(self, json):
        self.__photo = json

    @property
    def id(self) -> int:
        return int(self.__photo['id'])

    @property
    def width(self) -> int:
        return int(self.__photo['width'])

    @property
    def height(self) -> int:
        return int(self.__photo['height'])

    @property
    def url(self) -> str:
        return self.__photo['url']

    @property
    def avg_color(self) -> str:
        return self.__photo['avg_color']

    @property
    def original(self) -> str:
        return self.__photo['src']['original']

    @property
    def large2x(self) -> str:
        return self.__photo['src']['large2x']

    @property
    def large(self) -> str:
        return self.__photo['src']['large']

    @property
    def medium(self) -> str:
        return self.__photo['src']['medium']

    @property
    def small(self) -> str:
        return self.__photo['src']['small']

    @property
    def portrait(self) -> str:
        return self.__photo['src']['portrait']

    @property
    def landscape(self) -> str:
        return self.__photo['src']['landscape']

    @property
    def tiny(self) -> str:
        return self.__photo['src']['tiny']

    @property
    def liked(self) -> bool:
        return True if self.__photo['liked'] == 'true' else False

    @property
    def alt(self) -> str:
        return self.__photo['alt']

    @property
    def photographer(self) -> Photographer:
        return Photographer(self.__photo['photographer'],
                            self.__photo['photographer_url'],
                            int(self.__photo['photographer_id']))


class Photo_request:
    def __init__(self, request):
        self.__request = request

    @property
    def page(self) -> int:
        return int(self.__request['page'])

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
    def photos(self) -> list[Photo]:
        return [Photo(photo) for photo in self.__request['photos']]
