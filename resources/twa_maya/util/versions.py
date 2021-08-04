class VersionHandler(object):

    default_version = 1
    version_string = 'v'

    @staticmethod
    def _number_in_str(string):
        '''
        Find sequence of numbers in a string
            Parameters:
                string (str)
            Returns:
                (str): string containing the number in a string
        '''
        number = ''
        count = True
        for s in string:
            if count and s.isdigit():
                number += s
            else:
                count = False
        return number

    @staticmethod
    def _key_from_val(dictionary, value):
        '''
        Find key from value in a dictionary
            Parameters:
                dictionary (dict)
                string (str)
            Returns:
                (str): key
        '''
        for key, val in dictionary.items():
            if val == value:
                return key

    @classmethod
    def _split_version_string(cls, filename):
        '''
        Splits a filename string using version_string and keeps parts thats start with digits(potentially version numbers).
            Parameters:
                filename (str)
            Returns:
                (list): list of string parts
        '''
        return [s for s in filename.split(cls.version_string) if s[:1].isdigit()]

    @classmethod
    def find_version(cls, filename):
        '''
        Find the version of a file. If no version number or 0 return default_version
            Parameters:
                filename (str)
            Returns:
                (int): version number
        '''
        parts = cls._split_version_string(filename)
        if parts:
            version = int(cls._number_in_str(parts[0]))
        else:
            version = cls.default_version
        return version if version != 0 else cls.default_version

    @classmethod
    def version_name(cls, filename):
        '''
        Extract version name string from filename.
        foo_v01.bar >> v01
            Parameters:
                filename (str)
            Returns:
                (str): version name
                (None): if file has no version
        '''
        parts = cls._split_version_string(filename)
        if parts:
            version = cls._number_in_str(parts[0])
        else:
            return None
        return cls.version_string + version

    @classmethod
    def list_versions(cls, filelist):
        '''
        Return a dictionary "filename: (int)version" from list of files
            Parameters:
                filelist (list)
            Returns:
                (dict): dictionary of files and versions
        '''
        filedict = {}
        for file in filelist:
            if isinstance(file, str):
                filedict[file] = cls.find_version(file)
        return filedict

    @classmethod
    def latest_version(cls, filelist, filter=None):
        '''
        Return latest version of a file form list of files.
            Parameters:
                filelist (list)
                filter (str): filter the filelist. Ff file contains filter
            Returns:
                (tuple): filename, version
        '''
        if filter and isinstance(filter, str):
            filelist = [f for f in filelist if filter in f]
        filedict = cls.list_versions(filelist)
        latest = max(filedict.values())
        return (cls._key_from_val(filedict, latest), latest)
