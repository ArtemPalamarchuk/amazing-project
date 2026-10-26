import os

from django.core.management.base import BaseCommand, CommandError

from api.models import Project, User

E2E_USERNAME = "e2e"
E2E_PASSWORD = "e2e-pass"
E2E_PROJECT = "E2E project"


class Command(BaseCommand):
    help = "Create the e2e test user and project. Requires ALLOW_E2E_SEED=1."

    def handle(self, *args, **options):
        # The command ships in the prod image and the password is public,
        # so it only runs when explicitly allowed.
        if os.environ.get("ALLOW_E2E_SEED") != "1":
            raise CommandError("seed_e2e is disabled: set ALLOW_E2E_SEED=1 to run it.")

        user, user_created = User.objects.get_or_create(username=E2E_USERNAME)
        # Reset the password on every run so e2e login never depends on old data.
        user.set_password(E2E_PASSWORD)
        user.save()

        _, project_created = Project.objects.get_or_create(name=E2E_PROJECT, owner=user)

        self.stdout.write(
            self.style.SUCCESS(
                f"user {E2E_USERNAME}: {'created' if user_created else 'exists'}, "
                f"project: {'created' if project_created else 'exists'}"
            )
        )
