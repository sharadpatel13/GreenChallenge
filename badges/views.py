from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Challenge, UserProgress  # Corrected import
from .models import UserProofUpload, Badge, LeaderboardEntry, Challenge, UserProgress
from .forms import SubmitProofForm, BadgeAssignForm, ChallengeForm, JoinChallengeForm
from collections import defaultdict

# Challenge Views
class ChallengeCreateView(LoginRequiredMixin, CreateView):
    model = Challenge
    form_class = ChallengeForm
    template_name = 'challenge_form.html' # Modified
    success_url = reverse_lazy('challenge_list')

class ChallengeListView(ListView):
    model = Challenge
    template_name = 'challenge_list.html' # Modified
    context_object_name = 'challenges'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JoinChallengeForm()
        return context

class ChallengeDetailView(DetailView):
    model = Challenge
    template_name = 'challenge_detail.html' # Modified
    context_object_name = 'challenge'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = JoinChallengeForm(initial={'challenge_id': self.object.id})
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        challenge = self.get_object()

        existing_progress = UserProgress.objects.filter(user=request.user, challenge=challenge).exists()
        if not existing_progress:
            UserProgress.objects.create(
                user=request.user,
                challenge=challenge,
                start_date=timezone.now()
            )
            messages.success(request, "Successfully joined the challenge")
        else:
            messages.info(request, "You've already joined this challenge!")
        return HttpResponseRedirect(reverse('my-challenges'))

# Leaderboard View
class LeaderboardView(LoginRequiredMixin, ListView):
    model = LeaderboardEntry
    template_name = 'leaderboard.html' # Modified
    context_object_name = 'leaderboard'
    ordering = ['-points']

# My Challenges Dashboard
class MyChallengesView(LoginRequiredMixin, TemplateView):
    template_name = 'my_challenges.html' # Modified

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        approved_proofs = UserProofUpload.objects.filter(user=user, approved=True)
        pending_proofs = UserProofUpload.objects.filter(user=user, approved=False, rejected=False)
        rejected_proofs = UserProofUpload.objects.filter(user=user, rejected=True)

        grouped_approved = defaultdict(list)
        for proof in approved_proofs:
            grouped_approved[proof.challenge_title].append(proof)

        grouped_pending = defaultdict(list)
        for proof in pending_proofs:
            grouped_pending[proof.challenge_title].append(proof)

        grouped_rejected = defaultdict(list)
        for proof in rejected_proofs:
            grouped_rejected[proof.challenge_title].append(proof)

        total_submissions = UserProofUpload.objects.filter(user=user).count()
        total_badges = approved_proofs.exclude(badge_awarded=None).count()
        total_challenges = UserProofUpload.objects.filter(user=user).values('challenge_title').distinct().count()

        #GET USER PROGRESS FOR LIST
        user_progress = UserProgress.objects.filter(user=user)

        context.update({
            'grouped_proofs': grouped_approved,
            'pending_proofs_grouped': grouped_pending,
            'rejected_proofs_grouped': grouped_rejected,
            'total_badges': total_badges,
            'total_submissions': total_submissions,
            'total_challenges': total_challenges,
            'user_progress': user_progress
        })
        return context

# Submit Proof View
class SubmitProofView(LoginRequiredMixin, CreateView):
    model = UserProofUpload
    form_class = SubmitProofForm
    template_name = 'submit_proof.html' # Modified
    success_url = reverse_lazy('my-challenges')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "✅ Your proof has been submitted and is pending approval.")
        response = super().form_valid(form)

        # Badge logic (moved here from MyChallengesView to make badge logic happen during sumbit proof and not on the dashboard)
        user = self.request.user
        approved_uploads = UserProofUpload.objects.filter(user=user, approved=True)
        approved_count = approved_uploads.count()

        badge_name = "Challenge Achiever"
        badge, created = Badge.objects.get_or_create(
            name=badge_name,
            defaults={'description': 'Awarded for completing 3 approved challenges!'}
        )

        if approved_count >= 3 and not UserProofUpload.objects.filter(user=user, badge_awarded=badge).exists():
            form.instance.badge_awarded = badge
            form.instance.save()
            messages.success(self.request, f"🎉 Congrats! You've earned the '{badge.name}' badge!")

            try:
                send_mail(
                    subject='🎉 Badge Unlocked!',
                    message=f'Congrats {user.username}, you earned the "{badge.name}" badge!',
                    from_email='no-reply@greenchallenge.com',
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except:
                pass

        return response

# Assign Badge View
@login_required
def assign_badge_view(request, proof_id):
    proof = get_object_or_404(UserProofUpload, id=proof_id)

    if request.method == 'POST':
        form = BadgeAssignForm(request.POST, instance=proof)
        if form.is_valid():
            form.save()
            messages.success(request, f'Badge assigned to proof: {proof.challenge_title}')
            return redirect('my-challenges')
    else:
        form = BadgeAssignForm(instance=proof)

    return render(request, 'assign_badge.html', {'form': form, 'proof': proof})

class JoinChallengeView(LoginRequiredMixin, View):
    def post(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, id=challenge_id)
        user = request.user

        with transaction.atomic():  # Wrap in a transaction
            progress, created = UserProgress.objects.get_or_create(
                user=user,
                challenge=challenge,
                defaults={'status': 'in_progress', 'joined_at': timezone.now()}
            )

            if not created:
                messages.info(request, "You've already joined this challenge.")
            else:
                messages.success(request, f"You have joined the {challenge.title} challenge!") # Include the challenge title

        return redirect('my-challenges') #or my_progress depending on where you want to go.

class ReviewProofsView(LoginRequiredMixin, View):
    def get(self, request):
        proofs = UserProofUpload.objects.filter(approved=False, rejected=False)
        return render(request, 'review_proofs.html', {'proofs': proofs})

    def post(self, request):
        proof_id = request.POST.get('proof_id')
        action = request.POST.get('action')
        proof = get_object_or_404(UserProofUpload, id=proof_id)

        if action == 'approve':
            proof.approved = True
            messages.success(request, f"✅ Approved proof for {proof.challenge_title}")
        elif action == 'reject':
            proof.rejected = True
            messages.warning(request, f"❌ Rejected proof for {proof.challenge_title}")

        proof.save()
        return redirect('review_proofs')