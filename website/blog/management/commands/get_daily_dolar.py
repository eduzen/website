from datetime import datetime, timedelta, time
from yahoo_finance import Currency

from django.core.management.base import BaseCommand

from blog.models import DolarPeso


class Command(BaseCommand):
    help = "Get daily dolar/peso value"

    def handle(self, *args, **options):

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        current_peso = DolarPeso.objects.filter(created_date__lte=today_end, created_date__gte=today_start)
        if not current_peso.exists():
            currency = Currency("ARS")
            end_date = currency.data_set.get("DateTimeUTC")
            end_date = end_date.split(" ")
            end_date[-1] = end_date[-1][:4]
            end_date = " ".join(end_date)
            date = datetime.strptime(end_date[:-1], "%Y-%m-%d %H:%M:%S %Z")
            data = {
                "name": currency.data_set.get("Name"),
                "bid": currency.data_set.get("Bid"),
                "ask": currency.data_set.get("Ask"),
                "rate": currency.data_set.get("Rate"),
                "created_date": date,
            }
            current_peso = DolarPeso.objects.create(**data)
        else:
            current_peso = current_peso[0]

        self.stdout.write(self.style.SUCCESS('Successfully dolar poll "%s"' % current_peso))
