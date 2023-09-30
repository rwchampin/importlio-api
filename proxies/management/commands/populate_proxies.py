from django.core.management.base import BaseCommand, CommandError
from proxies.models import Proxy
import requests

class Command(BaseCommand):
    help = "Poopulate the initial proxies data"

    def add_arguments(self, parser):
        parser.add_argument("limit", nargs="+", type=int)

    def handle(self, *args, **options):
        if Proxy.objects.count() > 0:
            raise CommandError("Proxies already populated")
        
        if options["limit"] is None:
            options["limit"] = 500
            
        endpoint = f'https://proxylist.geonode.com/api/proxy-list?limit={options['limit']}&country=US&page=1&sort_by=lastChecked&sort_type=desc'
        proxies = requests.get(endpoint).json()
        
        
        
        for proxy in proxies:
            try:
                p = Proxy.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(
                self.style.SUCCESS('Successfully closed poll "%s"' % poll_id)
            )
            
            
  