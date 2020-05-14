from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist


class NewPostForm(forms.Form):
    subject = forms.CharField(max_length=60,
                              widget=forms.TextInput(attrs={'class': 'input-field',
                                                            'placeholder': 'Post Subject',
                                                            }
                                                     )
                              )

    text = forms.CharField(max_length=1000,
                           widget=forms.Textarea(attrs={'class': 'input-field',
                                                        'style': 'resize: none'
                                                        }
                                                 )
                           )


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password',
                                                                     }
                                                              )

        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirm password',
                                                                     }
                                                              )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {'username': forms.TextInput(attrs={'class': 'input-field',
                                                      'placeholder': 'Username',
                                                      }
                                               ),
                   'email': forms.EmailInput(attrs={'class': 'input-field',
                                                    'placeholder': 'Email',
                                                    }
                                             ),
                   }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('User with same email already exists')
        return email


class SignInForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter username',
                                                             }
                                                      )
                               )
    password = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Enter password',
                                                                                }
                                                                         )
                               )


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget = forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': ' Old password',
                                                                        }
                                                                 )

        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'New password',
                                                                         }
                                                                  )
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Confirm password',
                                                                         }
                                                                  )

        for name, field in self.fields.items():
            field.help_text = None


class ResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        widgets = {'email': forms.EmailInput(attrs={'class': 'input-field',
                                                    'placeholder': 'Email',
                                                    }
                                             )
                   }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            user = User.objects.get(email=email)
            return user.email

        except ObjectDoesNotExist:
            raise forms.ValidationError('User with this email does not exists')
