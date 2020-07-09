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

        total = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                total += record.amount

        return total

    def get_week_stats(self):
        """Сколько кКал получено/денег потрачено за последние 7 дней."""

        now = dt.datetime.now().date()
        week_ago = now - dt.timedelta(days=7)

        total = 0
        for record in self.records:
            if week_ago <= record.date <= now:
                total += record.amount

        return total


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
        elif date:
            self.date = (dt.datetime.strptime(date, "%d.%m.%Y")).date()


class CaloriesCalculator(Calculator):
    """Подкласс класса Calculator.
    Добавленный метод - определение, сколько кКал ёще можно получить сегодня.
    """

    def get_calories_remained(self):
        """Сколько ещё кКал можно/нужно получить сегодня."""

        remain = self.limit - self.get_today_stats()
        if remain > 0:
            string = (
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {remain} кКал'
            )

            return string

        elif remain <= 0:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """Подкласс класса Calculator.
    Добавленный метод - информация о дневном балансе.
    """

    USD_RATE = 70.8800
    EURO_RATE = 80.4134

    def get_today_cash_remained(self, currency):

        keys = ('rub', 'usd', 'eur')
        if currency.lower().startswith(keys):

            remain = self.limit - self.get_today_stats()

            amounts = (
                round(remain, 2),
                round(remain / self.USD_RATE, 2),
                round(remain / self.EURO_RATE, 2)
            )
            codes = ('руб', 'USD', 'Euro')

            which_currency = dict(zip(keys, zip(amounts, codes)))
            money_amount, currency_code = which_currency[currency]

            if remain > 0:
                return f'На сегодня осталось {money_amount} {currency_code}'

            elif remain == 0:
                return 'Денег нет, держись'

            if remain < 0:
                string = (
                    f'Денег нет, держись: твой долг - '
                    f'{abs(money_amount)} {currency_code}'
                )

                return string

        else:
            raise ValueError('This is not a supported currency') from Exception
