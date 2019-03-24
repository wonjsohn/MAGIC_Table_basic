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
def save_dataframe_os(dataframe, args, timeTag, startTimeFormatted):

    dataOutput_path = save_output_at("dataframeOutput")
    # save as csv
    fullfilename = os.path.join(dataOutput_path, timeTag+"_"  +  args["subject"]  +  "_success"+".csv")
    dataframe.to_csv(fullfilename, sep=',', encoding='utf-8')
    return fullfilename