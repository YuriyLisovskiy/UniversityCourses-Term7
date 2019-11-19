import os
import time
import subprocess


if __name__ == '__main__':
	print('main process started')

	filename = os.path.join(os.path.abspath('.'), '../lesson_10/main.py')
	async_task = subprocess.Popen(['python', filename])

	time.sleep(2)
	print('main process continue')

	print('subprocess finished? ', async_task.poll())
	print('main process finished')
	input()
