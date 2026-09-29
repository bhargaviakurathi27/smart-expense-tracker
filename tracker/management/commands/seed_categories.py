from django.core.management.base import BaseCommand
from tracker.models import Category


class Command(BaseCommand):
    help = "Creates the default set of categories if they don't already exist"

    def handle(self, *args, **options):
        categories = [
            ("Food", "expense"),
            ("Travel", "expense"),
            ("Shopping", "expense"),
            ("Education", "expense"),
            ("Bills", "expense"),
            ("Entertainment", "expense"),
            ("Health", "expense"),
            ("Other", "expense"),
            ("Salary", "income"),
        ]

        created_count = 0
        for name, category_type in categories:
            # get_or_create avoids duplicate errors if you run this command twice
            obj, created = Category.objects.get_or_create(
                name=name,
                defaults={"category_type": category_type},
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")

        self.stdout.write(self.style.SUCCESS(f"\nDone. {created_count} new categories created."))