from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu usuário')
        add_placeholder(self.fields['email'], 'Ex: email@email.com')
        add_placeholder(self.fields['first_name'], 'Ex.: Maria')
        add_placeholder(self.fields['last_name'], 'Ex.: Silva')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password2'], 'Repita sua senha')

    username = forms.CharField(
        label='Usuário',
        help_text=(
            'Nome de usuário deve ter letras, números ou um desses caracteres @.+-_. '
            'O comprimento deve estar entre 4 e 150 caracteres.'
        ),
        error_messages={
            'required': 'Este campo não deve estar vazio.',
            'min_length': 'O nome de usuário deve ter pelo menos 4 caracteres',
            'max_length': 'O nome de usuário deve ter menos de 150 caracteres',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Digite seu nome.'},
        label='Nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Digite seu sobrenome.'},
        label='Sobrenome'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail é obrigatório'},
        label='E-mail',
        help_text='O e-mail deve ser válido.',
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),

        error_messages={
            'required': 'A senha não deve estar vazia.'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula,'
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
        ),
        validators=[strong_password],
        label='Senha'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Repetir senha',
        error_messages={
            'required': 'Por favor, repita sua senha.'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(pipoca)s no campo password',
                code='invalid',
                params={'pipoca': '"atenção"'}
            )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo primeiro nome',
                code='invalid',
                params={'value': '"John Doe"'}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password e Password2 precisam ser iguais.',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
