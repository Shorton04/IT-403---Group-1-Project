from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import CustomAuthenticationForm, UserProfileForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import EditProfileForm, CustomPasswordChangeForm, EditMemberForm
from apps.accounts.forms import ProjectMemberRegistrationForm
from .models import CustomUser
from .utils import notify_account_activity
from .models import Notification


@login_required
def notifications_view(request):
    # Fetch notifications for the logged-in user
    notifications = request.user.received_notifications.all().order_by('-created_at')

    # Debugging output
    print("Number of notifications:", notifications.count())
    for n in notifications:
        print(n.message)

    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def register_member_view(request):
    if request.user.role != 'Project Manager':
        messages.error(request, "You are not authorized to register members.")
        return redirect('home')

    if request.method == 'POST':
        form = ProjectMemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save(created_by=request.user)
            messages.success(request, "Project Member account created successfully!")
            return redirect('member_list')
        else:
            messages.error(request, "Failed to register member. Please check the form.")
    else:
        form = ProjectMemberRegistrationForm()

    return render(request, 'register_member.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Automatically assign the default role 'Project Manager'
            user = form.save(commit=False)
            user.role = 'Project Manager'
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            # Display form errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('gantt_chart')
        else:
            messages.error(request, "Invalid email or password")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """
    Handles the logout functionality with a confirmation card.
    """
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect('Login')  # Redirect to the login page after logout
    return render(request, 'logout.html')  # Render the confirmation card

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'profile.html', {'form': form, 'user': user})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            # Notify the project manager about the profile update
            project_manager = user.created_by  # Assuming 'created_by' is set to the project manager
            if project_manager:
                notify_account_activity(
                    sender=user,
                    recipient=project_manager,
                    message=f"{user.username} has updated their profile."
                )
            return redirect('profile')  # Replace with the correct URL name for the profile page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form, 'user': user})


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            notify_account_activity(request.user, request.user.created_by, f"{request.user.username} changed their password")
            messages.success(request, 'Your password has been changed!')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # Notify the project manager about the account deletion
        project_manager = user.created_by  # Assuming 'created_by' is set to the project manager
        if project_manager:
            notify_account_activity(
                sender=user,
                recipient=project_manager,
                message=f"{user.username} has deleted their account."
            )
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('login')
    return render(request, 'delete_account.html')


@login_required
def member_list(request):
    if request.user.role != 'Project Manager':
        messages.error(request, "You are not authorized to view this page.")
        return redirect('home')

    search_email = request.GET.get('search_email', '')

    if search_email:
        # Filter members by email, ensuring they were created by the current user
        members = CustomUser.objects.filter(created_by=request.user, email__icontains=search_email)
    else:
        # Retrieve all members created by the current user
        members = CustomUser.objects.filter(created_by=request.user)

    return render(request, 'member_list.html', {'members': members, 'search_email': search_email})


def edit_member(request, user_id):
    member = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        if 'delete_member' in request.POST:  # Check if the delete button was clicked
            if request.user.role == 'Project Manager':  # Ensure only Project Managers can delete
                member.delete()
                messages.success(request, f"Member {member.username} has been deleted successfully.")
                return redirect('member_list')  # Redirect to the member list page
            else:
                messages.error(request, "You are not authorized to delete members.")
        else:
            # Handle normal edit functionality
            form = EditMemberForm(request.POST, instance=member)
            if form.is_valid():
                form.save()
                messages.success(request, "Member updated successfully.")
                return redirect('member_list')
            else:
                messages.error(request, "Please correct the errors below.")
    else:
        form = EditMemberForm(instance=member)

    return render(request, 'edit_member.html', {'form': form, 'member': member})

@login_required
def delete_member(request, user_id):
    member = get_object_or_404(CustomUser, id=user_id, created_by=request.user)

    if request.method == 'POST':
        member.delete()
        messages.success(request, "Member deleted successfully.")
        return redirect('member_list')

    return render(request, 'delete_member.html', {'member': member})