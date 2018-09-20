from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from . import main
from ..models import User, Question, Comment
from .forms import *
from .. import db
from datetime import datetime


@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home - Welcome to The best Movie Review Website Online'
    questions = Question.query.all()

    return render_template('index.html', title=title, questions=questions)


@main.route('/question/', methods=['GET', 'POST'])
@login_required
def new_question():
    form = QuestionForm()
    if form.validate_on_submit():

        content = form.content.data
        title = form.title.data
        category = form.category.data
        new_question = Question(
            content=content, title=title, category=category)
        db.session.add(new_question)
        db.session.commit()

    return render_template('question.html', question_form=form)


@main.route('/question/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_comment(id):
    '''
    view category that returns a form to create a new comment
    '''
    form = CommentForm()
    question = Question.query.filter_by(id=id).first()

    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data

        # comment instance
        new_comment = Comment(
            question_id=question.id, post_comment=comment, title=title, user=current_user)

        # save comment
        new_comment.save_comment()

        return redirect(url_for('.questions', id=question.id))

    title = f'{question.title} comment'
    return render_template('newcomment.html', title=title, comment_form=form, question=question)


@main.route('/allquestions')
def question_list():

    questions = Question.query.all()

    return render_template('question.html', questions=questions)


@main.route('/onequestion/<int:id>', methods=['GET', 'POST'])
def one_question(id):

    question = Question.query.get(id)
    form = CommentForm()
    question = question.query.filter_by(id=id).first()

    if form.validate_on_submit():
        # comment instance
        new_comment = Comment(
            ratings=0,
            like=0,
            dislike=0,
            content=form.content.data,
            time=datetime.utcnow(),
            comments=question,
            comment=current_user)

        # save comment
        db.session.add(new_comment)
        db.session.commit()

    comments = question.comments_id

    return render_template('viewquestion.html', question=question, id=id, comment_form=form, comments=comments)
