import argparse
from game_manager import run_snake


def main():
    """Read in preferences and direct program as appropriate"""
    parser = argparse.ArgumentParser(
        description="create a board, train a snake")

    parser.add_argument(
        "--sessions",
        type=int,
        default=10,
        help="Number of training sessions"
    )

    parser.add_argument(
        "--save",
        type=str,
        default="models/q_table.pkl",
        help="Name of saved model"
    )

    parser.add_argument(
        "--load",
        type=str,
        default="models/q_table10000.pkl",
        help="Name of loaded model"
    )

    parser.add_argument(
        "--step",
        type=str,
        default='off',
        choices=['off', 'on'],
        help="Step-by-step mode to display snake movement and vision"
    )

    parser.add_argument(
        "--explore",
        type=str,
        default='yes',
        choices=['yes', 'no'],
        help="Is the agent exploring?"
    )

    parser.add_argument(
        "--display",
        type=str,
        default='on',
        choices=['on', 'off'],
        help="Is the board displayed?"
    )

    args = parser.parse_args()

    try:
        sessions = args.sessions
        if sessions < 1:
            raise ValueError("Number of sessions must be positive.")
        model_output = args.save
        step = args.step
        model_input = args.load
        display = args.display
        explore = args.explore

        run_snake(sessions, explore, model_input, model_output, step, display)

    except (TypeError, Exception, KeyboardInterrupt) as e:
        print(e)


if __name__ == "__main__":
    main()
