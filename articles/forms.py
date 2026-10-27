
from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from .models import Article, Reply, Keyword


class ArticleForm(forms.ModelForm):
    keywords = forms.CharField(
        required=False,
        help_text="Enter up to 6 keywords separated by commas.",
        widget=forms.TextInput(
            attrs={
                "placeholder": "admission, fest, cse",
                "class": "form-control",
                "maxlength": 200,
            }
        ),
    )

    class Meta:
        model = Article
        fields = ["title", "kind", "section", "body"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter article title",
                    "maxlength": 160,
                }
            ),
            "kind": forms.Select(attrs={"class": "form-select"}),
            "section": forms.Select(attrs={"class": "form-select"}),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 12,
                    "maxlength": 6000,
                    "placeholder": "Write your article here...",
                }
            ),
        }

    field_order = ["title", "kind", "section", "keywords", "body"]

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if len(title) < 5:
            raise ValidationError(
                "The title must contain at least 5 characters."
            )

        return title

    def clean_body(self):
        body = self.cleaned_data["body"].strip()

        if len(body) < 20:
            raise ValidationError(
                "The article must contain at least 20 characters."
            )

        if len(body) > 6000:
            raise ValidationError(
                "The article cannot exceed 6000 characters."
            )

        return body

    def clean_keywords(self):
        raw_keywords = self.cleaned_data.get("keywords", "")
        keywords = []

        for item in raw_keywords.split(","):
            name = item.strip()

            if name and name.lower() not in {
                keyword.lower() for keyword in keywords
            }:
                keywords.append(name)

        if len(keywords) > 6:
            raise ValidationError("You can add at most 6 keywords.")

        for name in keywords:
            if len(name) > 30:
                raise ValidationError(
                    f'"{name[:40]}" exceeds the 30-character limit.'
                )

        return keywords

    def save(self, commit=True):
        article = super().save(commit=commit)

        if commit:
            self._save_keywords(article)

        return article

    def save_m2m(self):
        super().save_m2m()

        if self.instance.pk:
            self._save_keywords(self.instance)

    def _save_keywords(self, article):
        keyword_objects = []

        for name in self.cleaned_data.get("keywords", []):
            keyword, _ = Keyword.objects.get_or_create(name=name)
            keyword_objects.append(keyword)

        article.keywords.set(keyword_objects)


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["text"]
        labels = {"text": ""}
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 2,
                    "maxlength": 500,
                    "placeholder": "Write a reply...",
                    "class": "form-control",
                }
            )
        }

    def clean_text(self):
        text = self.cleaned_data["text"].strip()

        if len(text) < 2:
            raise ValidationError(
                "Your reply must contain at least 2 characters."
            )

        return text
