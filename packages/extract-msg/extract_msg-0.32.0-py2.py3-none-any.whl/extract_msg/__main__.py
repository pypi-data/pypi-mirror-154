import logging
import os
import sys
import traceback

from extract_msg import __doc__, utils
from extract_msg.message import Message


def main() -> None:
    # Setup logging to stdout, indicate running from cli
    CLI_LOGGING = 'extract_msg_cli'
    args = utils.getCommandArgs(sys.argv[1:])
    level = logging.INFO if args.verbose else logging.WARNING

    # Determine where to save the files to.
    currentDir = os.getcwd() # Store this incase the path changes.
    if not args.zip:
        if args.out_path:
            if not os.path.exists(args.out_path):
                os.makedirs(args.out_path)
            out = args.out_path
        else:
            out = currentDir
    else:
        out = args.out_path if args.out_path else ''

    if args.dev:
        import extract_msg.dev
        extract_msg.dev.main(args, sys.argv[1:])
    elif args.validate:
        import json
        import pprint
        import time

        from extract_msg import validation

        valResults = {x[0]: validation.validate(x[0]) for x in args.msgs}
        filename = f'validation {int(time.time())}.json'
        print('Validation Results:')
        pprint.pprint(valResults)
        print(f'These results have been saved to {filename}')
        with open(filename, 'w') as fil:
            json.dump(valResults, fil)
        input('Press enter to exit...')
    else:
        if not args.dump_stdout:
            utils.setupLogging(args.config_path, level, args.log, args.file_logging)

        # Quickly make a dictionary for the keyword arguments.
        kwargs = {
            'allowFallback': args.allowFallback,
            'attachmentsOnly': args.attachmentsOnly,
            'charset': args.charset,
            'contentId': args.cid,
            'customFilename': args.out_name,
            'customPath': out,
            'html': args.html,
            'json': args.json,
            'preparedHtml': args.preparedHtml,
            'rtf': args.rtf,
            'useMsgFilename': args.use_filename,
            'zip': args.zip,
        }

        for x in args.msgs:
            try:
                with utils.openMsg(x[0]) as msg:
                    if args.dump_stdout:
                        print(msg.body)
                    else:
                        msg.save(**kwargs)
            except Exception as e:
                print(f'Error with file "{x[0]}": {traceback.format_exc()}')


if __name__ == '__main__':
    main()
