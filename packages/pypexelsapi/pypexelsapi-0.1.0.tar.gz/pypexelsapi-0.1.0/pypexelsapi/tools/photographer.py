class Photographer:
    def __init__(self, ph: str, url: str, id: int):
        self.photographer: str = ph
        self.photographer_url: str = url
        self.photographer_id: int = id

    def __str__(self):
        return f'name: {self.photographer}\nurl: {self.photographer_url}\nid: {self.photographer_id}'
