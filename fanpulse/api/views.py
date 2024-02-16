
from django.shortcuts import render, redirect
from .models import Idea, Vote
from .forms import IdeaForm  # Assuming you have a form for Idea
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings
import json

from .forms import UserRegisterForm
stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY

def create_idea(request, username):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)  # Don't save to DB yet
            idea.creator = request.user  # Assign the current user as the creator
            idea.username = username
            idea.save()  # Now save to DB
            return redirect('/ideas/{0}'.format(username))
    else:
        form = IdeaForm()
    return render(request, 'api/create_idea.html', {'form': form})



def list_ideas(request, username):
    ideas =  list(Idea.objects.filter(username=username, approve=True).order_by('votes').values('id', 'title', 'description', 'votes'))
    return render(request, 'api/ideas_list.html', {"ideas": ideas, "username": username, "stripe_publishable_key": STRIPE_PUBLISHABLE_KEY})


def vote_idea(request, idea_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)

    idea = get_object_or_404(Idea, pk=idea_id)
    vote, created = Vote.objects.get_or_create(user=request.user, idea=idea)
    if not created:
        # The vote already exists, user has voted before
        return JsonResponse({'error': 'You have already voted for this idea'}, status=400)

    idea.votes += 1  # Increment the vote count

    idea.save()

    return JsonResponse({'votes': idea.votes})



# views.py



def create_checkout_session(request, idea_id):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            amount = data.get('amount')
            username = data.get('username')

            # You can adjust the payment amount and currency here
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Contribution for Idea ID {}'.format(idea_id),
                                'metadata': {
                                    'idea_id': idea_id
                                },
                            },
                            'unit_amount': amount,  # $1.00 minimum
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                # Example of setting success_url and cancel_url in your Django view
                success_url=request.build_absolute_uri('/ideas/{0}'.format(username)) + '?success=true',
                cancel_url=request.build_absolute_uri('/ideas/{0}'.format(username)) + '?canceled=true',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # You can also log the user in directly here and redirect them
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})