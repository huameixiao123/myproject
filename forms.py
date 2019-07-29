from wtforms import Form, StringField, FileField, IntegerField,TextAreaField,SelectField
from wtforms.validators import InputRequired, Length


class IntegerFieldBat(IntegerField):

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0]:
                try:
                    self.data = int(valuelist[0])
                except ValueError:
                    self.data = None
                    raise ValueError(self.gettext('填写内容必须是数字类型'))


class AddBookForm(Form):
    name = StringField(validators=[InputRequired("名字必须填写"), Length(0, 200, message="最大长度是200个字符")])
    isbn = StringField(validators=[Length(0,20,message="最大长度是20个字符")])
    language_level = StringField(validators=[Length(0,1000,message="最大长度是1000个字符")])
    vocleveltop = IntegerFieldBat()
    voclevelbottom = IntegerFieldBat()
    note = StringField(validators=[Length(0,1000,message="最大长度是1000个字符")])
    coverimg = StringField(validators=[Length(0,200,message="最大长度是200个字符")])
    isbncoverimg = StringField(validators=[Length(0,200,message="最大长度是200个字符")])
    seriesname = StringField(validators=[Length(0,200,message="最大长度是200个字符")])
    booklevel = StringField(validators=[Length(0,50,message="最大长度是50个字符")])

class AddContentForm(Form):
    content_id = IntegerFieldBat(validators=[InputRequired("课文序号必须填写")])
    title = StringField(validators=[Length(0,200,message="最大长度是200个字符"),InputRequired("标题必须填写")])
    content = StringField(validators=[Length(0,200,message="最大长度是200个字符")])
    content_from_name = StringField(validators=[Length(0,200,message="最大长度是200个字符")])
    content_prefix = StringField(validators=[Length(0,200,message="最大长度是200个字符")])
    content_origin = TextAreaField()
    content_type = SelectField(choices=((1,"精读"),(2,"泛读"),(3,"复习")),coerce=int,validators=[InputRequired("课文类型必须填写")])
    sn = IntegerFieldBat(validators=[InputRequired("课文页码必须填写")])
    note = StringField(validators=[Length(0,1000,message="最大长度是1000个字符")])
    unit_id = IntegerFieldBat()

class EditContentForm(Form):
    title = StringField(validators=[Length(0, 200, message="最大长度是200个字符"), InputRequired("标题必须填写")])
    content = StringField(validators=[Length(0, 200, message="最大长度是200个字符")])
    content_from_name = StringField(validators=[Length(0, 200, message="最大长度是200个字符")])
    content_prefix = StringField(validators=[Length(0, 200, message="最大长度是200个字符")])
    content_origin = TextAreaField()
    content_type = SelectField(choices=((1, "精读"), (2, "泛读"), (3, "复习")), coerce=int,
                               validators=[InputRequired("课文类型必须填写")])
    sn = IntegerFieldBat(validators=[InputRequired("课文页码必须填写")])
    note = StringField(validators=[Length(0, 1000, message="最大长度是1000个字符")])


