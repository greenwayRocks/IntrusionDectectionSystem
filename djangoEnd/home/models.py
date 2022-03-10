from django.db import models

# import joblib

# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
# from sklearn.tree import DecisionTreeClassifier

# Create your models here.

class Spam(models.Model):
    mail_content = models.TextField(max_length=50000, null=True)
    prediction = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    # model = joblib.load('ml_models/spam_model')
    # self.prediction = model.predict([ self.mail_content ])
    # return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.mail_content
