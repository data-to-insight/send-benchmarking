from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, Row
from django import forms
from django_select2 import forms as s2forms


class SingleYearChoice(forms.Form):
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
        super(SingleYearChoice, self).__init__(*args, **kwargs)

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
    helper.layout = Layout(
        Row(
            Field("la", wrapper_class="form-group col-md-3 mb-0"),
            Field("year", wrapper_class="form-group col-md-3 mb-0"),
            Field("phase", wrapper_class="form-group col-md-3 mb-0"),
            Field("establishment", wrapper_class="form-group col-md-3 mb-0"),
        ),
    )


class SingleYearChoiceEHCP(forms.Form):
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
        breakdown_topic_choices = kwargs.pop("breakdown_topic_choices")
        breakdown_choices = kwargs.pop("breakdown_choices")
        measure_choices = kwargs.pop("measure_choices")
        super(SingleYearChoiceEHCP, self).__init__(*args, **kwargs)

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

        # Single choice select for breakdown topic
        self.fields["breakdown_topic"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select Breakdown Topic",
            required=True,
            choices=breakdown_topic_choices,
        )

        # Single choice select for breakdown
        self.fields["breakdown"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select Breakdown",
            required=True,
            choices=breakdown_choices,
        )

        # Single choice select for breakdown
        self.fields["measure"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select Measure",
            required=True,
            choices=measure_choices,
        )

    helper = FormHelper()
    helper.add_input(Submit("submit", "Select Slices", css_class="btn-primary"))
    helper.layout = Layout(
        Row(
            Field("la", wrapper_class="form-group col-md-6 mb-0"),
            Field("year", wrapper_class="form-group col-md-6 mb-0"),
        ),
        Row(
            Field("breakdown_topic", wrapper_class="form-group col-md-4 mb-0"),
            Field("breakdown", wrapper_class="form-group col-md-4 mb-0"),
            Field("measure", wrapper_class="form-group col-md-4 mb-0"),
        ),
    )


class TrendChoice(forms.Form):
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
        phase_choices = kwargs.pop("phase_choices")
        establishment_choices = kwargs.pop("establishment_choices")
        super(TrendChoice, self).__init__(*args, **kwargs)

        # Single choice select for LA.
        self.fields["la"] = forms.ChoiceField(
            widget=s2forms.Select2Widget,
            label="Select LA",
            required=True,
            choices=la_choices,
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
    helper.layout = Layout(
        Row(
            Field("la", wrapper_class="form-group col-md-4 mb-0"),
            Field("phase", wrapper_class="form-group col-md-4 mb-0"),
            Field("establishment", wrapper_class="form-group col-md-4 mb-0"),
        ),
    )
