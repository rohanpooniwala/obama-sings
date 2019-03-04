from rev_ai import apiclient
import json
import time
import os
import datetime

client = apiclient.RevAiAPIClient(
    "02-SktQcq_WILkfcQ4ZFPC0A7B0jy57Mdef1Y1dv6I7dB-C_BQGduPIR03QxNomQVjX5nOt0uap-Zn35qDpDUcjwPN1_k")


def convertTime(t):
    return str(datetime.timedelta(seconds=t))


def S2T(audioFile):
    print("Sending ", audioFile, " for speech2text")
    job = client.submit_job_local_file(audioFile)
    id = job.id

    # id = "NIva4qKmLUt1"
    # id = "5xprc0oRG1id"

    # job_details = client.get_job_details(id)

    while True:
        time.sleep(2)
        print("Trying to fetch speech2text output")
        job_details = client.get_job_details(id)
        if str(job_details.status) == "JobStatus.TRANSCRIBED":
            print("Ready, reading json, txt, Txt  files")
            speech = client.get_transcript_text(id)
            # print(speech)
            with open(os.path.splitext(audioFile)[0] + ".txt", 'w') as f:
                f.write(speech)
            transcript = client.get_transcript_json(id)
            # print(transcript)
            # print(json.dumps(transcript, indent=4, sort_keys=True))
            # print("\n\n")
            data = {}
            data['IdleClips'] = []
            prevEndTS = []
            videoTxtTS = "Starting Time, Stopping Time, Word"
            for k in range(len(transcript["monologues"])):
                for i in range(len(transcript["monologues"][k]["elements"])):
                    note = transcript["monologues"][k]["elements"][i]
                    if note['type'] == "text" and note['confidence']>.7:
                        if note['value'] not in data:
                            data[note['value']] = []
                        data[note['value']].append(
                            os.path.basename(audioFile).replace('.wav','.mp4') + " ~(**)~ " + convertTime(note['ts']) + " ~(**)~ " + convertTime(note['end_ts']))
                        videoTxtTS += "\n"+convertTime(note['ts'])+','+convertTime(note['end_ts'])+','+note['value']
                    elif note['type'] != "text":
                        try:
                            next_note = transcript["monologues"][k]["elements"][i + 1]
                            data['IdleClips'].append(
                                os.path.basename(audioFile).replace('.wav','.mp4') + " ~(**)~ " + convertTime(prevEndTS) + " ~(**)~ " + convertTime(next_note['end_ts']))
                            videoTxtTS += "\n" + convertTime(prevEndTS) + ',' + convertTime(next_note['end_ts']) + ',IdleClips'
                        except Exception as e:
                            # print(e)
                            pass
                    if "end_ts" in note:
                        prevEndTS = note['end_ts']
            break
    # print(data)
    [print(i, len(data[i])) for i in data]
    with open(os.path.splitext(audioFile)[0] + ".json", 'w') as f:
        json.dump(data, f)
    with open(os.path.splitext(audioFile)[0] + "TimestampTxt.txt", 'w') as f:
        f.write(videoTxtTS)
    print("Ready")


if __name__ == "__main__":
    S2T("old/obama.mp4")
