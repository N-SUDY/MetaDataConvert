from math import floor as mathfloor
from re import findall as refindall
from asyncio import create_subprocess_exec, create_task, FIRST_COMPLETED
from asyncio import wait as asynciowait
from asyncio.subprocess import PIPE as asyncioPIPE
from pyrogram.errors.exceptions.flood_420 import FloodWait
from helper_fns.helper import getbotuptime, get_readable_time, delete_trash, get_human_size, get_stats, timex, process_checker, Timer
from asyncio import sleep as assleep
from helper_fns.progress_bar import get_progress_bar_string, get_progress_bar_from_percentage
from helper_fns.process import get_sub_process, get_master_process
from os.path import getsize, lexists
from json import loads

all_data = []
msg_data = ['Processing']
running_process = []
wpositions = {'5:5': 'Top Left', 'main_w-overlay_w-5:5': 'Top Right', '5:main_h-overlay_h': 'Bottom Left', 'main_w-overlay_w-5:main_h-overlay_h-5': 'Bottom Right'}


#############Checker################
async def check_task(pid, modes):
    while True:
        await assleep(1)
        if modes['files']>1:
          process_id = modes['process_id']
          subprocess_id = modes['subprocess_id']
          check_data = [[process_id, get_master_process()], [subprocess_id, get_sub_process()]]
        else:
            process_id = modes['process_id']
            check_data = [[process_id, get_master_process()]]
        check_data.append([pid, running_process])
        checker = await process_checker(check_data)
        if not checker:
            print(f"🔶{modes['process_type']} Task Checker Has Completed")
            break
    return


###########Logger###################
async def get_logs(process, pid, modes):
        while True:
                    try:
                            async for line in process:
                                        line = line.decode('utf-8').strip()
                                        print(line)
                                        all_data.append(line)
                                        if len(line)<3800:
                                            msg_data[-1] = line
                                        if modes['files']>1:
                                                process_id = modes['process_id']
                                                subprocess_id = modes['subprocess_id']
                                                check_data = [[process_id, get_master_process()], [subprocess_id, get_sub_process()]]
                                        else:
                                                process_id = modes['process_id']
                                                check_data = [[process_id, get_master_process()]]
                                        check_data.append([pid, running_process])
                                        checker = await process_checker(check_data)
                                        if not checker:
                                            print(f"🔶{modes['process_type']} Logger Has Completed")
                                            break
                    except ValueError:
                            continue
                    else:
                            break
        return

############Update_Message################
async def update_message(message, input_vid, output_vid, preset, process_log, duration, process_start_time, pid, datam, modes):
    try:
                txt = ''
                crf = modes['crf']
                encoder = modes['encoder']
                if modes['process_type'] == 'Watermark':
                        watermark_size = modes['watermark_size']
                        watermark_position = modes['watermark_position']
                        try:
                            position = wpositions[watermark_position]
                        except:
                            position = watermark_position
                        process_options =  f"\n🥽WPosition: {str(position)}\n🛸WSize: {str(watermark_size)}\n🎵CRF: {str(crf)}\n🍬Encoder: {str(encoder)}"
                elif modes['process_type'] == 'Compressing':
                        map_sub = modes['map_sub']
                        process_options = f"\n🛡Mode: {str(modes['process_type'])}\n🎵CRF: {str(crf)}\n🍬Encoder: {str(encoder)}\n🍄Copy Sub: {str(map_sub)}"
                elif modes['process_type'] == 'Converting':
                        map_sub = modes['map_sub']
                        process_options = f"\n🛡Mode: {str(modes['process_type'])}\n🎵CRF: {str(crf)}\n🍬Encoder: {str(encoder)}\n🍓Map Sub: {str(map_sub)}"
                else:
                        process_options = f"\n🛡Mode: {str(modes['process_type'])}\n🎵CRF: {str(crf)}\n🍬Encoder: {str(encoder)}"
                if modes['files']>1:
                        process_id = modes['process_id']
                        subprocess_id = modes['subprocess_id']
                        name = datam[0]
                        opt = datam[1]
                        remaining = datam[2]
                        process_name = datam[3]
                        sub_time = datam[4]
                        mas_time = datam[5]
                        failed = datam[6]
                        cancelled = datam[7]
                        wfailed = datam[8]
                        mfailed = datam[9]
                        fstats = f"❗Failed: {str(failed)}\n🚫Cancelled: {str(cancelled)}\n🤒FWatermark: {str(wfailed)}\n😬FMuxing: {str(mfailed)}"
                        ctext = f"⛔Skip Video: `/cancel sp {str(subprocess_id)}`"
                        ptext = f"🔴Cancel Task: `/cancel mp {str(process_id)}`"
                        process_head = f"{str(process_name)} ({opt})\n🎟️File: {name}\n🧶Remaining: {str(remaining)}"
                        process_foot = f"{str(fstats)}\n{str(ctext)}\n{str(ptext)}"
                else:
                    process_id = modes['process_id']
                    name = datam[0]
                    process_name = datam[1]
                    mas_time = datam[2]
                    process_head = f"{str(process_name)}\n🎟️File: {name}"
                    ptext = f"🔴Cancel Task: `/cancel mp {str(process_id)}`"
                    process_foot = f"{str(ptext)}"
                if modes['process_type'] != 'Merging':
                        process_head = process_head + process_options + f"\n♒Preset: {preset}\n🧭Duration: {get_readable_time(duration)}\n💽IN Size: {str(get_human_size(getsize(input_vid)))}"
                else:
                        map_merge = modes['map'] 
                        process_head = process_head + process_options + f"\n🍋Map: {str(map_merge)}\n♒Preset: {preset}\n🪁Total Files: {str(input_vid)}"
                while True:
                        await assleep(7)
                        print(f"🔶Updating {modes['process_type']} Message", pid)
                        current_time = timex()
                        masterprocess_time = get_readable_time(current_time - mas_time)
                        if modes['files']>1:
                                check_data = [[process_id, get_master_process()], [subprocess_id, get_sub_process()]]
                                subprocess_time = get_readable_time(current_time- sub_time)
                                process_mid = f"🔸SP Time: {str(subprocess_time)}\n🔹MP Time: {str(masterprocess_time)}"
                        else:
                                check_data = [[process_id, get_master_process()]]
                                process_mid = f"🔹MP Time: {str(masterprocess_time)}"
                        check_data.append([pid, running_process])
                        checker = await process_checker(check_data)
                        if not checker:
                            print(f"🔶{modes['process_type']} Message Updater Has Completed")
                            break
                        execution_time = get_readable_time(current_time - process_start_time)
                        botupt = getbotuptime()
                        try:
                                logs = all_data[-2] + "\n" + msg_data[-1]
                        except:
                            logs = msg_data[-1]
                        if len(logs)>3000:
                            logs = msg_data[-1]
                        ot_size = getsize(output_vid)
                        if modes['process_type'] != 'Merging':
                                with open(process_log, 'r+') as file:
                                                        text = file.read()
                                                        frame = refindall("frame=(\d+)", text)
                                                        time_in_us=refindall("out_time_ms=(\d+)", text)
                                                        bitrate = refindall("bitrate=(\d+)", text)
                                                        fps = refindall("fps=(\d+)", text)
                                                        progress=refindall("progress=(\w+)", text)
                                                        speed=refindall("speed=(\d+\.?\d*)", text)
                                                        if len(frame):
                                                            frame = int(frame[-1])
                                                        else:
                                                            frame = 1;
                                                        if len(speed):
                                                            speed = speed[-1]
                                                        else:
                                                            speed = 1;
                                                        if len(time_in_us):
                                                            time_in_us = time_in_us[-1]
                                                        else:
                                                            time_in_us = 1;
                                                        if len(progress):
                                                            if progress[-1] == "end":
                                                                break
                                                        if len(bitrate):
                                                            bitrate = bitrate[-1].strip()
                                                        else:
                                                            bitrate = "0"
                                                        if len(fps):
                                                            fps = fps[-1].strip()
                                                        else:
                                                            fps = "0"
                                                        elapsed_time = int(time_in_us)/1000000
                                                        out_time = get_readable_time(elapsed_time)
                                                        difference = mathfloor( (duration - elapsed_time) / float(speed) )
                                                        ETA = "-"
                                                        if difference > 0:
                                                            ETA = get_readable_time(difference)
                                                        perc = f"{elapsed_time * 100 / duration:.1f}%"
                                                        progress_bars = get_progress_bar_string(elapsed_time, duration)
                                                        eta_raw = (ot_size/int(time_in_us))*duration
                                                        eta_size =get_human_size(eta_raw*1024*1024)
                                                        pro_bar = f"{str(process_head)}\n\n\n{progress_bars}\n\n ┌ 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜:【 {perc} 】\n ├ 𝚂𝚙𝚎𝚎𝚍:【 {speed}x 】\n ├ 𝙱𝚒𝚝𝚛𝚊𝚝𝚎:【 {bitrate}kbits/s 】\n ├ 𝙵𝙿𝚂:【 {fps} 】\n ├ 𝚁𝚎𝚖𝚊𝚒𝚗𝚒𝚗𝚐:【 {get_readable_time((duration - elapsed_time))} 】\n └ 𝙿𝚛𝚘𝚌𝚎𝚜𝚜𝚎𝚍:【 {str(out_time)} 】\n\n\n⚡️●●●● 𝙿𝚛𝚘𝚌𝚎𝚜𝚜 ●●●●⚡️\n\n⚙{str(logs)}\n\n\n💾OT Size: {str(get_human_size(ot_size))}\n🚂ETA Size: {str(eta_size)}\n⏰️ETA Time: {ETA}\n⛓EX Time: {str(execution_time)}\n{str(process_mid)}\n{str(get_stats())}\n♥️Bot Uptime: {str(botupt)}\n{str(process_foot)}"
                        else:
                                pro_bar = f"{str(process_head)}\n\n\n⚡️●●●● 𝙿𝚛𝚘𝚌𝚎𝚜𝚜 ●●●●⚡️\n\n⚙{str(logs)}\n\n\n💾OT Size: {str(get_human_size(ot_size))}\n⛓EX Time: {str(execution_time)}\n{str(process_mid)}\n{str(get_stats())}\n♥️Bot Uptime: {str(botupt)}\n{str(process_foot)}"
                        if txt!=pro_bar:
                                txt=pro_bar
                                try:
                                    await message.edit(text=pro_bar)
                                except FloodWait as e:
                                    await assleep(e.value)
                                except Exception as e:
                                    print(e)
                return
    except Exception as e:
        await message.edit(text=f'❌Error While Updating Message: {str(e)}')
        return
    
    


#############Generating Screenshoot######################
async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(timex()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncioPIPE,
        stderr=asyncioPIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None
    

##############Run CMD##################
async def run_process_command(command):
    print(command)
    try:
        process = await create_subprocess_exec(
            *command,
            stdout=asyncioPIPE,
            stderr=asyncioPIPE,
            )
        while True:
                    try:
                            async for line in process.stderr:
                                        line = line.decode('utf-8').strip()
                                        print(line)
                    except ValueError:
                            continue
                    else:
                            break
        await process.wait()
        return_code = process.returncode
        if return_code == 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


###################FFMPEG Engine#############################
async def ffmpeg_engine(bot, user_id, message, command, input_vid, output_vid, preset, process_log, duration, datam, modes):
    print(f"🔶Starting {str(datam[0])} {modes['process_type']} Process")
    global all_data
    global msg_data
    print(command)
    all_data = []
    msg_data = ['Processing']
    process_start_time = timex()
    process = await create_subprocess_exec(
            *command,
            stdout=asyncioPIPE,
            stderr=asyncioPIPE,
            )
    pid = process.pid
    running_process.append(pid)
    task = create_task(check_task(pid, modes))
    log_task = create_task(get_logs(process.stderr, pid, modes))
    update_msg = create_task(update_message(message, input_vid, output_vid, preset, process_log, duration, process_start_time, pid, datam, modes))
    done, pending = await asynciowait([task, process.wait()], return_when=FIRST_COMPLETED)
    print(f"🔶{str(datam[0])} {modes['process_type']} Process Completed")
    return_code = process.returncode
    running_process.remove(pid)
    await delete_trash(process_log)
    print(f"🔶{str(datam[0])} {modes['process_type']} Process Return Code: ", return_code)
    if task not in pending:
                try:
                        print(f"🔶Terminating {modes['process_type']} Process")
                        process.terminate()
                        print(f"🔶{modes['process_type']} Process Terminated")
                except Exception as e:
                        print(e)
    else:
                try:
                        print(f"🔶Cancelling {modes['process_type']} Task Checker")
                        task.cancelled()
                        print(f"🔶Awaiting {modes['process_type']} Task Checker")
                        await task
                        print(f"🔶{modes['process_type']} Task Checker Cancelled")
                except Exception as e:
                        print(e)
    try:
            print(f"🔶Cancelling {modes['process_type']} Message Updater")
            update_msg.cancelled()
            print(f"🔶Awaiting {modes['process_type']} Message Updater")
            await update_msg
            print(f"🔶{modes['process_type']} Message Updater Cancelled")
    except Exception as e:
            print(e)
    try:
            print(f"🔶Cancelling {modes['process_type']} Logger")
            log_task.cancelled()
            print(f"🔶Awaiting {modes['process_type']} Logger")
            await log_task
            print(f"🔶{modes['process_type']} Logger Cancelled")
    except Exception as e:
            print(e)
    if modes['files']>1:
                    process_id = modes['process_id']
                    subprocess_id = modes['subprocess_id']
                    check_data = [[process_id, get_master_process()], [subprocess_id, get_sub_process()]]
    else:
                    process_id = modes['process_id']
                    check_data = [[process_id, get_master_process()]]
    checker = await process_checker(check_data)
    if not checker:
        print(f"⛔{str(datam[0])} {modes['process_type']} Process Cancelled By User.")
        all_data = []
        msg_data = ['Processing']
        return [True, True]
    elif return_code == 0:
        print(f"✅{str(datam[0])} {modes['process_type']} Process Successfully Completed.")
        all_data = []
        msg_data = ['Processing']
        return [True, False]
    else:
        cc=f"{str(datam[0])}\n\n❌{modes['process_type']} Process Failed."
        print(cc)
        fail_file = f"{str(datam[0])}_{modes['process_type']}_log.txt"
        zxx = open(fail_file, "w", encoding="utf-8")
        zxx.write(str(all_data))
        zxx.close()
        await bot.send_document(chat_id=user_id, document=fail_file, caption=cc)
        all_data = []
        msg_data = ['Processing']
        await delete_trash(fail_file)
        return [False]


############Rclone Drive Link##################
async def getdrivelink(search_command):
    process = await create_subprocess_exec(
        *search_command, stdout=asyncioPIPE
    )
    stdout, _ = await process.communicate()
    try:
        stdout = stdout.decode().strip()
        print(stdout)
        data = loads(stdout)
        gid = data[0]["ID"]
        # name = data[0]["Name"]
        link = f'https://drive.google.com/file/d/{gid}/view'
        print(link)
        return [True, link]
    except Exception as e:
        return [False, e]



############Rclone Message Updater############
async def update_rclone_message(process, pid, message, input_vid, datam, modes):
        timer = Timer(7)
        txt = ''
        # fsize = str(get_human_size(getsize(input_vid)))
        while True:
                    try:
                            async for line in process:
                                        line = line.decode().strip()
                                        print(line)
                                        all_data.append(line)
                                        if len(line)<3800:
                                            msg_data[-1] = line
                                        if modes['files']>1:
                                                process_id = modes['process_id']
                                                subprocess_id = modes['subprocess_id']
                                                check_data = [[process_id, get_master_process()], [subprocess_id, get_sub_process()]]
                                        else:
                                                process_id = modes['process_id']
                                                check_data = [[process_id, get_master_process()]]
                                        check_data.append([pid, running_process])
                                        checker = await process_checker(check_data)
                                        if not checker:
                                            print(f"🔶{modes['process_type']} Logger Has Completed")
                                            break
                                        if timer.can_send():
                                            try:
                                                mat = refindall("Transferred:.*ETA.*", line)
                                                if mat is not None:
                                                    if len(mat) > 0:
                                                        nstr = mat[0].replace("Transferred:", "")
                                                        nstr = nstr.strip()
                                                        nstr = nstr.split(",")
                                                        prg = nstr[1].strip("% ")
                                                        progress = get_progress_bar_from_percentage(prg)
                                                        dwdata = nstr[0].strip().split('/')
                                                        cur = dwdata[0].strip()
                                                        fsize = dwdata[1].strip()
                                                        eta = nstr[3].strip().replace('ETA', '').strip()
                                                        if modes['files']>1:
                                                            name = datam[0]
                                                            opt = datam[1]
                                                            remaining = datam[2]
                                                            process_name = datam[3]
                                                            mode = datam[4]
                                                            sub_time = datam[5]
                                                            mas_time = datam[6]
                                                            failed = datam[7]
                                                            cancelled = datam[8]
                                                            wfailed = datam[9]
                                                            mfailed = datam[10]
                                                            fstats = f"❗Failed: {str(failed)}\n🚫Cancelled: {str(cancelled)}\n🤒FWatermark: {str(wfailed)}\n😬FMuxing: {str(mfailed)}"
                                                            subprocess_time = get_readable_time(timex() - sub_time)
                                                            masterprocess_time = get_readable_time(timex() - mas_time)
                                                            bot_uptime = getbotuptime()
                                                            ctext = f"⛔Skip Video: `/cancel sp {str(subprocess_id)}`"
                                                            ptext = f"🔴Cancel Task: `/cancel mp {str(process_id)}`"
                                                            process_head = f"{str(process_name)} ({opt})\n🎟️File: {name}\n🧶Remaining: {str(remaining)}"
                                                            process_mid = f"🔸SP Time: {str(subprocess_time)}\n🔹MP Time: {str(masterprocess_time)}"
                                                            process_foot = f"♥️Bot Uptime: {str(bot_uptime)}\n{str(fstats)}\n{str(ctext)}\n{str(ptext)}"
                                                        else:
                                                            name = datam[0]
                                                            process_name = datam[1]
                                                            mode = datam[2]
                                                            mas_time = datam[3]
                                                            masterprocess_time = get_readable_time(timex() - mas_time)
                                                            bot_uptime = getbotuptime()
                                                            process_head = f"{str(process_name)}\n🎟️File: {name}"
                                                            process_mid = f"🔹MP Time: {str(masterprocess_time)}"
                                                            ptext = f"🔴Cancel Task: `/cancel mp {str(process_id)}`"
                                                            process_foot = f"♥️Bot Uptime: {str(bot_uptime)}\n{str(ptext)}"
                                                        process_mid = f"⏰️ETA Time: {eta}\n" + process_mid
                                                        pro_bar = f"{str(process_head)}\n\n\n {str(progress)}\n\n ┌ 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜:【 {prg}% 】\n ├ 𝚂𝚙𝚎𝚎𝚍:【 {nstr[2]} 】\n ├ {mode}:【 {cur} 】\n └ 𝚂𝚒𝚣𝚎:【 {fsize} 】\n\n\n{str(process_mid)}\n{str(get_stats())}\n{str(process_foot)}"
                                                        if txt!=pro_bar:
                                                            txt=pro_bar
                                                            try:
                                                                await message.edit(text=pro_bar)
                                                            except FloodWait as e:
                                                                await assleep(e.value)
                                                            except Exception as e:
                                                                print(e)
                                            except Exception as e:
                                                            await message.edit(text=f'❌Error While Updating Message: {str(e)}')
                    except ValueError:
                            continue
                    else:
                            break
        return


##############Rclone##################
async def upload_rclone(bot, user_id, message, command, input_vid, datam, modes, search_command):
    print(f"🔶Starting {str(datam[0])} {modes['process_type']} Process")
    global all_data
    global msg_data
    all_data = []
    msg_data = ['Processing']
    process = await create_subprocess_exec(
            *command,
            stdout=asyncioPIPE,
            stderr=asyncioPIPE,
            )
    pid = process.pid
    running_process.append(pid)
    task = create_task(check_task(pid, modes))
    log_task = create_task(update_rclone_message(process.stdout, pid, message, input_vid, datam, modes))
    done, pending = await asynciowait([task, process.wait()], return_when=FIRST_COMPLETED)
    print(f"🔶{str(datam[0])} {modes['process_type']} Process Completed")
    return_code = process.returncode
    running_process.remove(pid)
    print(f"🔶{str(datam[0])} {modes['process_type']} Process Return Code: ", return_code)
    if task not in pending:
                try:
                        print(f"🔶Terminating {modes['process_type']} Process")
                        process.terminate()
                        print(f"🔶{modes['process_type']} Process Terminated")
                except Exception as e:
                        print(e)
    else:
                try:
                        print(f"🔶Cancelling {modes['process_type']} Task Checker")
                        task.cancelled()
                        print(f"🔶Awaiting {modes['process_type']} Task Checker")
                        await task
                        print(f"🔶{modes['process_type']} Task Checker Cancelled")
                except Exception as e:
                        print(e)
    try:
            print(f"🔶Cancelling {modes['process_type']} Logger")
            log_task.cancelled()
            print(f"🔶Awaiting {modes['process_type']} Logger")
            await log_task
            print(f"🔶{modes['process_type']} Logger Cancelled")
    except Exception as e:
            print(e)
    if modes['files']>1:
                    process_id = modes['process_id']
                    subprocess_id = modes['subprocess_id']
                    check_data = [[process_id, get_master_process()], [subprocess_id, get_sub_process()]]
    else:
                    process_id = modes['process_id']
                    check_data = [[process_id, get_master_process()]]
    checker = await process_checker(check_data)
    if not checker:
        print(f"⛔{str(datam[0])} {modes['process_type']} Process Cancelled By User.")
        all_data = []
        msg_data = ['Processing']
        return [True, True]
    elif return_code == 0:
        print(f"✅{str(datam[0])} {modes['process_type']} Process Successfully Completed.")
        all_data = []
        msg_data = ['Processing']
        drive_link = await getdrivelink(search_command)
        if drive_link[0]:
            return [True, False, True, drive_link[1]]
        else:
            return [True, False, False, drive_link[1]]
    else:
        cc=f"{str(datam[0])}\n\n❌{modes['process_type']} Process Failed."
        print(cc)
        fail_file = f"{str(datam[0])}_{modes['process_type']}_log.txt"
        zxx = open(fail_file, "w", encoding="utf-8")
        zxx.write(str(all_data))
        zxx.close()
        await bot.send_document(chat_id=user_id, document=fail_file, caption=cc)
        all_data = []
        msg_data = ['Processing']
        await delete_trash(fail_file)
        return [False]
    