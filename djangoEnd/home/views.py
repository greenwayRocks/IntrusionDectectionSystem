from django.shortcuts import render, redirect

from .forms import SpamForm
import joblib

# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
# from sklearn.tree import DecisionTreeClassifier

# Create your views here.
def home(request):
    spamModel = joblib.load('ml_models/spam_model')
    pred = 2
    pkt = 'not captured yet'
    prediction_type = {
        0: "Spam",
        1: "Ham",
        2: "Not predicted"
    }
    # pred = spamModel.predict(["Hello, this is Mark and this is a ham message, isn't it?"])

    if request.method == 'POST':
        form = SpamForm(request.POST)

        if form.is_valid():
            mail = form.cleaned_data["mail_content"]
            print(mail)
            pred = spamModel.predict([mail])
            
            print(prediction_type[int(pred)])
            form.save()
            form = SpamForm()
            # return redirect('HomePage')
    else:
        form = SpamForm()

    context = {
        'form': form,
        'prediction': prediction_type[int(pred)],
        'packet_info': pkt
    }

    return render(request, 'index.html', context)
