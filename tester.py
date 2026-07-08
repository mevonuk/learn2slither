import argparse


def main():
    """Read in preferences and direct program as appropriate"""
    parser = argparse.ArgumentParser(
        description="create a map, train a snake")

    parser.add_argument(
        "--program_mode",
        type=str,
        default="all",
        choices=["map", "all"],
        help="Mode of program execution"
    )

    parser.add_argument(
        "--sessions",
        type=int,
        default=1,
        help="Number of training sessions"
    )

    parser.add_argument(
        "--save",
        type=str,
        default="model/model1.txt",
        help="Name of saved model"
    )

    parser.add_argument(
        "--load",
        type=str,
        default=None,
        help="Name of loaded model"
    )

    parser.add_argument(
        "--visual",
        type=str,
        default="on",
        choices=["on", "off"],
        help="Display board"
    )

    parser.add_argument(
        "--learn",
        type=str,
        default="on",
        choices=["on", "off"],
        help="Is the agent learning?"
    )

    parser.add_argument(
        "--display",
        type=str,
        default="continuous",
        choices=["continuous", "step-by-step"],
        help="Display mode."
    )

    args = parser.parse_args()

    try:
        program_mode = args.program_mode
        sessions = args.sessions
        if sessions < 1:
            raise ValueError("Number of sessions must be positive.")
        save = args.save
        visual = args.visual
        load = args.load
        display = args.display
        learn = args.learn

        print("Running in program mode:", program_mode)

    except (TypeError, Exception, KeyboardInterrupt) as e:
        print(e)


if __name__ == "__main__":
    main()
