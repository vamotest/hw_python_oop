# Калькулятор денег и калорий
Sprint 2. Итоговый проект.


# Index
1. [Technical requirement](#technical-requirement)
2. [Money calculator](#money-calculator)
3. [Calories calculator](#calories-calculator)
4. [Additional requirements](#additional-requirements)
5. [Examples](#examples)
6. [More about the output format](#more-about-the-output-format)
7. [How to check](#how-to-check)
8. [How to use](#how-to-use)

**[⬆ Back to Index](#index)**
## Technical requirement
Создайте два калькулятора: для подсчёта денег и калорий. 
Пользовательскую часть калькуляторов, их «лицо», писать не нужно, напишите только логику — отдельный класс для каждого из калькуляторов.

**[⬆ Back to Index](#index)**
## Money calculator
должен уметь:
1. Сохранять новую запись о расходах методом `add_record()`
2. Считать, сколько денег потрачено сегодня методом `get_today_stats()`
3. Определять, сколько ещё денег можно потратить сегодня в рублях, долларах или евро — метод `get_today_cash_remained(currency)`
4. Считать, сколько денег потрачено за последние 7 дней — метод `get_week_stats()`

**[⬆ Back to Index](#index)**
## Calories calculator
должен уметь:

1. Сохранять новую запись о приёме пищи — метод `add_record()`
2. Считать, сколько калорий уже съедено сегодня — метод `get_today_stats()`
3. Определять, сколько ещё калорий можно/нужно получить сегодня — метод `get_calories_remained()`
4. Считать, сколько калорий получено за последние 7 дней — метод `get_week_stats()`

**[⬆ Back to Index](#index)**
## Additional requirements
У калькуляторов много пересекающихся функций: они должны уметь хранить какие-то записи 
(о еде или деньгах, но по сути - всё числа и даты), знать дневной лимит 
(сколько в день можно истратить денег или сколько калорий можно получить) и 
суммировать записи за конкретные даты. 

Всю эту общую функциональность заложите в родительский класс __Calculator__, 
а от него унаследуйте классы __CaloriesCalculator__ и __CashCalculator__.

Конструктор класса __Calculator__ должен принимать один аргумент — 
число `limit` (дневной лимит трат/калорий, который задал пользователь). 
В конструкторе создайте пустой список, в котором потом будут храниться записи (назовите его `records`).

Чтобы было удобнее создавать записи, создайте для них отдельный класс __Record__. 

В нём сохраните:
* число `amount` (денежная сумма или количество килокалорий),
* дату создания записи `date` (передаётся в явном виде в конструктор, либо присваивается значение по умолчанию — текущая дата),
* комментарий `comment`, поясняющий, на что потрачены деньги или откуда взялись калории.

**[⬆ Back to Index](#index)**
## Examples
```python
# для CashCalculator 
r1 = Record(amount=145, comment="Безудержный шопинг", date="08.03.2019")
r2 = Record(amount=1568, comment="Наполнение потребительской корзины", date="09.03.2019")
r3 = Record(amount=691, comment="Катание на такси", date="08.03.2019")

# для CaloriesCalculator
r4 = Record(amount=1186, comment="Кусок тортика. И ещё один.", date="24.02.2019")
r5 = Record(amount=84, comment="Йогурт.", date="23.02.2019")
r6 = Record(amount=1140, comment="Баночка чипсов.", date="24.02.2019")
```

**[⬆ Back to Index](#index)**
## More about the output format

1. Метод `get_calories_remained()` __калькулятор калорий__ должен возвращать ответ
* _«Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более N кКал»_, если лимит `limit` не достигнут,
* или _«Хватит есть!»_, если лимит достигнут или превышен.

2. Метод `get_today_cash_remained(currency)` __денежного калькулятора)) должен 
принимать на вход код валюты: одну из строк `'rub'`, `'usd'` или `'eur'`.

Возвращает он сообщение о состоянии дневного баланса в этой валюте, 
округляя сумму до двух знаков после запятой (до сотых):

* _«На сегодня осталось N руб/USD/Euro»_ — в случае, если лимит `limit` не достигнут,
* или _«Денег нет, держись»_, если лимит достигнут,
* или _«Денег нет, держись: твой долг - N руб/USD/Euro»_, если лимит превышен.

Курс валют укажите константами `USD_RATE` и `EURO_RATE`, прямо в теле класса `CashCalculator`. 
Какой курс вы укажете — не так важно, выберите любой, похожий на правду. 
Значения обменного курса можно посмотреть, например, на главной странице [Яндекса](https://yandex.ru). 
Получать актуальный курс с биржи мы обязательно научимся, только чуть позже.

**[⬆ Back to Index](#index)**
## How to check
Чтобы своими глазами увидеть, что ваши классы работают правильно, напишите какой-нибудь сценарий их использования.

```python
import datetime as dt
        
class Record:
     ...
        
class Calculator:
     ...
        
# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
        
# дата в параметрах не указана, 
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
                
print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# На сегодня осталось 555 руб
```

**[⬆ Back to Index](#index)**
## How to use

1. Создайте виртуальное окружение и активируйте его:
```shell script
~ python3 -m venv env && source env/bin/activate
```
2. Обновите pip до последней версии:
```shell script
~ pip install --upgrade pip
```
3. Установите зависимости:
```shell script
~ pip install -r requirements.txt
```
4. Запустите тесты:
```shell script
~ python3 -m pytest --verbose --html=report.html
```
5. Arguments:
```
[--verbose]: increase verbosity
[--html]: generate a HTML report for the test results
```