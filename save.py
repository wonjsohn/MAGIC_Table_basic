import os


####################################################
### save at subdirectory, makedir if not exists ####
####################################################
def save_output_at(subdir):
    local_path = os.getcwd()

    dataOutput_path = os.path.join(str(local_path), "Output", subdir)
    if not os.path.exists(dataOutput_path):
        os.makedirs(dataOutput_path)
    return dataOutput_path



####################################################
### save video                                  ####
####################################################
def save_video_os(args, timeTag):

    dataOutput_path = save_output_at("videoOutput")
    videoName_common = timeTag + "_" + args.get("condition") + "_" + args["subject"]  + "_" + str(args["timed"]) + "s_" + str(
        args["fps"]) + "fps"

    videoName_path = os.path.join(dataOutput_path, videoName_common + ".mp4")

    return videoName_path


####################################################
### save using panda dataframe  (slower)        ####
####################################################
def save_dataframe_os(dataframe, args, timeTag, isSuccess, note, dir_of_move):

    # note can be stored if you wish here.

    dataOutput_path = save_output_at("dataframeOutput")
    # save as csv
    fullfilename = os.path.join(dataOutput_path, timeTag+"_" +dir_of_move+"_"+ args['idlevel'] + "_" +  args["subject"]  +  "_success"+str(isSuccess)+ ".csv")
    dataframe.to_csv(fullfilename, sep=',', encoding='utf-8')

    # write meta-data on top of the files. (hard attempt)
    with open(fullfilename, "w") as f:
        f.write('meta-data-length:' + str(12) + '\n')  # update as you add more meta-data.
        f.write('subjectID:' + args["subject"] + '\n')
        f.write('timeTag:' + timeTag + '\n')
        f.write('mode:' + args["mode"] + '\n')
        f.write('tasktype:' + args["tasktype"] + '\n')
        f.write('Direction:' + dir_of_move + '\n')
        f.write('marker:' + args["marker"] + '\n')
        f.write('thread:' + str(args["thread"]) + '\n')
        f.write('display:' + str(args["display"]) + '\n')
        f.write('ID:' + args['idlevel'] + '\n')
        f.write('handedness:' + args['handedness'] + '\n')
        f.write('Note:' + note + '\n')
        dataframe.to_csv(f, mode='a')


    return fullfilename