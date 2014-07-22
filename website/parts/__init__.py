from flask import Blueprint, render_template, abort, redirect, request

parts = Blueprint("parts",__name__,template_folder="templates",static_folder="static")

@parts.route('/')
def index():
	return abort(404)
