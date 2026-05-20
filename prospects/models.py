from django.db import models


class Prospect(models.Model):
    """
    Core data model representing a prospective student record.
    Email is the primary seed key — unique and always required.
    All other fields are optional and nullable.
    """

    HOW_HEARD_CHOICES = [
        ('roundabout_banner', 'Roundabout Banner'),
        ('friends_family', 'Friends/Family'),
        ('traditional_media', 'Traditional Media (Radio, TV, etc.)'),
        ('digital_advert', 'Digital Advert'),
        ('fliers_banner', 'Fliers/Banner'),
    ]

    email = models.EmailField(
        max_length=255,
        unique=True,
        help_text='Required. Must be a valid, unique email address.',
    )
    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    occupation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    highest_degree = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    program = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    how_heard = models.CharField(
        max_length=50,
        choices=HOW_HEARD_CHOICES,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prospect'
        verbose_name_plural = 'Prospects'

    def __str__(self):
        return self.email
