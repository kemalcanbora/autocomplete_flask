from flask import Flask, request, render_template, current_app
from flask_wtf import Form
from wtforms.validators import DataRequired
from wtforms import SelectField, SelectMultipleField, SubmitField


app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY = 'your_secret_key',
    CSRF_ENABLED = True,
))


class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class DemoForm(Form):

    must_multi_select = Select2MultipleField(u"Talents", [],
            choices=[("py", "python"), ("rb", "ruby"), ("js", "javascript")],
            description=u"must skills",
            render_kw={"multiple": "multiple"})

    nice_multi_select = Select2MultipleField(u"Talents", [],
                                             choices=[("aa", "aa"), ("rr", "rr"), ("jj", "jj")],
                                             description=u"nice to have skills",
                                             render_kw={"multiple": "multiple"})

    submit = SubmitField()


@app.route("/", methods=["GET", "POST"])
def home():
    form = DemoForm(request.form)

    if form.validate_on_submit():
        current_app.logger.debug(form.data)

        print(form.data["nice_multi_select"])
        print(form.data["must_multi_select"])
    return render_template("demo.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)