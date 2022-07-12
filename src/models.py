

class Cookie:
    """
    Class for storing the cookie temporarily.
        absolute_path: Netscape formatted file to read cookies from and dump cookie jar in
        cookie_data: String of cookie data. (We might  persist this if the user deletes the original file)
    """
    absolute_file_path: str
    cookie_data: str
