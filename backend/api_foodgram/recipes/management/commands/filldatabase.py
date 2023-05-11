'''Managment command to fill the database'''

import logging
import sys
from csv import DictReader

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(filename)s/%(funcName)s %(message)s'
)
logger.addHandler(handler)
handler.setFormatter(formatter)

User = get_user_model()


class Command(BaseCommand):
    help = 'Use this command to fill the database'

    def handle(self, *args, **options):
        logger.debug(f'Start {Ingredient.__name__} data transfer')
        try:
            objs = [
                Ingredient(**obj) for obj in DictReader(
                    open('static/data/ingredients.csv', encoding='utf8')
                )
            ]
            Ingredient.objects.bulk_create(objs=objs, ignore_conflicts=True)
            logger.debug(
                f'Data successfully loaded into {Ingredient.__name__}\n'
            )
        except Exception:
            logger.error(
                'We have a problem with data or model\n',
                exc_info=True
            )
