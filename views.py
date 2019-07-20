from functools import wraps

import os
from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify, send_from_directory

from exts import db
from models import User, Book, Unit, Task, BookImage, Content, Attach, BookImageEnum, ContentTypeEnum, ContentAttachEnum
from forms import AddBookForm, AddContentForm, EditContentForm

bp = Blueprint("book", __name__)

UPLOAD_PATH = os.path.join(os.path.dirname(__file__), "book_image")


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if "user_id" in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('book.login'))

    return inner


@bp.route("/del_attach/<int:content_id>", methods=["GET", "POST"])
# @login_required
def del_attach(content_id):
    if request.method == "GET":
        attachs = Attach.query.filter_by(content_id=content_id)
        return render_template("del_attach.html", attachs=attachs)
    if request.method == "POST":
        del_ids = request.form.getlist("del")
        for i in del_ids:
            attach = Attach.query.filter_by(id=int(i)).first()
            db.session.delete(attach)
        db.session.commit()
        return redirect(url_for("book.attach_manage", content_id=content_id))


@bp.route("/edit_attach/<int:attach_id>/", methods=["GET", "POST"])
# @login_required
def edit_attach(attach_id):
    if request.method == "GET":
        attach = Attach.query.filter_by(id=attach_id).first()
        return render_template("edit_attach.html", attach=attach, message=None)
    if request.method == "POST":
        # attach_id = request.form.get("attach_id")
        # if not attach_id:
        #     render_template("add_attach.html", message={"attach_id": "扩展阅读序号必须填写"})
        sn = request.form.get("sn")
        if not sn:
            render_template("add_attach.html", message={"sn": "扩展阅读页码必须填写"})
        type = request.form.get("type")
        if not type:
            render_template("add_attach.html", message={"type": "扩展阅读类型必须填写"})
        if type == "1":
            type = ContentAttachEnum.kuozhanyuedu

        if type == "2":
            type = ContentAttachEnum.cilianxi
        if type == "3":
            type = ContentAttachEnum.julianxi

        content = request.form.get("content")
        note = request.form.get("note")
        from_name = request.form.get("from_name")

        info = {
            "attach_id": attach_id,
            "sn": sn,
            "type": type,
            "content": content,
            "note": note,
            "from_name": from_name

        }

        db.session.query(Attach).filter_by(id=attach_id).update(info)
        db.session.commit()
        attach = Attach.query.filter_by(id=attach_id).first()
        return redirect(url_for("book.attach_manage", content_id=attach.content_id))


@bp.route("/add_attach/<int:content_id>/", methods=["GET", "POST"])
# @login_required
def add_attach(content_id):
    if request.method == "GET":
        return render_template("add_attach.html", message=None)
    if request.method == "POST":
        attach_id = request.form.get("attach_id")
        if not attach_id:
            return render_template("add_attach.html", message={"attach_id": "扩展阅读序号必须填写"})
        sn = request.form.get("sn")
        if not sn:
            return render_template("add_attach.html", message={"sn": "扩展阅读页码必须填写"})
        type = request.form.get("type")
        if not type:
            return render_template("add_attach.html", message={"type": "扩展阅读类型必须填写"})
        if type == "1":
            type = ContentAttachEnum.kuozhanyuedu

        if type == "2":
            type = ContentAttachEnum.cilianxi
        if type == "3":
            type = ContentAttachEnum.julianxi

        content = request.form.get("content")
        note = request.form.get("note")
        from_name = request.form.get("from_name")
        attach = Attach(content_id=content_id, sn=sn, type=type, content=content, note=note, from_name=from_name,
                        attach_id=attach_id)
        db.session.add(attach)
        db.session.commit()
        return redirect(url_for("book.attach_manage", content_id=content_id))


@bp.route("/attach_manage/<int:content_id>/", methods=["GET"])
# @login_required
def attach_manage(content_id):
    attachs = Attach.query.filter_by(content_id=content_id).order_by("attach_id").all()
    return render_template("attach_manage.html", content_id=content_id, attachs=attachs)


@bp.route("/del_unit_content/<int:unit_id>/", methods=["GET", "POST"])
# @login_required
def del_unit_content(unit_id):
    if request.method == "GET":
        contents = Content.query.all()
        return render_template("del_unit_content.html", contents=contents)
    if request.method == "POST":
        del_ids = request.form.getlist("del")
        for i in del_ids:
            content = Content.query.filter_by(content_id=int(i), unit_id=unit_id).first()
            db.session.delete(content)
        db.session.commit()
        return redirect(url_for("book.unit_content_manage", unit_id=unit_id))


@bp.route("/edit_unit_content/<int:content_id>/", methods=["GET", "POST"])
# @login_required
def edit_unit_content(content_id):
    if request.method == "GET":
        content = Content.query.filter_by(id=content_id).first()
        return render_template("edit_unit_content.html", content=content, errors=None)
    if request.method == "POST":
        form = EditContentForm(request.form)
        if form.validate():
            title = request.form.get("title")
            content = request.form.get("content")
            content_from_name = request.form.get("content_from_name")
            content_prefix = request.form.get("content_prefix")
            content_origin = request.form.get("content_origin")
            content_type = request.form.get("content_type")
            if content_type == "1":
                content_type = ContentTypeEnum.jingdu
            if content_type == "2":
                content_type = ContentTypeEnum.fandu
            if content_type == "3":
                content_type = ContentTypeEnum.review
            note = request.form.get("note")
            sn = request.form.get("sn")

            new_content = {
                "title": title,
                "content": content,
                "content_from_name": content_from_name,
                "content_prefix": content_prefix,
                "content_origin": content_origin,
                "content_type": content_type,
                "note": note,
                "sn": sn
            }
            db.session.query(Content).filter_by(id=content_id).update(new_content)
            db.session.commit()
            return redirect(url_for("book.content_detail", content_id=content_id))
        else:
            print(form.errors)
            content = Content.query.filter_by(id=content_id).first()
            return render_template("edit_unit_content.html", content=content, errors=form.errors)


@bp.route("/add_unit_content/<int:unit_id>/", methods=["GET", "POST"])
# @login_required
def add_unit_content(unit_id):
    if request.method == "GET":
        return render_template("add_unit_content.html", errors=None)
    if request.method == "POST":
        form = AddContentForm(request.form)
        if form.validate():
            content_id = form.data.get("content_id")
            title = form.data.get("title")
            content = form.data.get("content")
            content_from_name = form.data.get("content_from_name")
            content_prefix = form.data.get("content_prefix")
            content_origin = form.data.get("content_origin")
            content_type = form.data.get("content_type")
            if content_type == 1:
                content_type = ContentTypeEnum.jingdu

            if content_type == 2:
                content_type = ContentTypeEnum.fandu
            if content_type == 3:
                content_type = ContentTypeEnum.review
            sn = form.data.get("sn")
            note = form.data.get("note")

            unit_content = Content(content_id=content_id, title=title, content_type=content_type, content=content,
                                   content_from_name=content_from_name, unit_id=unit_id,
                                   content_prefix=content_prefix, content_origin=content_origin, sn=sn,
                                   note=note)
            db.session.add(unit_content)
            db.session.commit()
            return redirect(url_for("book.unit_content_manage", unit_id=unit_id))
        else:
            return render_template("add_unit_content.html", errors=form.errors)


@bp.route("/content_detail/<int:content_id>/", methods=["GET"])
def content_detail(content_id):
    content = db.session.query(Content).filter_by(id=content_id).first()
    return render_template("content_detail.html", content=content)


@bp.route("/unit_content_manage/<int:unit_id>/")
# @login_required
def unit_content_manage(unit_id):
    if request.method == "GET":
        contents = Content.query.filter_by(unit_id=unit_id).order_by("content_id").all()

        return render_template("unit_content_manage.html", contents=contents, unit_id=unit_id)


@bp.route("/del_unit_pic/<int:book_id>/<int:unit_id>/", methods=["GET", "POST"])
# @login_required
def del_unit_pic(book_id, unit_id):
    if request.method == "GET":
        pics = BookImage.query.filter_by(book_id=book_id, refid=unit_id, type=BookImageEnum.unit).all()
        return render_template("del_unit_pic.html", pics=pics)
    if request.method == "POST":

        units = request.form.getlist("unit")
        for i in units:
            bookimg = BookImage.query.filter_by(id=int(i)).first()
            db.session.delete(bookimg)
        db.session.commit()
        return render_template("red_page.html", path=url_for("book.unit_manage", book_id=book_id))


@bp.route("/add_unit_pic/<int:book_id>/<int:unit_id>/", methods=["GET", "POST"])
# @login_required
def add_unit_pic(book_id, unit_id):
    if request.method == "GET":
        return render_template("add_unit_pic.html")
    if request.method == "POST":
        sn = request.form.get("sn")
        if not sn:
            return render_template("add_unit_pic.html", message="请添加图片页码后在进行操作")
        unit_pic = request.files.get("unit_pic")
        if not unit_pic.filename:
            return render_template("add_unit_pic.html", message="请选择图片后在进行添加")
        # 写入磁盘
        path = os.path.join(UPLOAD_PATH, str(book_id), unit_pic.filename)
        unit_pic.save(path)
        # 保存数据库
        save_path = os.path.join("/book_image/", str(book_id), unit_pic.filename)
        bookimg = BookImage(path=save_path, type=BookImageEnum.unit, sn=sn, refid=unit_id, book_id=book_id)
        db.session.add(bookimg)
        db.session.commit()
        return redirect(url_for("book.unit_manage", book_id=book_id))


@bp.route("/del_unit/<int:book_id>/", methods=["GET", "POST"])
# @login_required
def del_unit(book_id):
    if request.method == "GET":
        units = Unit.query.filter_by(book_id=book_id).all()
        return render_template("del_unit.html", units=units)
    if request.method == "POST":
        units = request.form.getlist("unit")
        for i in units:
            unit = Unit.query.filter_by(unit_id=int(i), book_id=book_id).first()
            db.session.delete(unit)
        db.session.commit()
        return redirect(url_for("book.unit_manage", book_id=book_id))


@bp.route("/add_unit/<int:book_id>/", methods=["GET", "POST"])
# @login_required
def add_unit(book_id):
    if request.method == "GET":
        return render_template("add_unit.html")
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            return render_template("add_unit.html", message="单元名字必须填写")
        sn = request.form.get("sn")
        if not sn:
            return render_template("add_unit.html", message="单元页码必须填写")
        unit_id = request.form.get("unit_id")
        if not unit_id:
            return render_template("add_unit.html", message="单元ID必须填写")
        note = request.form.get("note")
        unit = Unit(sn=sn, name=name, note=note, book_id=book_id, unit_id=unit_id)
        db.session.add(unit)
        db.session.commit()
        return redirect(url_for("book.unit_manage", book_id=book_id))


@bp.route("/del_user_pic/<int:book_id>/", methods=["GET", "POST"])
# @login_required
def del_user_pic(book_id):
    if request.method == "GET":
        users = db.session.query(BookImage).filter_by(book_id=book_id, type=BookImageEnum.preface).all()
        return render_template("del_user.html", users=users)
    if request.method == "POST":
        user_ids = request.form.getlist("user")
        for user_id in user_ids:
            bookimg = db.session.query(BookImage).filter_by(id=user_id, book_id=book_id).first()
            db.session.delete(bookimg)
        db.session.commit()
        return redirect(url_for("book.unit_manage", book_id=book_id))


@bp.route("/add_user_pic/<int:book_id>/", methods=["GET", "POST"])
# @login_required
def add_user_pic(book_id):
    if request.method == "GET":
        return render_template("add_user.html")
    if request.method == "POST":
        user_pic = request.files.get("user")
        sn = request.form.get("sn")
        if not sn:
            return render_template("add_user.html", message="请先填写页码后在进行添加")
        if not user_pic.filename:
            return render_template("add_user.html", message="请先选择图片后在进行添加")

        # 写入磁盘
        path = os.path.join(UPLOAD_PATH, str(book_id), user_pic.filename)
        user_pic.save(path)
        # 保存数据库
        save_path = os.path.join("/book_image/", str(book_id), user_pic.filename)
        bookimg = BookImage(path=save_path, type=BookImageEnum.preface, sn=sn, refid=book_id, book_id=book_id)
        db.session.add(bookimg)
        db.session.commit()
        return redirect(url_for("book.unit_manage", book_id=book_id))


@bp.route("/del_cat_pic/<int:book_id>/", methods=["GET", "POST"])
# @login_required
def del_cat_pic(book_id):
    if request.method == "GET":
        cats = db.session.query(BookImage).filter_by(book_id=book_id, type=BookImageEnum.catalog).all()
        return render_template("del_cat.html", cats=cats)
    if request.method == "POST":
        cat_ids = request.form.getlist("cat")
        for cat_id in cat_ids:
            print(cat_id)
            bookimg = db.session.query(BookImage).filter_by(id=cat_id, book_id=book_id).first()
            db.session.delete(bookimg)
        db.session.commit()
        return redirect(url_for("book.unit_manage", book_id=book_id))


@bp.route("/add_cat_pic/<int:book_id>/", methods=["GET", "POST"])
# @login_required
def add_cat_pic(book_id):
    if request.method == "GET":
        return render_template("add_cat.html")
    if request.method == "POST":
        cat = request.files.get("cat")
        sn = request.form.get("sn")
        if not sn:
            return render_template("add_cat.html", message="请先填写页码后在进行添加")
        if not cat.filename:
            return render_template("add_cat.html", message="请先选择图片后在进行添加")

        # 写入磁盘
        path = os.path.join(UPLOAD_PATH, str(book_id), cat.filename)
        cat.save(path)
        # 保存数据库
        save_path = os.path.join("/book_image/", str(book_id), cat.filename)
        bookimg = BookImage(path=save_path, type=BookImageEnum.catalog, sn=sn, refid=book_id, book_id=book_id)
        db.session.add(bookimg)
        db.session.commit()
        return redirect(url_for("book.unit_manage", book_id=book_id))


@bp.route("/unit_manage/<int:book_id>/", methods=["GET"])
# @login_required
def unit_manage(book_id):
    cat_pics = db.session.query(BookImage).filter_by(refid=book_id, type=BookImageEnum.catalog).all()
    user_pics = db.session.query(BookImage).filter_by(refid=book_id, type=BookImageEnum.preface).all()
    units = db.session.query(Unit).filter_by(book_id=book_id).all()
    unit_pics = db.session.query(BookImage).filter_by(type=BookImageEnum.unit, book_id=book_id).all()
    data = {
        "book_id": book_id,
        "cat_pics": cat_pics,
        "user_pics": user_pics,
        "units": units,
        "unit_pics": unit_pics
    }
    return render_template("unit_manage.html", **data)


@bp.route("/delete_book/", methods=["GET"])
# @login_required
def delete_book():
    book_id = request.args.get("book_id")
    book = Book.query.filter_by(book_id=book_id).first()
    db.session.delete(book)
    user_id = session.get("user_id")
    task = Task.query.filter_by(user_id=user_id, book_id=book_id).first()
    if task:
        db.session.delete(task)
    db.session.commit()
    return jsonify({"code": 200})


@bp.route("/book_image/<book_id>/<file_name>")
# @login_required
def get_image(book_id, file_name):
    directory = os.path.join(UPLOAD_PATH, book_id)
    return send_from_directory(directory, file_name)


@bp.route("/book/edit/<book_id>", methods=["GET", "POST"])
# @login_required
def edit_book(book_id):
    if request.method == "GET":
        book = Book.query.filter_by(book_id=book_id).first()
        bookinfo = {
            "name": book.name,
            "isbn": book.isbn,
            "language_level": book.language_level,
            "vocleveltop": book.vocleveltop,
            "voclevelbottom": book.voclevelbottom,
            "note": book.note,
            "coverimg": book.coverimg,
            "isbncoverimg": book.isbncoverimg,
            "seriesname": book.seriesname,
            "booklevel": book.booklevel,
        }
        return render_template("edit_book.html", **bookinfo)

    if request.method == "POST":
        book = Book.query.filter_by(book_id=book_id).first()
        name = request.form.get("name")
        isbn = request.form.get("isbn")
        language_level = request.form.get("language_level")
        vocleveltop = request.form.get("vocleveltop")
        voclevelbottom = request.form.get("voclevelbottom")
        note = request.form.get("note")
        coverimg = request.files.get("coverimg")
        isbncoverimg = request.files.get("isbncoverimg")
        seriesname = request.form.get("seriesname")
        booklevel = request.form.get("booklevel")
        if coverimg.filename:
            coverimg_path = os.path.join(UPLOAD_PATH, book_id, coverimg.filename)
            coverimg.save(coverimg_path)
            coverimg_path_save = "/book_image/" + str(book_id) + "/" + coverimg.filename
        else:
            coverimg_path_save = book.coverimg
        if isbncoverimg.filename:
            isbncoverimg_path_save = "/book_image/" + str(book_id) + "/" + isbncoverimg.filename
            isbncoverimg_path = os.path.join(UPLOAD_PATH, book_id, isbncoverimg.filename)
            isbncoverimg.save(isbncoverimg_path)
        else:
            isbncoverimg_path_save = book.isbncoverimg

        new_book = {
            "name": name,
            "isbn": isbn,
            "language_level": language_level,
            "vocleveltop": vocleveltop,
            "voclevelbottom": voclevelbottom,
            "note": note,
            "coverimg": coverimg_path_save,
            "isbncoverimg": isbncoverimg_path_save,
            "seriesname": seriesname,
            "booklevel": booklevel,
        }

        db.session.query(Book).filter_by(book_id=book_id).update(new_book)
        db.session.commit()
        return redirect(url_for("book.book_list", page=1))


@bp.route("/book/add/", methods=["GET", "POST"])
## @login_required
def add_book():
    if request.method == "GET":
        return render_template("add_book.html")

    if request.method == "POST":
        form = AddBookForm(request.form, request.files)
        if form.validate():
            name = request.form.get("name")
            isbn = request.form.get("isbn")
            language_level = request.form.get("language_level")
            vocleveltop = request.form.get("vocleveltop")
            voclevelbottom = request.form.get("voclevelbottom")
            note = request.form.get("note")
            seriesname = request.form.get("seriesname")
            booklevel = request.form.get("booklevel")
            book = Book(name=name, isbn=isbn, language_level=language_level,
                        voclevelbottom=voclevelbottom,
                        vocleveltop=vocleveltop, note=note,
                        seriesname=seriesname, booklevel=booklevel)
            db.session.add(book)
            db.session.commit()

            book_id = Book.query.filter_by(name=name).first().book_id
            if not os.path.exists(os.path.join(UPLOAD_PATH, str(book_id))):
                os.mkdir(os.path.join(UPLOAD_PATH, str(book_id)))

            coverimg = request.files.get("coverimg")
            if coverimg.filename:
                coverimg_path = os.path.join(UPLOAD_PATH, str(book_id), coverimg.filename)
                coverimg.save(coverimg_path)
            isbncoverimg = request.files.get("isbncoverimg")
            if isbncoverimg.filename:
                isbncoverimg_path = os.path.join(UPLOAD_PATH, str(book_id), isbncoverimg.filename)
                isbncoverimg.save(isbncoverimg_path)

            coverimg_path_save = "/book_image/" + str(book_id) + "/" + coverimg.filename
            isbncoverimg_path_save = "/book_image/" + str(book_id) + "/" + isbncoverimg.filename
            info = {
                "coverimg": coverimg_path_save,
                "isbncoverimg": isbncoverimg_path_save
            }
            db.session.query(Book).filter_by(book_id=book_id).update(info)
            db.session.commit()

            # task = Task(user_id=session["user_id"],book_id=book_id)
            # db.session.add(task)
            # db.session.commit()

            return redirect(url_for("book.book_list", page=1))
        else:
            print(form.errors)
            return render_template("add_book.html", **form.errors)


@bp.route("/index/", methods=["GET"])
## @login_required
def index():
    return render_template("index.html")


@bp.route("/book_list/<int:page>/", methods=["GET"])
# @login_required
def book_list(page=None):
    if not page:
        page = 1
    books = Book.query.paginate(page=page, per_page=10)
    data = {
        "books": books,
    }

    return render_template("book_list.html", **data)


@bp.route('/logout/')
# # @login_required
def logout():
    del session["user_id"]
    return redirect(url_for('book.login'))


@bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            return redirect(url_for("book.index"))
        else:
            return render_template("login.html", message="用户名或者密码错误")


@bp.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html")
