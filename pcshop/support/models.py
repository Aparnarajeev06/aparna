from django.db import models
from django.contrib.auth.models import User
from orders.models import OrderItem

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Billing', 'Billing/Payment'),
        ('Shipping', 'Shipping/Delivery'),
        ('Hardware', 'Hardware & Compatibility'),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')

    def __str__(self):
        return self.question

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General Inquiry'),
        ('Order', 'Order Problem'),
        ('Builder', 'PC Builder Question'),
        ('Technical', 'Technical Support'),
    ]

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    subject = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='General')
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.status}] {self.subject} by {self.user.username}"

class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="replies")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.sender.username} on ticket {self.ticket.id}"

class RMARequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rma_requests")
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name="rma")
    reason = models.TextField(help_text="Reason for the return or warranty request")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"RMA {self.id} - {self.order_item.product.name if self.order_item.product else 'Unknown Part'} ({self.status})"

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '⭐ Poor'),
        (2, '⭐⭐ Fair'),
        (3, '⭐⭐⭐ Good'),
        (4, '⭐⭐⭐⭐ Excellent'),
        (5, '⭐⭐⭐⭐⭐ Outstanding'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedbacks", null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, help_text="Your name (optional if logged in)")
    email = models.EmailField(blank=True, help_text="Your email (optional if logged in)")
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=5)
    title = models.CharField(max_length=200, help_text="Brief title of your feedback")
    message = models.TextField(help_text="Your detailed feedback or suggestion")
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False, help_text="Display this feedback on the website")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_rating_display()}"
