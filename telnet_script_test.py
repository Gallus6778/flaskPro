import asyncio, telnetlib3

@asyncio.coroutine
def shell(reader, writer):
    inc = 1
    while True:
        # read stream until '?' mark is found
        outp = yield from reader.read(4096)
        if not outp:
            # End of File
            break
        elif 'ENTER USERNAME < ' in outp:
            # reply all questions with 'y'.
            writer.write('CHATBO\n\r')
            print('ok1')
            print(outp, flush=True)
            writer.write('1234567890\n\r')
            print('ok2')
            print(outp, flush=True)
        else: #'ENTER PASSWORD < ' in outp:
            if inc == 1:
                writer.write('ZMMI:MSISDN=237669595858:;\n\r')
                # print(outp, flush=True)
                inc += 1
            elif inc == 2:
                writer.write('ZMMO:MSISDN=237669595858:;\n\r')
                # print(outp, flush=True)
                inc += 1
            elif inc == 3:
                # writer.write('ZMMS:MSISDN=237669595858:;\n\r')
                # print(outp, flush=True)
                inc += 1
            elif inc == 4:
                # print(outp, flush=True)
                inc += 1
                break
            elif inc == 5:
                # print(outp, flush=True)
                inc += 1
                break
            elif inc == 6:
                # print(outp, flush=True)
                inc += 1
            # elif inc == 7:
            #     print(outp, flush=True)
            #     inc += 1
                break
        # elif 'MAIN LEVEL COMMAND <___>':
        print(outp, flush=True)
            # break
            # < ___ >
            # <
            # display all server output
        # print(outp, flush=True)

    # EOF
    print()

loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection('10.124.206.68', 23, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)