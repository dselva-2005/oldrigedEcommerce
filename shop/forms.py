from django import forms
from .models import ProductReview,SiteReviewModel

class ReviewForm(forms.ModelForm):

    class Meta:
        model = ProductReview
        fields = ['product','body','rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hide the 'product' field by using the HiddenInput widget
        self.fields['product'].widget = forms.HiddenInput()
    
class SiteReviewForm(forms.ModelForm):
    
    class Meta:
        model = SiteReviewModel
        fields = ['body','rating']
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'class': 'mx-3'})