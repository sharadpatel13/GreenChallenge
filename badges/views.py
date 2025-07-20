from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .models import UserProofUpload, Badge
from .forms import SubmitProofForm

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
