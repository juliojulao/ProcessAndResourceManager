import PCB
import RCB
import sys

global in_count
in_count = 0

input_file = 'sample-input.txt'
output_file = 'output.txt'

def init():
	PCB.PCB_list = [0 for i in range(16)]
	p = PCB.Process(0,'running',0,[],{},0)
	PCB.PCB_list[0] = p
	PCB.curr_proc = p

	RCB.RCB_list = []
	RCB.RCB_list.append(RCB.RCB(0,1,1,[]))
	RCB.RCB_list.append(RCB.RCB(1,1,1,[]))
	RCB.RCB_list.append(RCB.RCB(2,2,2,[]))
	RCB.RCB_list.append(RCB.RCB(3,3,3,[]))

	PCB.RL = {2: [], 1: [], 0: []}
	PCB.RL[0].append(p)	


def readFile():
	global in_count
	output = open(output_file, encoding='utf8', mode='w')
	for line in sys.stdin.readlines():
		try:
			command = line.split()
			if len(command) == 0:
				continue

			elif command[0] == 'in':
				if in_count != 0:
					output.write("\n")
				init()
				in_count += 1

			elif command[0] == 'cr':
				PCB.curr_proc.create(int(command[1]))

			elif command[0] == 'de':
				PCB.curr_proc.destroy_recur(int(command[1]))
			
			elif command[0] == 'rq':
				PCB.curr_proc.request(int(command[1]),int(command[2]))
			
			elif command[0] == 'rl':
				PCB.curr_proc.release(int(command[1]),int(command[2]))			
			
			elif command[0] == 'to':
				PCB.timeout()

			elif command[0] == 'tree':
				PCB.curr_proc.get_tree(int(command[1]))

			elif command[0] == 'p':
				print("PCB List: {}".format(PCB.PCB_list))
				print("Ready List: {}".format(PCB.RL))
				print("Current process: \n{}".format(PCB.curr_proc))
				print("RCB List: {}".format(RCB.RCB_list))
				continue

			print('Current running process: {}'.format(PCB.curr_proc.pid))
			output.write(str(PCB.curr_proc.pid) + ' ')

		except:
			print("-1")
			output.write("-1 ")




def command_line():
	# init()
	# print('Current running process: {}'.format(PCB.curr_proc.pid))
	while True:
		try:
			line = input()
			command = line.split()
			if len(command) == 0:
				continue

			if command[0] == 'in':
				init()

			elif command[0] == 'cr':
				PCB.curr_proc.create(int(command[1]))

			elif command[0] == 'de':
				PCB.curr_proc.destroy_recur(int(command[1]))
			
			elif command[0] == 'rq':
				PCB.curr_proc.request(int(command[1]),int(command[2]))
			
			elif command[0] == 'rl':
				PCB.curr_proc.release(int(command[1]),int(command[2]))			
			
			elif command[0] == 'to':
				PCB.timeout()

			elif command[0] == 'ex':
				print(PCB.process_exists(int(command[1])))

			elif command[0] == 'p':
				print("PCB List: {}".format(PCB.PCB_list))
				print("Ready List: {}".format(PCB.RL))
				print("Current process: \n{}".format(PCB.curr_proc))
				print("RCB List: {}".format(RCB.RCB_list))

			elif command[0] == 'exit':
				break

			print('Current running process: {}'.format(PCB.curr_proc.pid))
		except:
			print('-1')

def main():
	init()
	PCB.curr_proc.create(1)
	PCB.curr_proc.create(1)
	PCB.curr_proc.create(2)
	PCB.curr_proc.create(2)
	PCB.curr_proc.create(2)
	PCB.curr_proc.create(2)
	if PCB.process_exists(3):
		print("Process 3 exists")
	if PCB.process_exists(4):
		print("Process 4 exists")
	else:
		print("Process 4 does not exist")
	print(PCB.PCB_list)
	print(PCB.curr_proc)
	PCB.timeout()
	PCB.curr_proc.create(2)
	PCB.curr_proc.create(2)
	PCB.curr_proc.create(2)
	print(PCB.PCB_list)
	print(PCB.curr_proc)
	PCB.timeout()
	PCB.timeout()
	PCB.timeout()
	print(PCB.PCB_list)
	print(PCB.curr_proc)
	PCB.curr_proc.destroy_recur(4)
	print(PCB.PCB_list)
	print(PCB.curr_proc)



if __name__ == '__main__':
	# main()
	# command_line()
	readFile()