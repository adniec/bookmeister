from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    name: str
    value: str
    range_min: int
    range_max: int

    def is_length_correct(self, value):
        return self.range_min <= len(value) <= self.range_max


VALUES = (
    Record('Title', 'From Russia, with Love', 1, 50),
    Record('Author', 'Ian Fleming', 3, 50),
    Record('Type', 'Thriller', 3, 20),
    Record('Publisher', 'Thomas & Mercer', 1, 30),
    Record('ISBN', '9781612185477', 13, 13),
    Record('Release', '2012', 4, 4),
    Record('Language', 'EN', 2, 2),
    Record('Pages', '181', 1, 4),
    Record('Quantity', '10', 1, 100)
)
