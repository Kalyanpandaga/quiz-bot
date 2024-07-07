
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''

    if current_question_id is not None and current_question_id >= 0:
        if 'answers' not in session:
            session['answers'] = {}

        question = PYTHON_QUESTION_LIST[current_question_id]
        correct_answer = question['answer']

        if answer.strip().lower() == correct_answer.strip().lower():
            session['answers'][current_question_id] = True
        else:
            session['answers'][current_question_id] = False

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None or current_question_id < 0:
        next_question_id = 0
    elif current_question_id < len(PYTHON_QUESTION_LIST) - 1:
        next_question_id = current_question_id + 1
    else:
        return None, None

    next_question = PYTHON_QUESTION_LIST[next_question_id]['question_text']
    options = PYTHON_QUESTION_LIST[next_question_id]['options']
    options_text = "\n".join(f"{idx + 1}. {option}" for idx, option in enumerate(options))
    return f"{next_question}\n\n{options_text}", next_question_id


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    correct_answers = sum(session['answers'].values())
    total_questions = len(PYTHON_QUESTION_LIST)
    score = (correct_answers / total_questions) * 100

    return f"You've completed the quiz! Your score is {score:.2f}% ({correct_answers}/{total_questions} correct answers)."

