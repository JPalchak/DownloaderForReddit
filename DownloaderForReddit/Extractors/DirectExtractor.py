"""
Downloader for Reddit takes a list of reddit users and subreddits and downloads content posted to reddit either by the
users or on the subreddits.


Copyright (C) 2017, Kyle Hickey


This file is part of the Downloader for Reddit.

Downloader for Reddit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Downloader for Reddit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Downloader for Reddit.  If not, see <http://www.gnu.org/licenses/>.
"""


from Extractors.BaseExtractor import BaseExtractor


class DirectExtractor(BaseExtractor):

    url_key = None

    def __init__(self, post, reddit_object, content_display_only=False):
        super().__init__(post, reddit_object, content_display_only)

    def extract_content(self):
        domain, id_with_ext = self.url.rsplit('/', 1)
        image_id, extension = id_with_ext.rsplit('.', 1)
        file_name = self.post_title if self.name_downloads_by == 'Post Title' else image_id
        self.make_content(self.url, file_name, extension)