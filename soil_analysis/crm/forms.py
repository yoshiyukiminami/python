from django import forms

from .models import Company


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'remark', 'category')
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if 'クサリク' in name:
            raise forms.ValidationError('「クサリク」を含む取引先は登録できなくなりました（取引停止）')

        return name
