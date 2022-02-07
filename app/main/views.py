from . import main
from flask import render_template, url_for, abort, request, redirect
from flask_login import login_required, current_user
from ..models import User, Pitch, Upvote, Downvote, Comment
from .forms import UpdateForm, PitchForm, CommentForm
from .. import db, photos


@main.route('/')
def index():
    """main view function"""
    all_pitches = Pitch.query.all()
    title = "Flask Pitch Application"
    return render_template("index.html", all_pitches=all_pitches, title=title)


@main.route('/profile/<my_name>')
@login_required
def profile(my_name):
    title = "Flask Profile"
    user = User.query.filter_by(username=my_name).first()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, title=title)


@main.route('/update/<my_name>', methods=['GET', 'POST'])
@login_required
def edit_profile(my_name):
    title = "Edit profile"
    user = User.query.filter_by(username=my_name).first()
    if user is None:
        abort(404)
    update_form = UpdateForm()
    if update_form.validate_on_submit():
        user.biography = update_form.biography.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', my_name=user.username))

    return render_template("profile/update.html", update_form=update_form, title=title)


@main.route('/updateImage/<my_name>', methods=['POST'])
@login_required
def update_image(my_name):
    title = "Update image"
    user = User.query.filter_by(username=my_name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic = path
        db.session.commit()
    return redirect(url_for('main.profile', my_name=my_name, title=title))


@main.route('/new-pitch/<id>', methods=['GET', 'POST'])
@login_required
def pitch(id):
    """New Pitch function"""
    title = "New Pitch"
    pitch_form = PitchForm()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        category = pitch_form.category.data
        pitch = pitch_form.pitch.data

        new_pitch = Pitch(title=title, category=category, pitch=pitch, user=current_user)

        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    return render_template('pitch.html', pitch_form=pitch_form, title=title)


@main.route('/upvote/<id>', methods=['GET', 'POST'])
@login_required
def upVote(id):
    votes = Upvote.get_upvotes(id)
    output = f'{current_user.id}:{id}'
    for vote in votes:
        result = f'{vote}'
        if output == result:
            return redirect(url_for('main.index', id=id))
        else:
            continue
    new_upvote = Upvote(user=current_user, pitch_id=id)
    new_upvote.save()
    return redirect(url_for('main.index', id=id))


@main.route('/downvote/<id>', methods=['GET', 'POST'])
@login_required
def downVote(id):
    votes = Downvote.get_downvotes(id)
    output = f'{current_user.id}:{id}'
    for vote in votes:
        result = f'{vote}'
        if output == result:
            return redirect(url_for('main.index', id=id))
        else:
            continue
    new_downvote = Downvote(user=current_user, pitch_id=id)
    new_downvote.save()
    return redirect(url_for('main.index', id=id))


@main.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    pitch = Pitch.query.get(id)
    fetch_all_comments = Comment.query.filter_by(pitch_id=id).all()
    if comment_form.validate_on_submit():
        comment = comment_form.comment.data
        pitch_id = id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment=comment, user_id=user_id, pitch_id=pitch_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', id=pitch_id))
    return render_template('comments.html', comment_form=comment_form, pitch=pitch, all_comments=fetch_all_comments)


#######################################Categories##################################
# pickup lines, interview pitch, product pitch, promotion pitch.
@main.route('/pickup')
def pickup():
    # pitches = Pitch.query.all()
    title="Pickup Line Pitch"
    pickup = Pitch.query.filter_by(category='pickup').all()
    return render_template('category/pickup.html', all_pitches=pickup,title=title)

@main.route('/interview')
def interview():
    # pitches = Pitch.query.all()
    title="Interview Pitch"
    interview = Pitch.query.filter_by(category='interview').all()
    return render_template('category/interview.html', all_pitches=interview,title=title)

@main.route('/product')
def product():
    # pitches = Pitch.query.all()
    title="Product Pitch"
    product = Pitch.query.filter_by(category='product').all()
    return render_template('category/product.html', all_pitches=product,title=title)

@main.route('/promotion')
def promotion():
    # pitches = Pitch.query.all()
    title="Promotion Pitch"
    promotion = Pitch.query.filter_by(category='promotion').all()
    print(promotion)
    return render_template('category/promotion.html', all_pitches=promotion,title=title)