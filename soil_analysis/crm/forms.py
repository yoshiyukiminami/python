from django import forms

from .models import Company, Land


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


class LandCreateForm(forms.ModelForm):
    class Meta:
        model = Land
        fields = ('name', 'prefecture', 'location', 'latlon', 'remark', 'cultivation_type', 'owner')
        exclude = []
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'prefecture': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'latlon': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.TextInput(attrs={'class': 'form-control'}),
            'cultivation_type': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if 'あの圃場' in name:
            raise forms.ValidationError('「あの圃場」を含む圃場名は登録できなくなりました（あいまい）')

        return name
