import re
from kolibri.data.kolibri_data import FileSystemPathPointer, PathPointer, ZipFilePathPointer


class ResourceReader:
    """
    A base class for "resource reader" classes, each of which can be
    used to read a specific resource format.  Each individual resource
    reader instance is used to read a specific resource, consisting of
    one or more files under a common root directory.  Each file is
    identified by its ``file identifier``, which is the relative path
    to the file from the root directory.

    A separate subclass is defined for each resource format.  These
    subclasses define one or more methods that provide 'views' on the
    resource contents, such as ``words()`` (for a list of words) and
    ``parsed_sents()`` (for a list of parsed sentences).  Called with
    no arguments, these methods will return the contents of the entire
    resource.  For most corpora, these methods define one or more
    selection arguments, such as ``fileids`` or ``categories``, which can
    be used to select which portion of the resource should be returned.
    """

    def __init__(self, root, fileids, encoding="utf8", tagset=None):
        """
        :type root: PathPointer or str
        :param root: A path pointer identifying the root directory for
            this resource.  If a string is specified, then it will be
            converted to a ``PathPointer`` automatically.
        :param fileids: A list of the files that make up this resource.
            This list can either be specified explicitly, as a list of
            strings; or implicitly, as a regular expression over file
            paths.  The absolute path for each file will be constructed
            by joining the reader's root to each file name.
        :param encoding: The default unicode encoding for the files
            that make up the resource.  The value of ``encoding`` can be any
            of the following:

            - A string: ``encoding`` is the encoding name for all files.
            - A dictionary: ``encoding[file_id]`` is the encoding
              name for the file whose identifier is ``file_id``.  If
              ``file_id`` is not in ``encoding``, then the file
              contents will be processed using non-unicode byte strings.
            - A list: ``encoding`` should be a list of ``(regexp, encoding)``
              tuples.  The encoding for a file whose identifier is ``file_id``
              will be the ``encoding`` value for the first tuple whose
              ``regexp`` matches the ``file_id``.  If no tuple's ``regexp``
              matches the ``file_id``, the file contents will be processed
              using non-unicode byte strings.
            - None: the file contents of all files will be
              processed using non-unicode byte strings.
        :param tagset: The name of the tagset used by this resource, to be used
              for normalizing or converting the POS tags returned by the
              ``tagged_...()`` methods.
        """
        # Convert the root to a path pointer, if necessary.
        if isinstance(root, str) and not isinstance(root, PathPointer):
            m = re.match(r"(.*\.zip)/?(.*)$|", root)
            zipfile, zipentry = m.groups()
            if zipfile:
                root = ZipFilePathPointer(zipfile, zipentry)
            else:
                root = FileSystemPathPointer(root)
        elif not isinstance(root, PathPointer):
            raise TypeError("resourceReader: expected a string or a PathPointer")

        self._fileids = fileids
        """A list of the relative paths for the fileids that make up
        this resource."""

        self._root = root
        """The root directory for this resource."""

        # If encoding was specified as a list of regexps, then convert
        # it to a dictionary.
        if isinstance(encoding, list):
            encoding_dict = {}
            for fileid in self._fileids:
                for x in encoding:
                    (regexp, enc) = x
                    if re.match(regexp, fileid):
                        encoding_dict[fileid] = enc
                        break
            encoding = encoding_dict

        self._encoding = encoding
        """The default unicode encoding for the fileids that make up
           this resource.  If ``encoding`` is None, then the file
           contents are processed using byte strings."""
        self._tagset = tagset

    def __repr__(self):
        if isinstance(self._root, ZipFilePathPointer):
            path = f"{self._root.zipfile.filename}/{self._root.entry}"
        else:
            path = "%s" % self._root.path
        return f"<{self.__class__.__name__} in {path!r}>"

    def ensure_loaded(self):
        """
        Load this resource (if it has not already been loaded).  This is
        used by LazyresourceLoader as a simple method that can be used to
        make sure a resource is loaded -- e.g., in case a user wants to
        do help(some_resource).
        """
        pass  # no need to actually do anything.

    def fileids(self):
        """
        Return a list of file identifiers for the fileids that make up
        this resource.
        """
        return self._fileids

    def abspath(self, fileid):
        """
        Return the absolute path for the given file.

        :type fileid: str
        :param fileid: The file identifier for the file whose path
            should be returned.
        :rtype: PathPointer
        """
        return self._root.join(fileid)

    def abspaths(self, fileids=None, include_encoding=False, include_fileid=False):
        """
        Return a list of the absolute paths for all fileids in this resource;
        or for the given list of fileids, if specified.

        :type fileids: None or str or list
        :param fileids: Specifies the set of fileids for which paths should
            be returned.  Can be None, for all fileids; a list of
            file identifiers, for a specified set of fileids; or a single
            file identifier, for a single file.  Note that the return
            value is always a list of paths, even if ``fileids`` is a
            single file identifier.

        :param include_encoding: If true, then return a list of
            ``(path_pointer, encoding)`` tuples.

        :rtype: list(PathPointer)
        """
        if fileids is None:
            fileids = self._fileids
        elif isinstance(fileids, str):
            fileids = [fileids]

        paths = [self._root.join(f) for f in fileids]

        if include_encoding and include_fileid:
            return list(zip(paths, [self.encoding(f) for f in fileids], fileids))
        elif include_fileid:
            return list(zip(paths, fileids))
        elif include_encoding:
            return list(zip(paths, [self.encoding(f) for f in fileids]))
        else:
            return paths

    def open(self, file):
        """
        Return an open stream that can be used to read the given file.
        If the file's encoding is not None, then the stream will
        automatically decode the file's contents into unicode.

        :param file: The file identifier of the file to read.
        """
        encoding = self.encoding(file)
        stream = self._root.join(file).open(encoding)
        return stream

    def encoding(self, file):
        """
        Return the unicode encoding for the given resource file, if known.
        If the encoding is unknown, or if the given file should be
        processed using byte strings (str), then return None.
        """
        if isinstance(self._encoding, dict):
            return self._encoding.get(file)
        else:
            return self._encoding

    def _get_root(self):
        return self._root

    root = property(
        _get_root,
        doc="""
        The directory where this resource is stored.

        :type: PathPointer""",
    )
