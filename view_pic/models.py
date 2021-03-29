from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


class Picture(models.Model):
	current_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="", blank=True)
	title = models.CharField('', max_length=50)
	anons = models.CharField('', max_length=160, default="")
	full_text = models.TextField('', default="")
	picture = models.FileField('', upload_to='pictures/', default="")
	date = models.DateTimeField('', default=timezone.now, blank=True)


	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return f'/view_pic/{self.id}'

	class Meta:
		verbose_name = 'Рисунок'
		verbose_name_plural = 'Рисунки'


class Grading(models.Model):
	evaluating_user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="", blank=True)
	rate_content_meaning = models.IntegerField()
	rate_draw_technique = models.IntegerField()
	rate_originality = models.IntegerField()
	picture_id = models.ForeignKey(Picture, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return f'/view_pic/{self.id}'

	class Meta:
		verbose_name = 'Оценка'
		verbose_name_plural = 'Оценки'