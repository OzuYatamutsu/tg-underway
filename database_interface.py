from constants import DATABASE_PATH
from database import Database
from state import State
from step import Step


def init(username: str):
    """
    Initializes the user to a starting state.
    """

    with Database(DATABASE_PATH) as db:
        db.query(
            "INSERT INTO USER_STATE(username, state) VALUES (%s, %d)",
            username, State.ASK_STEP_INITIAL.value
        )


def transition_state(username: str, target_state: State):
    """
    Transitions the user to the target state.
    Requires the user to be inited.
    """

    with Database(DATABASE_PATH) as db:
        db.query(
            "UPDATE USER_STATE SET state=%d WHERE username=%s",
            target_state.value, username
        )


def add_step(username: str, step_num: int, step: str):
    """
    Adds a step to track.
    """

    with Database(DATABASE_PATH) as db:
        db.query(
            "INSERT INTO STEPS(username, step_num, step, completed) VALUES (%s, %d, %s, FALSE)",
            username, step_num, step
        )


def complete_step(username: str, step_num: int):
    """
    Completes the given step in a sequence.
    """

    with Database(DATABASE_PATH) as db:
        db.query(
            "UPDATE STEPS SET completed=TRUE WHERE username=%s AND step_num=%d",
            username, step_num
        )


def uncomplete_step(username: str, step_num: int):
    """
    Undos completion of the given step in a sequence.
    """

    with Database(DATABASE_PATH) as db:
        db.query(
            "UPDATE STEPS SET completed=FALSE WHERE username=%s AND step_num=%d",
            username, step_num
        )


def get_all_steps(username: str) -> list:
    """
    Returns a list of Step objects corresponding to the given user.
    """

    with Database(DATABASE_PATH) as db:
        return [
            Step(row['description'], not not row['completed'])
            for row in db.query(
                "SELECT description, completed FROM STEPS WHERE username=%s ORDER BY step_num ASC",
                username
            )
        ]


def get_step_by_username_and_num(username: str, step_num: int) -> Step:
    """Returns a Step object corresponding to the username and given number."""

    with Database(DATABASE_PATH) as db:
        raw_step = db.query(
            "SELECT description, completed FROM STEPS "
            "WHERE username=%s "
            "AND step_num=%d "
            "LIMIT 1", step_num
        )[0])

    return Step(
        description=raw_step['description'],
        completed=(not not raw_step['completed'])
    )


def get_next_step_num(username: str) -> int:
    """Returns the number of the next uncompleted step."""

    with Database(DATABASE_PATH) as db:
        return db.query(
            "SELECT step_num FROM STEPS WHERE username=%s "
            "AND completed=FALSE "
            "ORDER BY step_num ASC LIMIT 1"
        )[0]['step_num']


def user_is_active(username: str) -> bool:
    """Returns whether or not the user is being tracked or not."""

    with Database(DATABASE_PATH) as db:
        result = db.query(
            "SELECT state FROM USER_STATE WHERE username=%s", username
        )

        return (not not result) and State(result[0]) in [State.TRACKING, State.COMPLETE]

