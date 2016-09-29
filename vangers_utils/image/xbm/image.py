from typing import Any, Dict

from PIL import Image


class XbmImage:
    class Meta:
        def __init__(self, posx: int, posy: int, size_x: int, size_y: int, b_size_x: int, b_size_y: int,
                     image_size: int):
            self.image_size = image_size
            self.posx = posx
            self.posy = posy
            self.size_x = size_x
            self.size_y = size_y
            self.b_size_x = b_size_x
            self.b_size_y = b_size_y

        def __str__(self):
            return """XbmImage.Meta(
    image_size={image_size},
    posx={posx},
    posy={posy},
    size_x={size_x},
    size_y={size_y},
    b_size_x={b_size_x},
    b_size_y={b_size_y})
            """.format(**self.__dict__)

        def to_dict(self)->Dict[str, Any]:
            return {
                'image_size': self.image_size,
                'posx': self.posx,
                'posy': self.posy,
                'size_x': self.size_x,
                'size_y': self.size_y,
                'b_size_x': self.b_size_x,
                'b_size_y': self.b_size_y,
            }

        @staticmethod
        def from_dict(d: Dict[str, Any])->'XbmImage.Meta':
            return XbmImage.Meta(**d)

    def __init__(self, meta: 'XbmImage.Meta', image: Image):
        self.meta = meta
        self.image = image

