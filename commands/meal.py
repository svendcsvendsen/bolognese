import constants
import os
import sys
import subprocess
import yaml
from meal import Meal
from food import Food
from dictionary_helpers import update_dictionary

def root_handle(args):
    for root, dirs, files in os.walk(constants.MEALS_DIR):
        for f in files:
            if root == constants.MEALS_DIR:
                print(f)
            else:
                print(root[len(constants.MEALS_DIR)+1:] + '/' + f)

def edit_handle(args):
    meal = Meal(args.meal)
    vargs = vars(args)

    if args.servings is None:
        subprocess.call([constants.EDITOR, meal.path()])
    else:
        if meal.exists():
            meal.load()
        meal.update(vargs)
        meal.save()

def edit_register(parent):
    edit_parser = parent.add_parser('edit')
    edit_parser.set_defaults(func=edit_handle)
    edit_parser.add_argument('meal', type=str, help='Set the number of foo')
    edit_parser.add_argument('--servings', type=str, nargs='+', help='Set the number of foo')

def add_handle(args):
    meal = Meal(args.meal)
    vargs = vars(args)

    if meal.exists():
        print("The meal '{}' already exists.".format(args.meal), file=sys.stderr)
        return

    if args.servings is None:
        subprocess.call([constants.EDITOR, meal.path()])
    else:
        meal.load()
        meal.update(vargs)
        meal.save()

def add_register(parent):
    parser = parent.add_parser('edit')
    parser.set_defaults(func=add_handle)
    parser.add_argument('meal', type=str, help='Set the number of foo')
    parser.add_argument('--servings', type=str, nargs='+', help='Set the number of foo')

def add_food_handle(args):
    meal = Meal(args.meal)
    food = Food(args.food)
    vargs = vars(args)

    if not meal.exists():
        print("The meal '{}' does not exist.".format(args.meal), file=sys.stderr)
        return

    if not food.exists():
        print("The food '{}' does not exist.".format(args.food), file=sys.stderr)
        return

    food.load()

    if not food.servings.is_valid_serving(args.serving):
        print("The serving '{}' is not a valid serving for the given food.".format(args.serving), file=sys.stderr)
        return

    meal.load()
    meal.add_food(args.food, args.serving)
    meal.save()

def add_food_register(parent):
    parser = parent.add_parser('add-food')
    parser.set_defaults(func=add_food_handle)
    parser.add_argument('meal', type=str, help='Set the number of foo')
    parser.add_argument('food', type=str, help='Set the number of foo')
    parser.add_argument('serving', nargs="?", type=str, default='1', help='Set the number of foo')

def log_handle(args):
    print("Log handler")

def log_register(parent):
    log_parser = parent.add_parser('log')
    log_parser.set_defaults(func=log_handle)
    log_parser.add_argument('meal', type=str, help='Set the number of foo')
    log_parser.add_argument('amount', type=str, help='Set the number of foo')

def register(parent):
    parser = parent.add_parser('meal', help='meal help')
    parser.set_defaults(func=root_handle)
    subparsers = parser.add_subparsers(help='subsub parser help')

    edit_register(subparsers)
    log_register(subparsers)
    add_register(subparsers)
    add_food_register(subparsers)

    # remove, add, edit, log
