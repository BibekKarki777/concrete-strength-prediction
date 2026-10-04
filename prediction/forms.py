from django import forms


class PredictionForm(forms.Form):
    # Units match the headers in ml/data/concrete_compressive_strength.csv.
    cement = forms.FloatField(
        help_text="kg per cubic metre of mixture",
        min_value=102.0,
        max_value=540.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "any"})
    )

    blast_furnace_slag = forms.FloatField(
        help_text="kg per cubic metre of mixture",
        min_value=0.0,
        max_value=359.4,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "any"})
    )

    fly_ash = forms.FloatField(
        help_text="kg per cubic metre of mixture",
        min_value=0.0,
        max_value=200.1,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "any"})
    )

    water = forms.FloatField(
        help_text="kg per cubic metre of mixture",
        min_value=121.8,
        max_value=247.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "any"})
    )

    superplasticizer = forms.FloatField(
        help_text="kg per cubic metre of mixture",
        min_value=0.0,
        max_value=32.2,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "any"})
    )

    coarse_aggregate = forms.FloatField(
        help_text="kg per cubic metre of mixture",
        min_value=801.0,
        max_value=1145.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "any"})
    )

    fine_aggregate = forms.FloatField(
        help_text="kg per cubic metre of mixture",
        min_value=594.0,
        max_value=992.6,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "any"})
    )

    age = forms.IntegerField(
        help_text="days",
        min_value=1,
        max_value=365,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["aria-describedby"] = self[name].auto_id + "_helptext"
