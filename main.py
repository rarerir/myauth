import psycopg, django


class Database:
    def __init__(self, password) -> None:
        self.CONNECTION = psycopg.connect("user='admin' password='rar'")
        self.CURSOR = self.CONNECTION.cursor()


    def connect(self) -> None | str:
        psycopg.connect(**self.__dict__)
        return

    def disconnect(self) -> None | str:
        return

    def execute(self, query) -> None | str:
        return

    def check(self) -> bool:
        return True
