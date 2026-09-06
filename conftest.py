import pytest

from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


@pytest.fixture
def collector_with_two_books():
    collector = BooksCollector()
    collector.add_new_book('Гордость и предубеждение и зомби')
    collector.add_new_book('Что делать, если ваш кот хочет вас убить')
    return collector


@pytest.fixture
def collector_with_genres():
    collector = BooksCollector()
    books = {
        'Гордость и предубеждение и зомби': 'Ужасы',
        'Шерлок Холмс': 'Детективы',
        'Незнайка на Луне': 'Мультфильмы',
        'Марсианин': 'Фантастика',
        'Двенадцать стульев': 'Комедии',
    }
    for name, genre in books.items():
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
    return collector
