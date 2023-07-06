from django.db import models

class APILogEntry(models.Model):
    """
    Model for APILogEntry
    Atribs:
        method(str): API method name
        path(str): API endpoint
        status_code(int): Status of the request
        response_time(float): Response time of the request
        response_content(str): Content of the response
        created_at(date): Date and time of creation
    """
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    status_code = models.IntegerField()
    response_time = models.FloatField()
    response_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} {self.method} {self.path}"

    class Meta:
        # Ordered in the form of creation
        ordering = ['-created_at']
