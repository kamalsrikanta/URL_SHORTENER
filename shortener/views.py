from django.shortcuts import render, redirect, get_object_or_404
from .forms import URLForm
from .models import ShortURL
from .utils import generate_short_code


def home(request):

    if request.method == "POST":

        form = URLForm(request.POST)

        if form.is_valid():

            original_url = form.cleaned_data["url"]

            existing_url = ShortURL.objects.filter(
                original_url=original_url
            ).first()

            if existing_url:

                code = existing_url.short_code

            else:

                code = generate_short_code()

                ShortURL.objects.create(
                    original_url=original_url,
                    short_code=code
                )

            request.session["short_url"] = (
                request.build_absolute_uri("/") + code
            )

            return redirect("home")

    else:
        form = URLForm()

    short_url = request.session.pop("short_url", None)

    return render(
        request,
        "shortener/home.html",
        {
            "form": form,
            "short_url": short_url
        }
    )


def redirect_url(request, code):

    url_obj = get_object_or_404(
        ShortURL,
        short_code=code
    )

    url_obj.click_count += 1
    url_obj.save()

    return redirect(url_obj.original_url)