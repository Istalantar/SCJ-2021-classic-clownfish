import numpy as np
from PIL import Image


class Images:
    def __init__(self, file: str,
                 cols: int = 80,
                 scale: float = 0.43,
                 resolution: int = 0,
                 shade_str: str = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\()1{}[]?-_+~<>i!lI;:,\"^`'.",
                 shade_min: str = "@#+-."):
        """
        Initiates the Images class while takes an image file and converts it into an Ascii image
        :param file: The image file path, allows .jpg, .jpeg, .png and other popular file formats
        Ascii related parameters =>
        :param cols: Number of columns in the ascii image, defaults to 80
        :param scale: defines the adjusted aspect ratio for the ascii image, defaults to 0.43
        :param resolution: defines resolution, takes in values as percentage of the highest resolution possible with
               characters from shade_str
               Special value: 0 (default) is interpreted as mode switch to minimalistic output with characters from
               shade_min
        :param shade_str: defaults to a well known pattern of 69 characters used to define the greyscale
        :param shade_min: defaults to a minimalistic pattern of 5 characters used to define the greyscale
        """
        # TODO: error handling when no file is selected
        self.file = file
        self.image = Image.open(file).convert("L")
        self.cols = cols
        self.scale = scale
        self.shade = {
            "str": shade_str,
            "str_len": len(shade_str),
            "min": shade_min,
            "min_len": len(shade_min),
            "length": 0,
            "resolution": 0
        }

        # ensure level is [0-100]
        resolution = 100 if resolution > 100 else 0 if resolution < 0 else resolution
        self.shade["resolution"] = resolution

    def __repr__(self) -> str:
        return f'<Images file={self.file} image={self.image}>'

    def __str__(self) -> str:
        return '\n'.join(self.img_to_ascii)

    def g_scale(self, resolution: int = 0) -> str:
        """
        Helper function to determine the character set based on the resolution
        :return: a string of characters which corresponds to the luminance in descending order
        """
        if resolution == 0:
            self.shade["length"] = self.shade["min_len"]
            return self.shade["min"]
        else:
            resolution = resolution * self.shade["str_len"] // 100
            # get evenly spaced indices and return them as a string
            ret_scale = ""
            indices = np.linspace(0, self.shade["str_len"] - 1, resolution, dtype=int)
            self.shade["length"] = len(indices)
            for i in indices:
                ret_scale += self.shade["str"][i]
            return ret_scale

    @staticmethod
    def get_average(image) -> float:
        """Given PIL Image, return average value of grayscale value (luminance)"""
        # get image as numpy array and get the shape, then returns the average
        im = np.array(image)
        w, h = im.shape
        return np.average(im.reshape(w * h))

    @property
    def img_to_ascii(self) -> str:

        # get the dimensions
        horizontal, vertical = self.image.size
        w = horizontal / self.cols

        # compute tile height based on aspect ratio and scale
        h = w / self.scale
        rows = int(vertical / h)

        # check if image size is too small
        if self.cols > horizontal or rows > vertical:
            print("Image too small for specified cols!")
            # TODO: better error handling here
            exit(0)

        aimg = []
        # generate list of dimensions
        for j in range(rows):
            y1 = int(j * h)
            y2 = int((j + 1) * h)
            if j == rows - 1:
                y2 = vertical
            aimg.append("")

            for i in range(self.cols):
                # crop image to tile
                x1 = int(i * w)
                x2 = int((i + 1) * w)
                if i == self.cols - 1:
                    x2 = horizontal

                # crop image to extract tile
                img = self.image.crop((x1, y1, x2, y2))
                # get average luminance
                avg = int(Images.get_average(img))
                # look up ascii char
                char = Images.g_scale(self, resolution=self.shade["resolution"])[
                    int((avg * (self.shade["length"] - 1)) / 255)]
                # append ascii char to string
                aimg[j] += char

        # return ascii image as a array/string
        return aimg
    
