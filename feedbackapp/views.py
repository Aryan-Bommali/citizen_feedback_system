
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import FeedbackForm
from .models import Feedback
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden



def landing(request):
    if request.user.is_authenticated:
        if request.user.is_staff:  
            return redirect('admin_dashboard')
        else:  
            return redirect('user_dashboard')
    
    return render(request, 'landing.html')

def register_user(request):

    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.is_staff else 'user_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'auth/register.html')


def login_user(request):

    if request.user.is_authenticated:
        return redirect('admin_dashboard' if request.user.is_staff else 'user_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_dashboard' if user.is_staff else 'user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'auth/login.html')


    
def logout_user(request):
    logout(request)
    return redirect('/')

@login_required
def feedback_detail(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)

    if not request.user.is_staff and feedback.user != request.user:
        messages.error(request, "You are not authorized to view this feedback.")
        return redirect('user_dashboard')

    if request.method == 'POST' and request.user.is_staff:
        new_status = request.POST.get('status')
        feedback.status = new_status
        feedback.save()
        messages.success(request, f"Feedback #{feedback.id} status updated to {new_status}.")
        return redirect('feedback_detail', pk=pk)

    return render(request, 'feedback_detail.html', {'feedback': feedback})

def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.user.is_staff or request.user == feedback.user:
        feedback.delete()
        messages.success(request, "✅ Feedback deleted successfully!")
    else:
        messages.error(request, "❌ You don't have permission to delete this feedback.")

    # Redirect accordingly
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')
        
@login_required
def profile_page(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Update fields
        user.username = username
        user.email = email
        if password:
            user.set_password(password)
        user.save()

        messages.success(request, "Profile updated successfully!")

        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, user)

        return redirect('profile')

    return render(request, 'profile.html', {'user': user})


@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  
            feedback.save()
            messages.success(request, "Feedback submitted successfully.")
            return redirect('user_dashboard')
    else:
        form = FeedbackForm()

    return render(request, 'submit_feedback.html', {'form': form})

@login_required
def user_dashboard(request):

    if request.user.is_staff:
        return redirect('admin_dashboard')

    feedbacks = Feedback.objects.filter(user=request.user)

    status = request.GET.get('status')
    if status:
        feedbacks = feedbacks.filter(status=status)

    return render(request, 'user_dashboard.html', {'feedbacks': feedbacks})


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')

    feedbacks = Feedback.objects.all().order_by('-created_at')
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard.html', {'feedbacks': feedbacks, 'users': users})

@login_required
def update_feedback_status(request, feedback_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to perform this action.")

    if request.method == "POST":
        new_status = request.POST.get("status")
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.status = new_status
        feedback.save()
        messages.success(request, "Feedback status updated successfully.")
        return redirect('admin_dashboard')