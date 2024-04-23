import click
import json
import jsonschema


@click.group()
def cli():
    pass


@cli.command()
@click.argument('filename', type=click.Path())
@click.option('-d', '--destination', prompt='Destination',
              help='The destination of the flight')
@click.option('-n', '--number', prompt='Flight number',
              help='The flight number')
@click.option('-t', '--plane_type', prompt='Type of plane',
              help='The type of plane')
def add(filename, destination, number, plane_type):
    """Add a new flight"""
    flights = load_flights(filename)
    flights.append(
        {
            'destination': destination,
            'flight_number': number,
            'plane_type': plane_type
        }
    )
    save_flights(filename, flights)
    click.echo('Flight added successfully.')


@cli.command()
@click.argument('filename', type=click.Path())
def display(filename):
    """Display all flights"""
    flights = load_flights(filename)
    if flights:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 20
        )
        print(line)

        print(
            '| {:^4} | {:^30} | {:^20} | {:^20} |'.format(
                "No",
                "Пункт назначения",
                "Номер рейса",
                "Тип самолета"
            )
        )

        print(line)

        for idx, flight in enumerate(flights, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>20} |'.format(
                    idx,
                    flight.get('destination', ''),
                    flight.get('flight_number', ''),
                    flight.get('plane_type', '')
                )
            )
    else:
        click.echo("No flights available.")


@cli.command()
@click.argument('filename', type=click.Path())
@click.option('-f', '--plane_type', prompt='Type of plane',
              help='The type of plane to search for')
def find(filename, plane_type):
    """Find flights by plane type"""
    flights = load_flights(filename)
    found_flights = [
        flight for flight in flights if flight['plane_type'] == plane_type
        ]
    if found_flights:
        for flight in found_flights:
            click.echo(
                f"Destination: {flight['destination']}, "
                f"Flight number: {flight['flight_number']}, "
                f"Plane type: {flight['plane_type']}"
            )
    else:
        click.echo(f"No flights found for plane type '{plane_type}'.")


def save_flights(filename, flights):
    with open(filename, 'w') as f:
        json.dump(flights, f)


def load_flights(filename):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "flight_number": {"type": "string"},
                "plane_type": {"type": "string"}
            },
            "required": ["destination", "flight_number", "plane_type"]
        }
    }
    # Открыть файл с заданным именем для чтения.
    with open(filename, "r", encoding="utf-8") as fin:
        loaded = json.load(fin)
    try:
        jsonschema.validate(loaded, schema)
    except jsonschema.exceptions.ValidationError as e:
        print(">>> Error:")
        print(e.message)  # Ошибка валидацци будет выведена на экран
    return loaded


if __name__ == '__main__':
    cli()
