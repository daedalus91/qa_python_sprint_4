from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test

class TestBooksCollector:

    def test_init_collections_are_empty_and_genres_filled(self, collector):
        get_empty_books_genre = collector.get_books_genre()
        get_empty_favorites_books = collector.get_list_of_favorites_books()
        get_empty_genre = collector.genre
        get_empty_genre_age_rating = collector.genre_age_rating
        assert get_empty_books_genre == {}
        assert get_empty_favorites_books == []
        assert get_empty_genre == ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        assert get_empty_genre_age_rating == ['Ужасы', 'Детективы']

    def test_add_new_book_add_two_books_added_with_empty_genre(self, collector_with_two_books):
        books_genre = collector_with_two_books.get_books_genre()
        assert len(books_genre) == 2
        assert list(books_genre.values()) == ['', '']

    @pytest.mark.parametrize(
        'name',
        [
            'А',                # 1 символ — минимальная граница
            'А' * 39,           # 39 символов
            'А' * 40,           # 40 символов — максимальная граница
        ],
        ids=['1_symbol', '39_symbols', '40_symbols']
    )
    def test_add_new_book_valid_name_length_book_added(self, collector, name):
        collector.add_new_book(name)
        assert name in collector.get_books_genre()

    @pytest.mark.parametrize(
        'name',
        [
            '',                 # пустое имя
            'А' * 41,           # 41 символ — за границей
            'А' * 100,
        ],
        ids=['empty_name', '41_symbols', '100_symbols']
    )
    def test_add_new_book_invalid_name_length_book_not_added(self, collector, name):
        collector.add_new_book(name)
        assert collector.get_books_genre() == {}

    def test_add_new_book_same_book_twice_added_once(self, collector):
        collector.add_new_book('Марсианин')
        collector.add_new_book('Марсианин')
        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_existing_book_with_genre_genre_not_reset(self, collector):
        collector.add_new_book('Марсианин')
        collector.set_book_genre('Марсианин', 'Фантастика')
        collector.add_new_book('Марсианин')
        assert collector.get_book_genre('Марсианин') == 'Фантастика'

    @pytest.mark.parametrize(
        'genre',
        ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
    )
    def test_set_book_genre_valid_genre_genre_set(self, collector, genre):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', genre)
        assert collector.get_book_genre('Книга') == genre

    @pytest.mark.parametrize(
        'genre',
        ['Роман', 'фантастика', '', 'Драма'], 
        ids=['unknown_genre', 'wrong_case', 'empty_genre', 'drama'] ) 
    def test_set_book_genre_genre_not_in_list_genre_not_set(self, collector, genre):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', genre)
        assert collector.get_book_genre('Книга') == ''
    
    def test_set_book_genre_book_not_in_dict_book_not_added(self, collector):
        collector.set_book_genre('Неизвестная книга', 'Ужасы')
        assert collector.get_books_genre() == {}

    def test_set_book_genre_change_genre_genre_updated(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Ужасы')
        collector.set_book_genre('Книга', 'Комедии')
        assert collector.get_book_genre('Книга') == 'Комедии'

    def test_get_book_genre_existing_book_returns_genre(self, collector_with_genres):
        get_books_genre = collector_with_genres.get_book_genre('Шерлок Холмс')
        assert get_books_genre == 'Детективы'

    def test_get_book_genre_unknown_book_returns_none(self, collector):
        get_book_genre = collector.get_book_genre('Нет такой книги')
        assert get_book_genre is None

    def test_get_books_with_specific_genre_two_books_one_genre_returns_both(self, collector):
        collector.add_new_book('Марсианин')
        collector.set_book_genre('Марсианин', 'Фантастика')
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.add_new_book('Шерлок Холмс')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')

        assert collector.get_books_with_specific_genre('Фантастика') == ['Марсианин', 'Дюна']

    def test_get_books_with_specific_genre_no_books_with_genre_returns_empty_list(self, collector_with_two_books):
        get_books_with_specific_genre = collector_with_two_books.get_books_with_specific_genre('Комедии')
        assert get_books_with_specific_genre == []

    def test_get_books_with_specific_genre_invalid_genre_returns_empty_list(self, collector_with_genres):
        get_books_with_specific_genre = collector_with_genres.get_books_with_specific_genre('Роман')
        assert get_books_with_specific_genre == []

    def test_get_books_with_specific_genre_empty_collector_returns_empty_list(self, collector):
        get_books_with_specific_genre = collector.get_books_with_specific_genre('Ужасы')
        assert get_books_with_specific_genre == []

    def test_get_books_genre_returns_dict_with_books_and_genres(self, collector):
        collector.add_new_book('Марсианин')
        collector.set_book_genre('Марсианин', 'Фантастика')
        assert collector.get_books_genre() == {'Марсианин': 'Фантастика'}

    def test_get_books_for_children_returns_only_books_without_age_rating(self, collector_with_genres):
        get_books_for_children = collector_with_genres.get_books_for_children()
        assert get_books_for_children == [
            'Незнайка на Луне', 'Марсианин', 'Двенадцать стульев'
        ]

    def test_get_books_for_children_book_without_genre_not_in_list(self, collector_with_two_books):
        get_books_for_children = collector_with_two_books.get_books_for_children()
        assert get_books_for_children == []

    @pytest.mark.parametrize('genre', ['Ужасы', 'Детективы'])
    def test_get_books_for_children_age_rating_genre_not_in_list(self, collector, genre):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', genre)
        assert collector.get_books_for_children() == []

    def test_get_books_for_children_empty_collector_returns_empty_list(self, collector):
        get_books_for_children = collector.get_books_for_children()
        assert get_books_for_children == []

    def test_add_book_in_favorites_book_from_dict_added(self, collector_with_two_books):
        collector_with_two_books.add_book_in_favorites('Гордость и предубеждение и зомби')
        assert collector_with_two_books.get_list_of_favorites_books() == ['Гордость и предубеждение и зомби']

    def test_add_book_in_favorites_same_book_twice_added_once(self, collector_with_two_books):
        collector_with_two_books.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector_with_two_books.add_book_in_favorites('Гордость и предубеждение и зомби')
        assert len(collector_with_two_books.get_list_of_favorites_books()) == 1

    def test_add_book_in_favorites_book_not_in_dict_not_added(self, collector):
        collector.add_book_in_favorites('Неизвестная книга')
        assert collector.get_list_of_favorites_books() == []

    def test_add_book_in_favorites_two_different_books_both_added(self, collector_with_two_books):
        collector_with_two_books.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector_with_two_books.add_book_in_favorites('Что делать, если ваш кот хочет вас убить')
        assert len(collector_with_two_books.get_list_of_favorites_books()) == 2

    def test_delete_book_from_favorites_existing_book_deleted(self, collector_with_two_books):
        collector_with_two_books.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector_with_two_books.delete_book_from_favorites('Гордость и предубеждение и зомби')
        assert collector_with_two_books.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_book_not_in_favorites_list_not_changed(self, collector_with_two_books):
        collector_with_two_books.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector_with_two_books.delete_book_from_favorites('Что делать, если ваш кот хочет вас убить')
        assert collector_with_two_books.get_list_of_favorites_books() == ['Гордость и предубеждение и зомби']

    def test_delete_book_from_favorites_book_stays_in_books_genre(self, collector_with_two_books):
        collector_with_two_books.add_book_in_favorites('Гордость и предубеждение и зомби')
        collector_with_two_books.delete_book_from_favorites('Гордость и предубеждение и зомби')
        assert 'Гордость и предубеждение и зомби' in collector_with_two_books.get_books_genre()

    def test_get_list_of_favorites_books_empty_by_default(self, collector):
        get_list_of_favorites_books = collector.get_list_of_favorites_books()
        assert get_list_of_favorites_books == []

    def test_get_list_of_favorites_books_returns_added_books(self, collector_with_genres):
        collector_with_genres.add_book_in_favorites('Марсианин')
        collector_with_genres.add_book_in_favorites('Шерлок Холмс')
        assert collector_with_genres.get_list_of_favorites_books() == ['Марсианин', 'Шерлок Холмс']
        
