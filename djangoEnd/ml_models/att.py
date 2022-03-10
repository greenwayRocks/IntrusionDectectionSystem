import joblib

model = joblib.load('spam_model')
pred = []

with open('mails.txt', 'r') as fp:
    msg = fp.readlines()
    for m in msg:
        prediction = model.predict([m])
        pred.append(str(prediction))
    
# msg = 'Hello Mark, how are you? This is not a spam, is it?'


print(pred)
