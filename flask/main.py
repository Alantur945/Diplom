from flask import Flask, make_response, redirect, render_template, request
from loguru import logger
from sqlalchemy import select, exists
from database.base import generate_tables
from database.create_engine import engine
from sqlalchemy.orm import Session
from database.models import *
import secrets
from datetime import datetime

# generate_tables(engine)

app = Flask(__name__, static_folder='assets',)


def serialize_datetime(obj):
    """функция для сериализации времени.
    Встроенный во фласк сериализатор не может пребразовать datetime в строку
    """
    if isinstance(obj, datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 


def get_user_by_token():
    with Session(autoflush=False, bind=engine) as session:
        if "session" not in request.cookies:
            return None
        token = request.cookies["session"]
        token = session.execute(select(Token).where(Token.token==token)).scalar_one_or_none()
        if token:
            user = session.get(User, token.user)
            return user

@app.route("/")
def index():
    """Роут главной страницы"""
    user = get_user_by_token()
    with Session(autoflush=False, bind=engine) as session:
        products = session.execute(select(Product).limit(3)).scalars().all()
    return render_template("index.html", products=products)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """Роут авторизации"""
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")
        
        with Session(autoflush=False, bind=engine) as session:
            user = session.execute(select(User).where(User.username==username)).scalar_one_or_none()
            if user:
                token = session.execute(select(Token).where(Token.user==user.id)).scalar_one_or_none()
            else:
                token = None
        if token:
            resp = make_response(redirect("/"))
            resp.set_cookie('session', token.token)
            return resp
        if user:
            if user.password == password:
                token = secrets.token_urlsafe(16)
                token_object = Token()
                token_object.token = token
                token_object.user = user.id
                session.add(token_object)
                session.commit()
                resp = make_response(redirect("/"))
                resp.set_cookie('session', token)
                return resp
        return render_template("login.html", errors="Неверный логин или пароль")
    return render_template("login.html")


@app.get("/catalog")
def catalog():
    """Роут каталога"""
    user = get_user_by_token()
    sort = request.args.get('sort')
    with Session(autoflush=False, bind=engine) as session:
        if sort == "price":
            products = session.execute(select(Product).order_by(Product.price.asc())).scalars().all()
        else:
            products = session.execute(select(Product).order_by(Product.date.desc())).scalars().all()
        
    return render_template("shop.html", products=products, user=user)
    
@app.route("/products/add", methods=['GET', 'POST'])
def add_prod():
    """Роут добавления продукта"""
    user = get_user_by_token()
    if not user.is_admin:
        return {"error": "admins only"}
    
    if request.method == "GET":
        return render_template("add_product.html")
    else:
        name = request.form.get("name")
        articule = request.form.get("articule")
        price = request.form.get("price")
        description = request.form.get("description")
        photo = request.files.get("photo")
        path = "assets/img/user_files/" + photo.filename
        photo.save(path)
        
        with Session(autoflush=False, bind=engine) as session:
            q = session.query(exists().where(Product.articule == articule)).scalar()
            if q:
                return render_template("add_product.html", error=error)
            product = Product()
            product.name = name
            product.articule = articule
            product.price = price
            product.description = description
            product.photo = path

            session.add(product)
            session.commit()
        
        return render_template("add_product.html", success=True)


@app.route("/product/delete/<id>", methods=['GET'])
def delete(id: int):
    """Роут удаления продукта"""
    user = get_user_by_token()
    if not user.is_admin:
        return {"error": "admins only"}
    with Session(autoflush=False, bind=engine) as session:
        
        product = session.get(Product, id)
        session.delete(product)
        session.commit()
        
        return redirect("/catalog")
    
    
@app.route("/product/<id>", methods=['GET'])
def detail(id):
    """Роут детальной страницы ттовара"""
    with Session(autoflush=False, bind=engine) as session:
        product = session.get(Product, id)
        
    return render_template("shop-single.html", product=product)


@app.route("/delete_by_art", methods=["POST"])
def delete_by_atr():
    """Роут удаления товара по артикулу"""
    art = request.form.get("art")
    with Session(autoflush=False, bind=engine) as session:
        product =  session.execute(select(Product).where(Product.articule==art)).scalar_one_or_none()

        if product:
            session.delete(product)
            session.commit()

    return redirect("/catalog")


if __name__ == '__main__':
    app.run(debug=True)
