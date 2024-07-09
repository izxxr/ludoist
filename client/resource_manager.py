# MIT License

# Copyright (c) 2024 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import Dict, Union, Optional, TYPE_CHECKING
from pyglet import image, resource

import os

if TYPE_CHECKING:
    from client.window import LudoistWindow

__all__ = (
    "ResourceManager",
)

ResourceT = Union[image.Texture, image.TextureRegion]


class ResourceManager:
    """The resources manager.

    This class stores and manages various resources (images, sounds etc.)
    used by the client window.
    """
    def __init__(self, resources_dir: str, window: LudoistWindow):
        self._window = window
        self._resources_dir = resources_dir
        self._resources: Dict[str, ResourceT] = {}
        self._load()

    def _rsrcimage(self, name: str) -> Union[image.Texture, image.TextureRegion]:
        path = self._resources_dir + "/" + name
        return resource.image(path)

    def _load(self) -> None:
        for filename in os.listdir(self._resources_dir):
            if filename.endswith(".png"):
                name = filename.replace(".png", "")
                self._resources.setdefault(name, self._rsrcimage(filename))

    def get(self, name: str, width: Optional[int] = None, height: Optional[int] = None) -> ResourceT:
        """Get a resource by its name."""
        try:
            resource = self._resources[name]
        except KeyError:
            raise RuntimeError("invalid resource") from None
        else:
            if width:
                resource.width = width
            if height:
                resource.height = height
            return resource
