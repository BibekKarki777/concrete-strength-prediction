from django.shortcuts import redirect, render


def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard:dashboard")
        return redirect("accounts:dashboard")

    return render(request, "core/home.html")


def about_view(request):
    return render(request, "core/about.html")