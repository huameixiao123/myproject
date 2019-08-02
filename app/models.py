from .exts import db
import enum


class ContentAttachEnum(enum.Enum):
    kuozhanyuedu = 1
    cilianxi = 2
    julianxi = 3


class BookImageEnum(enum.Enum):
    catalog = 1
    preface = 2
    unit = 3


class ContentTypeEnum(enum.Enum):
    jingdu = 1
    fandu = 2
    review = 3


class User(db.Model):
    """
    用户表
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Book(db.Model):
    """
    教材表
    """
    __tablename__ = "book"
    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), nullable=False, default="")
    language_level = db.Column(db.String(1000), nullable=False, default="")
    vocleveltop = db.Column(db.Integer, nullable=False, default=0)
    voclevelbottom = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.String(1000), nullable=False, default="")
    coverimg = db.Column(db.String(200), nullable=False, default="")
    isbncoverimg = db.Column(db.String(200), nullable=False, default="")
    seriesname = db.Column(db.String(200), nullable=False, default="")
    booklevel = db.Column(db.String(50), nullable=False, default="")


class Attach(db.Model):
    """
    课文附件表
    """
    __tablename__ = "attach"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    attach_id = db.Column(db.Integer)
    sn = db.Column(db.Integer, nullable=False)  # 扩展阅读在书中的页码位置  内容附件序号
    type = db.Column(db.Enum(ContentAttachEnum), nullable=False)  # 附件类型。1：扩展阅读；2：练习（词）；3：练习（句）
    content = db.Column(db.Text, nullable=False, default="")
    from_name = db.Column(db.String(200), nullable=False, default="")
    note = db.Column(db.String(1000), nullable=False, default="")
    content_id = db.Column(db.ForeignKey("content.id", ondelete="CASCADE"))


class BookImage(db.Model):
    """
    教材图片表
    """
    __tablename__ = "book_image"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(1000), nullable=False, default="")
    type = db.Column(db.Enum(BookImageEnum), nullable=False)  # 1.使用说明 2.单元内容 3.目录
    sn = db.Column(db.Integer, nullable=False)  # 单元里面的页面序号 取页码
    refid = db.Column(db.Integer, nullable=True)  # 如果图片类型为使用说明或者目录，则refid为教材id；如果图片类型为单元，则refid为单元id
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete="CASCADE"))


class Task(db.Model):
    """
    任务表
    """
    __tablename__ = "task"
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete='CASCADE'))


class Unit(db.Model):
    """
    单元表
    """
    __tablename__ = "unit"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    unit_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    sn = db.Column(db.Integer, nullable=False)  # 页码
    note = db.Column(db.String(1000), nullable=False, default="")
    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id", ondelete='CASCADE'))

    def get_info(self):
        book = Book.query.filter_by(book_id=self.book_id).first()
        return {
            "unit": self,
            "book": book,
        }


class Content(db.Model):
    """
    课文表
    """
    __tablename__ = "content"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content_id = db.Column(db.Integer)
    title = db.Column(db.String(200), nullable=False, default="")
    content = db.Column(db.Text, nullable=True, default="")
    content_from_name = db.Column(db.String(200), nullable=False, default="")
    content_prefix = db.Column(db.String(200), nullable=False, default="")
    content_origin = db.Column(db.Text, nullable=False, default="")
    content_type = db.Column(db.Enum(ContentTypeEnum), nullable=False)  # 内容类型。1：精度课文；2：泛读课文；3：复习
    sn = db.Column(db.Integer, nullable=False)  # 页码
    note = db.Column(db.String(1000), nullable=False, default='‘’')
    unit_id = db.Column(db.ForeignKey("unit.id", ondelete="CASCADE"))

    def get_info(self):
        unit = Unit.query.filter_by(id=self.unit_id).first()
        book = Book.query.filter_by(book_id=unit.book_id).first()
        return {
            "unit": unit,
            "book": book
        }
