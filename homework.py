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

    def add_record(self, record):
        """Сохранение новой записи о расходах/приёме пищи.
        Метод принимает объект класса Record и сохраняет его в списке records.
        """

        self.records.append(record)

    def get_today_stats(self):
        """Сколько сегодня кКал получено/денег потрачено."""

        today = dt.date.today()
        total = sum(
            [
                record.amount for record in self.records
                if record.date == today
            ]
        )
        return total

    def get_week_stats(self):
        """Сколько кКал получено/денег потрачено за последние 7 дней."""

        today = dt.date.today()
        week_ago = today - dt.timedelta(days=7)

        total = sum(
            [
                record.amount for record in self.records
                if week_ago <= record.date <= today
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

        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    """Подкласс класса Calculator.
    Добавленный метод - определение, сколько кКал ёще можно получить сегодня.
    """

    def get_calories_remained(self):
        """Сколько ещё кКал можно/нужно получить сегодня."""

        remain = self.today_remain()
        if remain > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {remain} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Подкласс класса Calculator.
    Добавленный метод - информация о дневном балансе.
    """

    USD_RATE = 70.8800
    EURO_RATE = 80.4134

    @staticmethod
    def raise_unsupported_currency(currency):
        """Вызов исключения для неподдерживаемой валюты"""
        raise ValueError(f'{currency} is not supported') from Exception

    def get_today_cash_remained(self, currency):
        """Возвращение сообщения о состоянии дневного баланса."""

        currencies = ('rub', 'usd', 'eur')

        if currency.lower() not in currencies:
            self.raise_unsupported_currency(currency)

        if currency.lower() in currencies:
            remain = self.today_remain()

            if remain == 0:
                return 'Денег нет, держись'

            which_currency = {
                'rub': (remain, 'руб'),
                'usd': (remain / self.USD_RATE, 'USD'),
                'eur': (remain / self.EURO_RATE, 'Euro')
            }
            money_amount, currency_code = which_currency[currency]
            money_amount = abs(round(money_amount, 2))

            if remain > 0:
                return f'На сегодня осталось {money_amount} {currency_code}'

            return ('Денег нет, держись: твой долг - '
                    f'{money_amount} {currency_code}')
