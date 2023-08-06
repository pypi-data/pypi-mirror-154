from sqlalchemy import create_engine, Table, Column, Integer, String, Text, \
    MetaData, DateTime
from sqlalchemy.orm import mapper, sessionmaker
import datetime
from sqlalchemy.sql import default_comparator


class ClientDatabase:
    """База данных клиента"""

    class KnownUsers:
        """Отображение таблицы известных пользователей."""

        def __init__(self, user):
            self.id = None
            self.username = user

    class MessageStat:
        """Отображение таблицы статистики переданных сообщений"""

        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    class Contacts:
        """Отображение списка контактов"""

        def __init__(self, contact):
            self.id = None
            self.name = contact

    def __init__(self, name):
        # Создаём движок базы данных, поскольку разрешено несколько клиентов
        # одновременно, каждый должен иметь свою БД
        # Поскольку клиент мультипоточный необходимо отключить проверки
        # на подключения с разных потоков,
        # иначе sqlite3.ProgrammingError
        self.database_engine = create_engine(
            f'sqlite:///{name}',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})
        # Создаём объект MetaData
        self.metadata = MetaData()

        # Создаём таблицу известных пользователей
        users = Table('known_users', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('username', String))

        # Создаём таблицу истории сообщений
        history = Table('message_history', self.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('contact', String),
                        Column('direction', String),
                        Column('message', Text),
                        Column('date', DateTime))

        # Создаём таблицу контактов
        contacts = Table('contacts', self.metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String, unique=True))

        # Создаём таблицы
        self.metadata.create_all(self.database_engine)

        # Создаём отображения
        mapper(self.KnownUsers, users)
        mapper(self.MessageStat, history)
        mapper(self.Contacts, contacts)

        # Создаём сессию
        self.session = sessionmaker(bind=self.database_engine)()

        # Необходимо очистить таблицу контактов, т.к. при запуске они
        # подгружаются с сервера.
        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """Добавление контакта."""
        if not self.session.query(
                self.Contacts).filter_by(
            name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def contacts_clear(self):
        '''Очищение таблицы со списком контактов.'''
        self.session.query(self.Contacts).delete()

    def del_contact(self, contact):
        """Удаление контакта."""
        self.session.query(self.Contacts).filter_by(name=contact).delete()

    def add_users(self, users_list):
        """Добавление известных пользователей.
        Пользователи получаются только с сервера, поэтому таблица очищается."""
        self.session.query(self.KnownUsers).delete()
        for user in users_list:
            user_row = self.KnownUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, from_user, to_user, message):
        """Сохранение сообщений"""
        message_row = self.MessageStat(from_user, to_user, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """Получить контакты"""
        return [contact[0]
                for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """Список известных пользователей"""
        return [user[0]
                for user in self.session.query(self.KnownUsers.username).all()]

    def check_user(self, user):
        """Наличие пользователя в известных"""
        return bool(
            self.session.query(
                self.KnownUsers).filter_by(
                username=user).count())

    def check_contact(self, contact):
        """Наличие пользователя в контактах"""
        return bool(
            self.session.query(
                self.Contacts).filter_by(
                name=contact).count())

    def get_history(self, contact):
        """История переписки"""
        query = self.session.query(self.MessageStat).filter_by(contact=contact)
        return [(history_row.contact,
                 history_row.direction,
                 history_row.message,
                 history_row.date) for history_row in query.all()]


if __name__ == '__main__':
    test_db = ClientDatabase('databases/db_test1.db3')
    for i in ['test3', 'test4', 'test5']:
        test_db.add_contact(i)
    test_db.add_contact('test4')
    test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
    test_db.save_message(
        'test1',
        'test2',
        f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
    test_db.save_message(
        'test2',
        'test1',
        f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
    print(test_db.get_contacts())
    print(test_db.get_users())
    print(test_db.check_user('test1'))
    print(test_db.check_user('test10'))
    print(test_db.get_history('test2'))
    print(test_db.get_history(to_who='test2'))
    print(test_db.get_history('test3'))
    test_db.del_contact('test4')
    print(test_db.get_contacts())
