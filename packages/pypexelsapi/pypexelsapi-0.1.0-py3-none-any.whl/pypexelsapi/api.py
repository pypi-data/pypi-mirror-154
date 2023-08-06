import requests
from tools import Photo, Photo_request, Video, Video_request
from typing import TypedDict, Optional, Literal, Union


class search_params(TypedDict):
    query: str
    orientation: Optional[Literal['landscape', 'portrait', 'square']]
    size: Optional[Literal['large', 'medium', 'small']]
    color: Optional[Union[Literal['red', 'orange', 'yellow', 'green', 'turquoise', 'blue',
                                  'violet', 'pink', 'brown', 'black', 'gray', 'white'], str]]
    locale: Optional[Literal['en-US', 'pt-BR', 'es-ES', 'ca-ES', 'de-DE', 'it-IT', 'fr-FR', 'sv-SE', 'id-ID', 'pl-PL',
                             'ja-JP', 'zh-TW', 'zh-CN', 'ko-KR', 'th-TH', 'nl-NL', 'hu-HU', 'vi-VN', 'cs-CZ', 'da-DK',
                             'fi-FI', 'uk-UA', 'el-GR', 'ro-RO', 'nb-NO', 'sk-SK', 'tr-TR', 'ru-RU']]
    page: Optional[int]
    per_page: Optional[int]


class get_curated_params(TypedDict):
    page: Optional[int]
    per_page: Optional[int]


class get_popular_params(TypedDict):
    min_width: Optional[int]
    min_height: Optional[int]
    min_duration: Optional[int]
    max_duration: Optional[int]
    page: Optional[int]
    per_page: Optional[int]


class API:
    def __init__(self, API_KEY: str):
        self.PEXELS_AUTHORIZATION = {"Authorization": API_KEY}
        self.request = None
        self.parsed = None

    '''Public photos methods'''
    def search_photos(self, params: search_params) -> Photo_request:
        url = 'https://api.pexels.com/v1/search'
        self.__request(url, params)
        return Photo_request(self.parsed)

    def get_curated(self, params: get_curated_params) -> Photo_request:
        url = 'https://api.pexels.com/v1/curated'
        self.__request(url, params)
        return Photo_request(self.parsed)

    def get_photo(self, id: Union[int, str]) -> Photo:
        url = 'https://api.pexels.com/v1/photos/' + str(id)
        self.__request(url, None)
        return Photo(self.parsed)

    '''Public video methods'''
    def search_videos(self, params: search_params) -> Video_request:
        url = 'https://api.pexels.com/videos/search'
        self.__request(url, params)
        return Video_request(self.parsed)

    def get_popular(self, params: Union[get_popular_params, None]) -> Video_request:
        url = 'https://api.pexels.com/videos/popular'
        self.__request(url, params)
        return Video_request(self.parsed)

    def get_video(self, id: Union[int, str]) -> Video:
        url = 'https://api.pexels.com/v1/videos/' + str(id)
        self.__request(url, None)
        return Video(self.parsed)

    '''Private methods'''
    def __request(self, url: str, params: Union[dict, None]):
        try:
            self.request = requests.get(url, params=params, timeout=15, headers=self.PEXELS_AUTHORIZATION)
            self.parsed = self.request.json()
            if not self.request.ok:
                print('Wrong response you might have a wrong API key')
                print(self.request)
                print(f'API key: {self.PEXELS_AUTHORIZATION}')
                self.request = None
                self.parsed = None
                exit()

        except requests.exceptions.RequestException:
            print('Request failed, check your internet connection')
            self.request = None
            self.parsed = None
            exit()
