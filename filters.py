def high_rating_filter():
    return "Rating >= 8"


def film_for_children_filter():
    return "(Certificate == \'G\' OR " \
           "Certificate == \'PG\' OR " \
           "Certificate == \'TV-PG\' OR " \
           "Certificate == \'PG-13\' OR " \
           "Certificate == \'U\')"


def film_for_adults_filter():
    return "(Certificate == \'R\' OR " \
           "Certificate == \'A\')"


def runtime_filter(index):
    if index == 1:
        return "Runtime < 120"
    if index == 2:
        return "Runtime >= 120 AND Runtime <= 180"
    if index == 3:
        return "Runtime > 180"


def year_filter(index):
    if index == 1:
        return "Year < 1980"
    if index == 2:
        return "Year >= 1980 AND Year <= 1989"
    if index == 3:
        return "Year >= 1990 AND Year <= 1999"
    if index == 4:
        return "Year >= 2000 AND Year <= 2009"
    if index == 5:
        return "Year >= 2010"


def dataframe_date_filter(genre):
    return "Genres LIKE \'%" + genre + "%\'"


def director_filter(director):
    return "Director LIKE \'%" + director + "%\'"


def actor_filter(actor):
    return "Stars LIKE \'%" + actor + "%\'"

