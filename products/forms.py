from django import forms
from .widgets import CustomClearableFileInput
from .models import Product,Category, ProductReview


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('rating',)


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('rating_score', 'review_title', 'review_comment')

class ProduceForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'