from django.contrib.auth.models import User
from django.db import models

class Movie(models.Model):
    """Represents a movie listing"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    """
    Represents a movie review that has a foreign key to
    `Movie` model.
    """
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    # CASCADE: If I delete a movie that a review references, all
    # reviews delete along with the movie.
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Report(models.Model):
    """
    Represents a review report. This should NOT cascading delete because
    admins want to keep a consistent history for all abuse on our site.
    """
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    review = models.ForeignKey(Review, on_delete=models.DO_NOTHING)
    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reporter_user')
    reportee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reportee_user')

    def __str__(self):
        return f'{self.id} - {self.reporter.username}|{self.movie.name}'
