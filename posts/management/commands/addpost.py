from django.core.management import BaseCommand
from posts.models import Post


class Command(BaseCommand):
    help = 'creates given number of test posts'

    def add_arguments(self, parser):
        parser.add_argument('num_posts', type=int)

    def handle(self, *args, **options):
        num_posts = options['num_posts']
        if num_posts > 0:
            objs = [
                Post(
                    title=f'Test Post{i}',
                    content=f'This is the test post {i}'
                )
                for i in range(num_posts)
            ]
            print(objs)
            Post.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {num_posts} posts'))