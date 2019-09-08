from .constants import months
from .models import Movie, Rating
from .request_handler import RequestHandler


def get_movie_data_by_title(title):
    """
    Make request for movie data via RequestHandler.
    :param title: str
    :return: dict
    """
    handler = RequestHandler()
    return handler.request(title=title)


def create_movie_object(data):
    """
    Prepare dictionaries with data
    and create movie object from provided data.
    :param data: dict
    :return: Movie object
    """
    data, ratings = prepare_movie_data(data)
    movie, created = Movie.objects.update_or_create(
        title=data['title'],
        defaults=data
    )
    create_rating_object(ratings, movie)
    return movie


def prepare_movie_data(data):
    """
    Prepare provided movie data for upload to database.
    :param data: dict
    :return: dict, dict
    """

    data = lowercase_dict_keys(data)
    if 'ratings' in data:
        ratings = data.get('ratings')
        del data['ratings']

    data = remove_not_applicable_from_data(data)
    if data.get('type', None):
        #  Change key name to non build-in name
        data['typee'] = data.pop('type')

    if data.get('released', None) == '':
        del data['released']

    if data.get('released', None):
        data['released'] = format_date(data['released'])

    if data.get('dvd', None):
        data['dvd'] = format_date(data['dvd'])

    if data.get('imdbvotes', None):
        data['imdbvotes'] = data['imdbvotes'].replace(',', '')

    prepared_ratings = []
    for rate in ratings:
        prepared_ratings.append(lowercase_dict_keys(rate))
    return data, prepared_ratings


def create_rating_object(data, movie):
    """
    Create rating objects from provided data.
    :param data: dict
    :param movie: Movie object
    :return: list
    """
    ratings = []
    for rating in data:
        rating['movie'] = movie
        rating_obj = Rating.objects.update_or_create(
            movie=rating['movie'],
            source=rating['source'],
            defaults=rating
        )
        ratings.append(rating_obj)
    return ratings


def lowercase_dict_keys(data):
    """
    Lowercase all keys in provided dict.
    :param data: dict
    :return: dict
    """
    return dict((key.lower(), value) for key, value in data.items())


def remove_not_applicable_from_data(data):
    """
    Remove all 'N/A' values from movie data.
    :param data: dict
    :return: dict
    """
    return dict((key, value.replace('N/A', '')) for key, value in data.items())


def format_date(data):
    """
    Format provided string date to database acceptable format.
    DD-MMM-RRRR -> RRRR-MM-DD
    :param data: str
    :return: str
    """
    month = months[data[3:6]]
    date = f'{int(data[7:11])}-{month}-{int(data[0:2])}'
    return date


def calculate_rank(queryset):
    """
    Calculate and additional field to objects in queryset with rank value.
    :param queryset: Queryset of Movie objects
    :return: Queryset of Movie objects
    """
    total_comments = set(list(queryset.values_list('total_comments', flat=True)))
    top_total_comments = sorted(total_comments, reverse=True)
    for obj in queryset:
        obj.rank = top_total_comments.index(obj.total_comments) + 1  # Ranking starts from 1
    return queryset
