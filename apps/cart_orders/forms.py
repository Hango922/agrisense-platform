from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    phone = forms.RegexField(r'^\+?[0-9 ()-]{4,15}$', max_length=15)
    address = forms.CharField(max_length=2000)
    payment_method = forms.ChoiceField(choices=[('cod', 'COD'), ('vietqr', 'VietQR')])
    note = forms.CharField(required=False, max_length=2000)


class PaymentProofForm(forms.Form):
    payment_proof = forms.ImageField()

    def clean_payment_proof(self):
        upload = self.cleaned_data['payment_proof']
        if upload.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Ảnh tối đa 5 MB.')
        if upload.image.format not in ('PNG', 'JPEG', 'WEBP'):
            raise forms.ValidationError('Chỉ nhận ảnh PNG, JPEG hoặc WebP.')
        return upload
