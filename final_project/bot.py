from copy import deepcopy
import logging
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import os

# os.environ['TG_TOKEN'] = ...

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# get token using BotFather
TOKEN = os.getenv('TG_TOKEN')

CONTINUE_GAME, FINISH_GAME = range(2)

FREE_SPACE = '.'
CROSS = 'X'
ZERO = 'O'


DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]


def get_default_state():
    """Helper function to get default state of the game"""
    return deepcopy(DEFAULT_STATE)


def generate_keyboard(state: list[list[str]]) -> list[list[InlineKeyboardButton]]:
    """Generate tic tac toe keyboard 3x3 (telegram buttons)"""
    return [
        [
            InlineKeyboardButton(state[r][c], callback_data=f'{r}{c}')
            for r in range(3)
        ]
        for c in range(3)
    ]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    context.user_data['keyboard_state'] = get_default_state()
    keyboard = generate_keyboard(context.user_data['keyboard_state'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Ваш ход! Поставьте крестик в любой свободной кнопке', reply_markup=reply_markup)
    return CONTINUE_GAME


async def change_message(update: Update, context: ContextTypes.DEFAULT_TYPE, new_msg: str):
    keyboard = generate_keyboard(context.user_data["keyboard_state"])
    await update.callback_query.edit_message_text(reply_markup=InlineKeyboardMarkup(keyboard), text=new_msg)


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Main processing of the game
    :param update
    :param context
    :return either CONTINUE_GAME if there is no winner yet or FINISH_GAME if there is a winner
    """
    cur_state = context.user_data["keyboard_state"]
    new_game_msg = "Чтобы начать заново, введите /start"

    # update.callback_query.data - it's a string "cr", where c is column and r is row

    row, column = map(int, update.callback_query.data)
    if cur_state[row][column] is not FREE_SPACE:
        return CONTINUE_GAME
    cur_state[row][column] = CROSS

    if won(cur_state):
        await change_message(update, context, f"Победа! :) {new_game_msg}")
        return FINISH_GAME

    cells_for_zeros = [(i // 3, i % 3) for i in range(9) if cur_state[i // 3][i % 3] is FREE_SPACE]

    if len(cells_for_zeros) == 0:
        await change_message(update, context, f"Ничья! {new_game_msg}")
        return FINISH_GAME

    column, row = -1, -1
    # write a simple algorithm for choosing a place for zero:
    # if is sees a potential won row or column or diagonal for crosses
    # it will put zero into this column or row to stop you from easy win
    for (c, r) in cells_for_zeros:
        if (
                ((c + 1) % 3, (r + 1) % 3) not in cells_for_zeros and ((c + 2) % 3, (r + 2) % 3) not in cells_for_zeros
                and cur_state[(c + 1) % 3][(r + 1) % 3] == ZERO and cur_state[(c + 2) % 3][(r + 2) % 3] == ZERO
                and c == r
        ) or (
            ((c - 1) % 3, (r + 1) % 3) not in cells_for_zeros and ((c - 2) % 3, (r + 2) % 3) not in cells_for_zeros
            and cur_state[(c - 1) % 3][(r + 1) % 3] == ZERO and cur_state[(c - 2) % 3][(r + 2) % 3] == ZERO
            and c + r == 2
        ) or (
                (c, (r + 1) % 3) not in cells_for_zeros and (c, (r + 2) % 3) not in cells_for_zeros and
                cur_state[c][(r+1) % 3] == ZERO and cur_state[c][(r+2) % 3] == ZERO
        ) or (
                ((c + 1) % 3, r) not in cells_for_zeros and ((c + 2) % 3, r) not in cells_for_zeros and
                cur_state[(c + 1) % 3][r] == ZERO and cur_state[(c + 2) % 3][r] == ZERO
        ):
            row, column = (c, r)
        elif (
            ((c + 1) % 3, (r + 1) % 3) not in cells_for_zeros and ((c + 2) % 3, (r + 2) % 3) not in cells_for_zeros
            and cur_state[(c + 1) % 3][(r + 1) % 3] == CROSS and cur_state[(c + 2) % 3][(r + 2) % 3] == CROSS
            and c == r
        ) or (
            ((c - 1) % 3, (r + 1) % 3) not in cells_for_zeros and ((c - 2) % 3, (r + 2) % 3) not in cells_for_zeros
            and cur_state[(c - 1) % 3][(r + 1) % 3] == CROSS and cur_state[(c - 2) % 3][(r + 2) % 3] == CROSS
            and c + r == 2
        ) or (
            (c, (r + 1) % 3) not in cells_for_zeros and (c, (r + 2) % 3) not in cells_for_zeros and
            cur_state[c][(r+1) % 3] == CROSS and cur_state[c][(r+2) % 3] == CROSS
        ) or (
            ((c + 1) % 3, r) not in cells_for_zeros and ((c + 2) % 3, r) not in cells_for_zeros and
            cur_state[(c + 1) % 3][r] == CROSS and cur_state[(c + 2) % 3][r] == CROSS
        ):
            row, column = (c, r)
    if column == -1:
        row, column = random.choice(cells_for_zeros)

    cur_state[row][column] = ZERO
    if won(cur_state):
        await change_message(update, context, f"Проигрыш! :( {new_game_msg}")
        return FINISH_GAME

    await change_message(update, context, "Ваш ход! Поставьте крестик")
    return CONTINUE_GAME


def won(fields: list[list[str]]) -> bool:
    """
    Check if crosses or zeros have won the game
    :param fields - a list of lists of strings with crosses and zeros
    :return
      won - either True if there is a winner or False if there isn't yet
    """
    cross_paths = []
    for i in range(3):
        cross_paths.append([[i, 0], [i, 1], [i, 2]])
        cross_paths.append([[0, i], [1, i], [2, i]])

    cross_paths.append([[0, 0], [1, 1], [2, 2]])
    cross_paths.append([[2, 0], [1, 1], [0, 2]])

    for path in cross_paths:
        if (
            fields[path[0][0]][path[0][1]] in (CROSS, ZERO) and
            fields[path[0][0]][path[0][1]] == fields[path[1][0]][path[1][1]] and
            fields[path[1][0]][path[1][1]] == fields[path[2][0]][path[2][1]]
        ):
            return True

    return False


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    # reset state to default, so you can play again with /start
    context.user_data['keyboard_state'] = get_default_state()
    return ConversationHandler.END


def main() -> None:
    """Run the bot"""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Setup conversation handler with the states CONTINUE_GAME and FINISH_GAME
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end, pattern='^' + f'{r}{c}' + '$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
