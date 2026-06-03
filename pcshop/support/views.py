from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FAQ, Ticket, TicketReply, RMARequest, Feedback
from .forms import FeedbackForm
from orders.models import OrderItem

def support_home_view(request):
    faqs = FAQ.objects.all()
    categories = FAQ.CATEGORY_CHOICES
    
    # Simple direct message contact form handler
    if request.method == 'POST' and not request.user.is_authenticated:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and email and message:
            messages.success(request, "Telemetry received! Our support androids will reach out via email.")
            return redirect('support:home')
        else:
            messages.error(request, "Please fill out all contact form parameters.")
            
    context = {
        'faqs': faqs,
        'categories': categories
    }
    return render(request, 'support/support_home.html', context)

@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        category = request.POST.get('category')
        description = request.POST.get('description')
        
        if subject and description:
            ticket = Ticket.objects.create(
                user=request.user,
                subject=subject,
                category=category,
                description=description
            )
            messages.success(request, f"Support Ticket #{ticket.id} has been logged in the system.")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "Subject and description fields are mandatory.")
            
    return redirect('support:home')

@login_required
def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    replies = ticket.replies.all()
    
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            TicketReply.objects.create(
                ticket=ticket,
                sender=request.user,
                message=message
            )
            # Re-open if closed
            if ticket.status == 'Closed':
                ticket.status = 'Open'
                ticket.save()
            messages.success(request, "Reply dispatched successfully.")
            return redirect('support:ticket_detail', ticket_id=ticket.id)
            
    return render(request, 'support/ticket_detail.html', {'ticket': ticket, 'replies': replies})

@login_required
def create_rma_view(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user)
    
    # Check if RMA already exists
    existing = RMARequest.objects.filter(order_item=order_item).first()
    if existing:
        messages.warning(request, f"RMA warranty ticket #{existing.id} already exists for this item.")
        return redirect('accounts:dashboard')
        
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            rma = RMARequest.objects.create(
                user=request.user,
                order_item=order_item,
                reason=reason
            )
            messages.success(request, f"RMA return query #{rma.id} successfully lodged in database.")
            return redirect('accounts:dashboard')
        else:
            messages.error(request, "A reason for return is required.")
            
    return render(request, 'support/create_rma.html', {'order_item': order_item})

def submit_feedback(request):
    """Handle feedback submission from home page"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            
            # Set user if logged in
            if request.user.is_authenticated:
                feedback.user = request.user
                # Auto-fill name and email from user if not provided
                if not feedback.name:
                    feedback.name = request.user.get_full_name() or request.user.username
                if not feedback.email:
                    feedback.email = request.user.email
            
            feedback.save()
            messages.success(request, "✓ Thank you for your feedback! We appreciate your input.")
            return redirect('/')
        else:
            messages.error(request, "Please check your feedback form and try again.")
            return redirect('/')
    
    # If GET request, redirect to home
    return redirect('/')
