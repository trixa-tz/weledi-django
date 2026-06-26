from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField (max_length = 100)
    slug = models.SlugField (unique = True )
    body = models.TextField ()
    created = models.DateTimeField( auto_now_add = True )

    def __str__(self):
        # Post Object(4) - changes to the custon name
        return self.title
    
