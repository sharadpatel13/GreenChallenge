from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from collections import defaultdict

from .models import UserProofUpload, Badge, LeaderboardEntry
from .forms import SubmitProofForm, BadgeAssignForm


class SubmitProofView(LoginRequiredMixin, CreateView):
    model = UserProofUpload
    form_class = SubmitProofForm
    template_name = 'submit_proof.html'
    success_url = reverse_lazy('my-challenges')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "✅ Your proof has been submitted and is pending approval.")
        response = super().form_valid(form)

        # Badge logic
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


class MyChallengesView(LoginRequiredMixin, TemplateView):
    template_name = 'my_challenges.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        approved_proofs = UserProofUpload.objects.filter(user=user, approved=True)
        pending_proofs = UserProofUpload.objects.filter(user=user, approved=False, rejected=False)
        rejected_proofs = UserProofUpload.objects.filter(user=user, rejected=True)

        # Group approved by challenge title
        grouped_approved = {}
        for proof in approved_proofs:
            grouped_approved.setdefault(proof.challenge_title, []).append(proof)

        # Group pending by challenge title
        grouped_pending = {}
        for proof in pending_proofs:
            grouped_pending.setdefault(proof.challenge_title, []).append(proof)

        # Group rejected by challenge title
        grouped_rejected = {}
        for proof in rejected_proofs:
            grouped_rejected.setdefault(proof.challenge_title, []).append(proof)

        # Total submissions = all submissions by user
        total_submissions = UserProofUpload.objects.filter(user=user).count()

        # Total badges = count of approved proofs with badges
        total_badges = approved_proofs.exclude(badge_awarded=None).count()

        # Total distinct challenges user submitted proofs for
        total_challenges = UserProofUpload.objects.filter(user=user).values('challenge_title').distinct().count()

        context.update({
            'grouped_proofs': grouped_approved,
            'pending_proofs_grouped': grouped_pending,
            'rejected_proofs_grouped': grouped_rejected,
            'total_badges': total_badges,
            'total_submissions': total_submissions,
            'total_challenges': total_challenges,
        })

        return context


class LeaderboardView(LoginRequiredMixin, ListView):
    model = LeaderboardEntry
    template_name = 'leaderboard.html'
    context_object_name = 'leaderboard'
    ordering = ['-points']


@login_required
def assign_badge_view(request, proof_id):
    proof = get_object_or_404(UserProofUpload, id=proof_id)

    if request.method == 'POST':
        form = BadgeAssignForm(request.POST, instance=proof)
        if form.is_valid():
            form.save()
            messages.success(request, f'Badge assigned to proof: {proof.challenge_title}')
            return redirect('my-challenges')  # Redirect to My Challenges dashboard
    else:
        form = BadgeAssignForm(instance=proof)

    return render(request, 'assign_badge.html', {'form': form, 'proof': proof})


@login_required
def review_proofs(request):
    if not request.user.is_superuser:
        return redirect('my-challenges')

    pending_proofs = UserProofUpload.objects.filter(approved=False, rejected=False)

    if request.method == 'POST':
        proof_id = request.POST.get('proof_id')
        action = request.POST.get('action')
        proof = get_object_or_404(UserProofUpload, id=proof_id)

        if action == 'approve':
            proof.approved = True
            proof.rejected = False
        elif action == 'reject':
            proof.approved = False
            proof.rejected = True
        proof.save()
        messages.success(request, f"✅ Submission for '{proof.challenge_title}' has been {action}d.")
        return redirect('review-proofs')

    return render(request, 'review_proofs.html', {'proofs': pending_proofs})
