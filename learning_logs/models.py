from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):

    # length of title

    text = models.CharField(max_length=200)

    # topic image

    image = models.ImageField(upload_to='image/', null=True, blank=True)

    # Date and time of the usage/making

    date_added = models.DateTimeField(auto_now_add=True)

    # Defining an owner
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Returning the title

    def __str__(self):
        return self.text

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


# Making an entry class so the user can add info to the topics


class Entry(models.Model):

    # if topic gets deleted everything about the topic will get deleted

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    # Making so the user can enter as many text in the topic

    text = models.TextField()

    date_added = models.DateTimeField(auto_now_add=True)

    # Making an owner
    owner = models.ForeignKey(User,null=True, on_delete=models.CASCADE)

    # making a plural fot the word entry

    class Meta:

        verbose_name_plural = 'entries'

    # so just the first 50 characters gets printed for a shortcut

    def __str__(self):

        if self.text <= self.text[:49]:
            return self.text
        else:
            return f"{self.text[:50]}..."

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
