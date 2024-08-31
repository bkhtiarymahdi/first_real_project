import os
from common.models import Movie
from moviepy.editor import VideoFileClip

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

@receiver(post_save, sender=Movie)
def get_video_duration(sender, instance, **kwargs):
    if not instance.duration:
        vidoe_path = os.path.join(settings.MEDIA_ROOT, instance.film.name)
        with VideoFileClip(vidoe_path) as video:
            minutes = int(video.duration // 60)
            seconds = int(video.duration % 60)
            instance.duration = f'{minutes}:{seconds}'        
        instance.save()