from django import forms
from .models import Article, Reply

class ArticleForm(forms.ModelForm):
    keywords = forms.CharField(required=False, help_text="Comma separated, up to 6",
                               widget=forms.TextInput(attrs={"placeholder": "admission, fest, cse"}))
    class Meta:
        model = Article
        fields = ["title", "kind", "section", "body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 12, "maxlength": 6000})}
    field_order = ["title", "kind", "section", "keywords", "body"]

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["text"]
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={"rows": 2, "placeholder": "Write a reply"})}
