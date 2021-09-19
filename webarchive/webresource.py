"""WebResource class implementation."""

from .util import make_data_uri, process_style_sheet


__all__ = ["WebResource"]


class WebResource(object):
    """An individual resource within a WebArchive.

    WebResource objects are created by their parent WebArchive as it
    processes the .webarchive file's contents. This class is not meant
    to be instantiated directly by users.
    """

    # WebResourceData
    # WebResourceMIMEType
    # WebResourceTextEncodingName
    # WebResourceURL
    # WebResourceFrameName

    __slots__ = ["_archive", "_data", "_mime_type", "_url",
                 "_text_encoding", "_frame_name"]

    def __init__(self, archive, plist_data):
        """Return a new WebResource object."""

        # The parent WebArchive
        self._archive = archive

        # Required attributes
        self._data = plist_data["WebResourceData"]
        self._mime_type = plist_data["WebResourceMIMEType"]
        self._url = plist_data["WebResourceURL"]

        # Text encoding (not present for all WebResources)
        if "WebResourceTextEncodingName" in plist_data:
            self._text_encoding = plist_data["WebResourceTextEncodingName"]
            self._text_encoding = self._text_encoding.lower()
        elif self._mime_type.startswith("text/"):
            # Fall back on UTF-8 for text resources
            self._text_encoding = "utf-8"
        else:
            # No encoding specified or needed
            self._text_encoding = None

        # Frame name (not present for all WebResources)
        if "WebResourceFrameName" in plist_data:
            self._frame_name = plist_data["WebResourceFrameName"]
        else:
            self._frame_name = None

    def __bytes__(self):
        """Return this resource's data as bytes."""

        return bytes(self._data)

    def __str__(self):
        """Return this resource's data as a printable string.

        This is only available for text resources (i.e., those whose MIME
        type starts with "text/"), and will raise a TypeError for other
        resources that cannot be reliably converted to strings.
        """

        if self.mime_type.startswith("text/"):
            return str(self._data, encoding=self._text_encoding)

        else:
            raise TypeError("cannot convert non-text resource to str")

    def to_data_uri(self):
        """Return a data URI corresponding to this subresource's content."""

        if self.url == self.archive.main_resource.url:
            # This is the archive's main resource.
            # Embed subresources recursively using data URIs.
            #
            # N.B. Comparing the URL is the quickest way to check this, but
            # assumes a well-formed webarchive where the URL field is unique.
            data = bytes(self.archive.to_html(), encoding=self._text_encoding)

        elif self.mime_type == "text/css":
            # This is a style sheet.
            # Embed external content recursively using data URIs.
            content = process_style_sheet(self, self._archive.subresources)
            data = bytes(content, encoding=self._text_encoding)

        else:
            data = self._data

        return make_data_uri(self._mime_type, data)

    @property
    def archive(self):
        """This resource's parent WebArchive."""

        return self._archive

    @property
    def data(self):
        """This resource's data."""

        return self._data

    @property
    def mime_type(self):
        """MIME type of this resource's data."""

        return self._mime_type

    @property
    def url(self):
        """Original URL of this resource."""

        return self._url

    @property
    def text_encoding(self):
        """Text encoding of this resource's data."""

        return self._text_encoding

    @property
    def frame_name(self):
        """This resource's frame name."""

        return self._frame_name
