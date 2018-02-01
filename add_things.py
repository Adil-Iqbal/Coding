from os import remove, path, getcwd


print('\nThis python script adds four spaces to the beginning of each line in any text file.',
      '\nCurrent working directory: ' + getcwd() + '\n')


def confirmExecute():
    confirm = input('Are you in the right directory? (Y/N): ')
    if (confirm.lower() == 'n'):
        print('Please navigate to the correct directory and rerun the script.')
        exit()
    elif confirm.lower() == 'y':
        addSpaces()
    else:
        confirmExecute()


def addSpaces():
    targetFile = input('Type name of the target file (including extension): ')
    fileName, fileExt = path.splitext(targetFile)
    tempFile = fileName + '_copy' + fileExt
    header = "numbers.append(int("
    footer = "))"

    try:
        with open(targetFile, 'r') as target:
            with open(tempFile, 'w') as temp:
                for line in target:
                    new_line = header + str(line)
                    temp.write(new_line)

        with open(tempFile, 'r') as temp:
            with open(targetFile, 'w') as target:
                for line in temp:
                    target.write(line)

        with open(targetFile, 'r') as target:
            with open(tempFile, 'w') as temp:
                for line in target:
                    new_line = str(line) + footer
                    temp.write(new_line)

        with open(tempFile, 'r') as temp:
            with open(targetFile, 'w') as target:
                for line in temp:
                    target.write(line)

        remove(tempFile)
        print('File modification complete.')
        exit()

    except FileNotFoundError:
        print('That file was not found. Please check the file name and try again.\n')
        exit()


confirmExecute()