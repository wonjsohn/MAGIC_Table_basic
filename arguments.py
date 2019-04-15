import argparse

####################################################
###               arguments                     ####
####################################################
def get_arguments():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser(prog="PROG", description="program")
    ap.add_argument("-mod", "--mode", type=str,  default="feedback",help="mode: Feedback or record. Record mode can acheive high fps without tracking operation.")
    ap.add_argument('--version', action='version', version='%(prog)s 3.0')
    ap.add_argument("-d", "--display", type=int, default=-1, help="Whether or not frames should be displayed")
    ap.add_argument("-s", "--snapshot",type=int, default=0, help = "take a new snapshot")
    ap.add_argument("-tr", "--trace", type=int, default=-1,
    help="Whether or not traces should be displayed")
    ap.add_argument("-ltr", "--linetrace", type=int, default=-1,
    help="Whether or not line traces should be displayed")
    ap.add_argument("-th", "--thread", type=int, default=-1,
    help="Whether or not to use thread in reading frames")
    ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
    ap.add_argument("-f", "--fps", type=int, default=60,
    help="FPS of output video")
    ap.add_argument("-cod", "--codec", type=str, default="XVID",
    help="codec of output video")
    ap.add_argument("-c", "--condition",  default ="condition",
    help="condition of trial")
    ap.add_argument("-ts", "--targetsound",  type=int, default=1,
    help="sound on at target")
    ap.add_argument("-tv", "--targetvisual",  type=int, default=1,
    help="highlight if cursor on the target")
    ap.add_argument("-t", "--timed", type=int,  default=0,
    help="timed loop (s)")
    ap.add_argument("-m", "--marker", type=str,  default="object",
    help="markder: ball (default) / cup / both")
    ap.add_argument("-tt", "--tasktype", type=str,  default="p2p",
    help="game types: p2p (point-to-point), fig8.")
    ap.add_argument("-clk", "--clock", type=int, default="0",
    help="display clock and frame number.")
    ap.add_argument("-sid", "--subject", type=str, default="subj0",
    help="subject ID")
    ap.add_argument("-nt", "--note", type=int, default="0",
    help="Leave note if necessary")
    ap.add_argument("-hn", "--handedness", type=str, default="r",
    help="Righthander:r, lefthander:l")
    ap.add_argument("-idx", "--idlevel", type=str, default="ID1",
    help="Index of Difficulty (ID) 1 to 4.")
    ap.add_argument("-obs", "--obstacles", type=int, default="0",
    help="Existence of polygon obstacles")

    args = vars(ap.parse_args())
    print(args)

    if args["mode"] == "play":  #
        # args["targetsound"] = 1  # sound on at targets
        # args["targetvisual"] = 1
        args["display"] = 1
        # args["snapshot"] = 1
        args["thread"] = 1    # must
        # args["trace"] = 1
        args["linetrace"] = 1
        args["marker"] = "el_object"
    else:
        args["display"] = 1
        args["thread"] = 1  # must
        args["trace"] = 1
        args["linetrace"] = 1
        args["marker"] = "el_object"  # option
    return args


