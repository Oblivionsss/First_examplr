import datetime as dt
        
date_format = '%d.%m.%Y'

class Record:
    def __init__(self, amount, comment: str, date: str = None):
        self.amount = amount
        self.comment = comment
        if date == None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """
        Функция записи данных
        record - объект класса Record  
        """     
        self.records.append(record)

    def get_today(self):
        """
        Фунция возвращает сегодняшнюю дату
        """
        return dt.datetime.today().date()
    
    def get_today_stats(self):
        """
        Функция возвращает сумму калорий / денег
        потраченных за сегодняшний день
        today = дата на сегодня
        """
        today = self.get_today()
        return sum([record.amount 
                for record in self.records 
                if record.date == today])

    def get_week_stats(self):
        """
        Функция возвращает сумму калорий / денег
        потраченных за последнюю неделю
        today = дата сегодня
        first date = дата семь дней назад
        """
        today = self.get_today()
        first_date = today - dt.timedelta(days=7)
        return sum([record.amount 
                    for record in self.records 
                    if first_date < record.date <= today])


class CashCalculator(Calculator):
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        """
        Функция показвает остаток денег на день
        all_curency - массив констант курсов
        today_remained - потрачено за день
        remained - разница между дневным лимитом и объемом за день
        abs_remained - remained в абсолютной величине 
        """     
        all_currency = {
            'rub': (self.RUB_RATE, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
        }

        if currency not in all_currency:
            raise ValueError("Валюта введена некорректно")
        currency_course, currency_name = all_currency[currency]
        today_remained = self.get_today_stats()
        remained = round ((self.limit - today_remained) / currency_course, 2)
        abs_remained = abs(remained)
        
        if remained == 0:
            return("Денег нет, держись")
        elif remained > 0:
            return(f"На сегодня осталось {remained} {currency_name}")
        else:
            return(f"Денег нет, держись: твой долг - "
                  f"{abs_remained} {currency_name}")


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """
        Функция показвает остаток калорий на день
        today_remained - потрачено за день
        remained - разница между дневным лимитом и объемом за день 
        """
        today_remained = self.get_today_stats()
        remained = self.limit - today_remained

        if remained > 0:
            return(f"Сегодня можно съесть что-нибудь ещё, " 
                  f"но с общей калорийностью не более {remained} кКал")    
        else:
            return(f"Хватит есть!")

# создадим калькулятор денег с дневным лимитом 1000
# cash_calculator = CashCalculator(1000)
        
# # дата в параметрах не указана, 
# # так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
# cash_calculator.add_record(Record(amount=100, comment="кофе", date="08.06.2023"))
# cash_calculator.add_record(Record(amount=111, comment="булка", date="08.06.2023"))
# cash_calculator.add_record(Record(amount=111, comment="пятерочка", date="08.06.2023"))
# cash_calculator.add_record(Record(amount=120, comment="магазин", date="02.06.2023"))
# cash_calculator.add_record(Record(amount=120, comment="магазин", date="30.05.2023"))
# cash_calculator.add_record(Record(amount=900, comment="магазин", date="09.06.2023"))
# cash_calculator.add_record(Record(amount=101, comment="магазин", date="09.06.2023"))
# print(cash_calculator.records)
# print(cash_calculator.get_today_stats())
# print(cash_calculator.get_week_stats())
# cash_calculator.get_today_cash_remained('usd')
# и к этой записи тоже дата должна добавиться автоматически
# cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
# cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
                
# print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# На сегодня осталось 555 руб