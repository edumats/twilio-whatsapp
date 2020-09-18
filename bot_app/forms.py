from django import forms

class ReschedulingForm(forms.Form):
    DIA = 'D'
    HORA = 'H'
    ENDEREÇO = 'E'
    RESCHEDULE = [
        (DIA, 'Não posso receber o mecânico nesse dia'),
        (HORA, 'Não posso receber o mecânico nesse horário, mas posso nesse dia'),
        (ENDEREÇO, 'O endereço onde será realizado o serviço está errado')
    ]
    customer_issue = forms.ChoiceField(label='Selecione o motivo para reagendamento', choices=RESCHEDULE, widget=forms.CheckboxSelectMultiple)
    comment = forms.CharField(label='Observações', widget=forms.Textarea, required=False)
