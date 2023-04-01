class H3Error(Exception):
    """
    Дефолтная ошибка http
    """


class NoAvailablePushIDError(H3Error):
    """
    Нет ID
    """