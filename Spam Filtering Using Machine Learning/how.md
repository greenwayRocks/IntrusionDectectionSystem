### How we did it?

- Step 1 :: We start by preparing a dataset consisting of raw emails in "spam_emails_data" directory.

- In Step 2, we specify the paths of the spam and ham emails, as well as assign labels to their directories.

- We proceed to read all of the emails into an array, and create a labels array in Step 3.

- Next, we train-test split our dataset (Step 4), and then fit an NLP pipeline on it in Step 5.

- Finally, in Step 6, we test our pipeline.

- We see that accuracy is pretty high.
- Since the dataset is relatively balanced, there is no need to use special metrics to evaluate success.
