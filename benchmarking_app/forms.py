from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django_select2 import forms as s2forms


class PhaseEstablishmentChoice(forms.Form):
    """
    Used in analysis pages to make dropsdown widgets for phase type and establishment type selection.

    Phase type and establishment type choices must be passed from views as such:
    form = PhaseEstablishmentChoice(
            phase_choices=datacontainer.phase_choices,
            eastablishment_choices=datacontainer.establishment_choices,
        )
    """

    def __init__(self, *args, **kwargs):
        # Used to be able to pass year and placement choice arguments to the form.
        la_choices = kwargs.pop("la_choices")
        year_choices = kwargs.pop("year_choices")
        phase_choices = kwargs.pop("phase_choices")
        establishment_choices = kwargs.pop("establishment_choices")
        super(PhaseEstablishmentChoice, self).__init__(*args, **kwargs)

        # Single choice select for LA.
        self.fields["la"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select LA",
            required=True,
            choices=la_choices,
        )

        # Single choice select for year.
        self.fields["year"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select year",
            required=True,
            choices=year_choices,
        )

        # Single choice select for phase
        self.fields["phase"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select Phase Type",
            required=True,
            choices=phase_choices,
        )

        # Multi choice select for establishment types
        self.fields["establishment"] = forms.MultipleChoiceField(
            widget=s2forms.Select2MultipleWidget,
            label="Select Establishment Type(s)",
            required=False,
            choices=establishment_choices,
        )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Select Slices", css_class="btn-primary"))


class LAYearChoice(forms.Form):
    """
    Used in analysis pages to make dropsdown widgets for LA and year selection.

    Phase type and establishment type choices must be passed from views as such:
    form = LAYearChoice(
            la_choices=datacontainer.la_choices,
            year_choices=datacontainer.la_choices,
        )
    """

    def __init__(self, *args, **kwargs):
        # Used to be able to pass year and placement choice arguments to the form.
        la_choices = kwargs.pop("la_choices")
        year_choices = kwargs.pop("year_choices")
        super(LAYearChoice, self).__init__(*args, **kwargs)

        # Single choice select for LA.
        self.fields["la"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select LA",
            required=True,
            choices=la_choices,
        )

        # Single choice select for year.
        self.fields["year"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select year",
            required=True,
            choices=year_choices,
        )

    helper = FormHelper()
    helper.add_input(Submit("submit_la", "Select Slices", css_class="btn-primary"))
