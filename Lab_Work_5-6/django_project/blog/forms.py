from django import forms

class FeedbackForm(forms.Form):
    """Форма зворотного зв'язку."""
    
    # 1. Текстове поле з обмеженням довжини
    name = forms.CharField(
        max_length=50,
        label="Ваше ім'я та прізвище",
        widget=forms.TextInput(attrs={
            'class': 'form-input', 
            'placeholder': 'Наприклад: Іван Петренко'
        })
    )
    
    # 2. Поле електронної пошти
    email = forms.EmailField(
        label="Електронна пошта",
        widget=forms.EmailInput(attrs={
            'class': 'form-input', 
            'placeholder': 'example@mail.com'
        })
    )
    
    # 3. Поле вибору зі списку
    subject = forms.ChoiceField(
        choices=[
            ('general', 'Загальне питання'),
            ('support', 'Технічна підтримка'),
            ('feedback', 'Відгук про сайт'),
        ],
        label="Тема звернення"
    )
    
    # 4. Багаторядкове текстове поле
    message = forms.CharField(
        label="Ваше повідомлення",
        widget=forms.Textarea(attrs={
            'rows': 5, 
            'class': 'form-input', 
            'placeholder': 'Опишіть ваше питання детально...'
        })
    )

    # Кастомна валідація для поля name
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and len(name.split()) < 2:
            raise forms.ValidationError("Будь ласка, введіть повне ім'я та прізвище (мінімум 2 слова).")
        return name

    # Кастомна валідація для поля message
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message and len(message.split()) < 5:
            raise forms.ValidationError("Повідомлення має містити щонайменше 5 слів.")
        return message