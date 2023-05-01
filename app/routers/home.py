from flask import Blueprint, render_template

router = Blueprint('home', __name__, url_prefix="/")


@router.route('/', methods=['GET'])
def home():
    return render_template('home.html')
