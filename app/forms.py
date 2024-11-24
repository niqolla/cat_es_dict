from django import forms

AUTO_CHOICES = [(i, i ) for i in ['', 'ALFA ROMEO', 'AUDI', 'CHEVROLET', 'CITROEN', 'DACIA',
                                    'FIAT', 'FORD', 'HYUNDAI', 'KIA', 'LANCIA', 'MAZDA',
                                    'MERCEDES', 'MINI', 'MITSUBISHI', 'NISSAN', 'OPEL', 'PEUGEOT', 
                                    'RENAULT', 'SEAT', 'SKODA', 'SUZUKI', 'TOYOTA', 'VAUXHALL', 
                                    'VOLVO', 'VW']]

SNAGA_CHOICES = [(i, i) for i in ['', 50, 51, 65, 66, 68, 70, 75, 80, 82, 86, 88, 89, 90, 92, 94, 95, 
                                    100, 102, 103, 104, 105, 106, 107, 109, 110, 114, 115, 120, 127, 
                                    130, 138, 140, 150, 163, 170]]

CMM_CHOICES = [(i, i) for i in ['', '1', '1.25', '1.3', '1.4', '1.46', '1.5', '1.6', '1.7', '1.8',
                                    '1.9', '2.0', '2.1', '2.2', '2.5', 'I.4', 'T.4']]


class TurbiniForm(forms.Form):
    auto = forms.ChoiceField(choices=AUTO_CHOICES, label='Auto', required=False)
    CCM = forms.ChoiceField(choices=CMM_CHOICES, label='CCM', required=False)
    HP = forms.ChoiceField(choices=SNAGA_CHOICES, label='HP', required=False)

    shifra = forms.CharField(max_length=100, label='Shifra', required=False, 
                             widget=forms.TextInput(attrs={'placeholder': 'Shifra ili OE'}))
