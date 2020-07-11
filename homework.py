import datetime as dt


class Calculator:

    def __init__(self, limit):
        """Общая функциональность подклассов Calories и CashCalculator.
        Свойства класса Calculator:
        - число limit (заданный дневной лимит трат/кКал);
        - пустой список record (хранение записей).
        """

        self.limit = limit
        self.records = []
        self.today = dt.date.today()

    def add_record(self, record):
        """Сохранение новой записи о расходах/приёме пищи.
        Метод принимает объект класса Record и сохраняет его в списке records.
        """

        self.records.append(record)

    def get_today_stats(self):
        """Сколько сегодня кКал получено/денег потрачено."""

        total = sum(
            [
                record.amount for record in self.records
                if record.date == self.today
            ]
        )
        return total

    def get_week_stats(self):
        """Сколько кКал получено/денег потрачено за последние 7 дней."""

        week_ago = self.today - dt.timedelta(days=7)
        total = sum(
            [
                record.amount for record in self.records
                if week_ago <= record.date <= self.today
            ]
        )
        return total

    def today_remain(self):
        return self.limit - self.get_today_stats()


class Record:
    """Создание записей.
    Свойства экземпляров класса:
    - число amount (денежная сумма или количество килокалорий);
    - дата создания записи date (передаётся в явном виде в конструктор,
    либо присваивается значение по умолчанию — текущая дата);
    - комментарий comment (на что потрачены деньги или откуда взялись кКал).
    """

    def __init__(self, amount, comment, date=None):
        """Подкласс класса Calculator.
         Добавленный метод - определение, сколько кКал ёще можно получить
        сегодня.
        """

        self.amount = amount
        self.comment = comment
        self.today = dt.date.today()

        if date is None:
            self.date = self.today
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class CaloriesCalculator(Calculator):
    """Подкласс класса Calculator.
    Добавленный метод - определение, сколько кКал ёще можно получить сегодня.
    """

    def get_calories_remained(self):
        """Сколько ещё кКал можно/нужно получить сегодня."""

        remain = self.today_remain()
        if remain > 0:
            string = (
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {remain} кКал'
            )
            return string
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Подкласс класса Calculator.
    Добавленный метод - информация о дневном балансе.
    """

    USD_RATE = 70.8800
    EURO_RATE = 80.4134

    def get_today_cash_remained(self, currency):
        """Возвращение сообщения о состоянии дневного баланса."""

        currencies = ('rub', 'usd', 'eur')

        if currency.lower() in currencies:

            remain = self.today_remain()
            values = (
                (abs(round(remain, 2)), 'руб'),
                (abs(round(remain / self.USD_RATE, 2)), 'USD'),
                (abs(round(remain / self.EURO_RATE, 2)), 'Euro')
            )

            which_currency = dict(zip(currencies, values))
            money_amount, currency_code = which_currency[currency]

            if remain == 0:
                return 'Денег нет, держись'

            elif remain > 0:
                return f'На сегодня осталось {money_amount} {currency_code}'

            elif remain < 0:
                string = (
                    'Денег нет, держись: твой долг - '
                    f'{money_amount} {currency_code}'
                )
                return string
        else:
            raise ValueError('This is not a supported currency') from Exception
