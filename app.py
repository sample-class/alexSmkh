from flask import Flask, render_template, abort
import data

app = Flask(__name__)


@app.context_processor
def context_processor():
    return {
        'tours': data.TOURS,
        'title': data.TITLE,
        'subtitle': data.SUBTITLE,
        'description': data.DESCRIPTION,
        'departures': data.DEPARTURES,
    }


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/from/<departure>')
def direction(departure):
    if not data.DEPARTURES.get(departure):
        abort(404)

    tours_for_departure = list(
        filter(
            lambda tour: tour.get('departure') == departure,
            data.TOURS
        )
    )
    if tours_for_departure:
        tours_info = {
            'number_of_tours': len(tours_for_departure),
            'max_price': max(tours_for_departure, key=lambda x: x['price']).get('price'),
            'min_price': min(tours_for_departure, key=lambda x: x['price']).get('price'),
            'min_number_of_nights': min(tours_for_departure, key=lambda x: x['nights']).get('nights'),
            'max_number_of_nights': max(tours_for_departure, key=lambda x: x['nights']).get('nights'),
        }
    else:
        tours_info = {}

    context = {
        'departure': data.DEPARTURES.get(departure).split(' ')[1],
        'tours_for_departure': tours_for_departure,
        'tours_info': tours_info
    }
    return render_template('from.html', **context)


@app.route('/tours/<int:tour_id>')
def tours(tour_id):
    tour = next((tour for tour in data.TOURS if tour['id'] == tour_id), None)

    if tour is None:
        abort(404)

    context = {
        'tour': tour,
    }

    return render_template('tours.html', **context)


@app.errorhandler(404)
def not_found(error):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"


if __name__ == '__main__':
    app.run()