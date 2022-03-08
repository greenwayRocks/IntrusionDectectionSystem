from django.shortcuts import render, redirect

from .forms import SpamForm
import joblib

spamModel = joblib.load('ml_models/spam_model')

# Create your views here.
def home(request):
    # pred = spamModel.predict(["Hello, this is Mark and this is a ham message, isn't it?"])

    if request.method == 'POST':
        form = SpamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('HomePage')
    else:
        form = SpamForm()

    context = {
        'form': form,
        # 'prediction': pred
    }

    return render(request, 'index.html', context)
